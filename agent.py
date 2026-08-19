"""
agent.py — Pleximus AI Agent core.

Integrates Google Gemini with four tools via the google-genai SDK's
automatic function-calling feature. Each tool is a plain Python function;
the SDK handles schema generation and execution loop.
"""

import os
from google import genai
from google.genai import types

from tools.calculator import calculate
from tools.weather import get_weather
from tools.text_utils import process_text
from tools.unit_converter import convert_unit


# ---------------------------------------------------------------------------
# Tool wrapper functions (docstrings are read by Gemini to decide when to call)
# ---------------------------------------------------------------------------

def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression and return the numeric result.

    Use this tool whenever the user asks to:
    - calculate, compute, or evaluate a math expression
    - perform arithmetic: addition, subtraction, multiplication, division
    - compute powers, percentages, or parenthesised expressions

    Args:
        expression: A clean mathematical expression string, e.g. '25 * 18',
                    '(100 + 50) / 5', '2 ** 10', '1250 / 25 + 17'.

    Returns:
        The numeric result as a string, or an error message if invalid.
    """
    print(f"\n  [Tool: calculator] expression='{expression}'")
    result = calculate(expression)
    print(f"  [Tool Result] {result}")
    return result


def weather_lookup(city: str) -> str:
    """
    Fetch the current weather for a given city name.

    Use this tool whenever the user asks about weather, temperature,
    wind speed, or atmospheric conditions in a city.

    Args:
        city: The name of the city, e.g. 'Mumbai', 'Ratnagiri', 'London'.

    Returns:
        A formatted weather summary with temperature, wind speed, and condition.
    """
    print(f"\n  [Tool: weather_lookup] city='{city}'")
    result = get_weather(city)
    print(f"  [Tool Result]\n  {result}")
    return result


def text_utility(operation: str, text: str) -> str:
    """
    Perform a text or string operation on a piece of text.

    Use this tool whenever the user asks to:
    - count words or characters
    - reverse text or a string
    - convert text to uppercase or lowercase
    - clean up or remove extra spaces from text

    Args:
        operation: The operation to perform. Must be one of:
                   'word_count'    — count the number of words
                   'char_count'    — count the number of characters
                   'reverse'       — reverse the text
                   'uppercase'     — convert to all caps
                   'lowercase'     — convert to all lowercase
                   'remove_spaces' — collapse multiple spaces into one
        text: The input text to process.

    Returns:
        The result of the operation as a string.
    """
    print(f"\n  [Tool: text_utility] operation='{operation}' text='{text[:60]}{'...' if len(text) > 60 else ''}'")
    result = process_text(operation, text)
    print(f"  [Tool Result] {result}")
    return result


def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
    """
    Convert a numeric value from one unit of measurement to another.

    Use this tool whenever the user asks to convert between units, including:
    - Length: meters, kilometers, centimeters, miles, feet
    - Weight: kilograms, grams, pounds
    - Temperature: Celsius, Fahrenheit, Kelvin

    Args:
        value:     The numeric value to convert (e.g., 5.0, 72.0, 300.0).
        from_unit: The source unit as a string (e.g., 'km', 'kg', 'Fahrenheit').
        to_unit:   The target unit as a string (e.g., 'meters', 'pounds', 'Celsius').

    Returns:
        A human-readable conversion result, e.g. '5 km = 5000 meters'.
    """
    print(f"\n  [Tool: unit_converter] {value} {from_unit} → {to_unit}")
    result = convert_unit(value, from_unit, to_unit)
    print(f"  [Tool Result] {result}")
    return result


# ---------------------------------------------------------------------------
# Agent class
# ---------------------------------------------------------------------------

SYSTEM_INSTRUCTION = """You are a helpful AI assistant for Pleximus Inc.
You have access to four tools:
1. calculator       — for any math or arithmetic
2. weather_lookup   — for weather queries about any city
3. text_utility     — for word count, character count, reverse, uppercase, lowercase, remove spaces
4. unit_converter   — for converting between length, weight, or temperature units

IMPORTANT RULES:
- Always use the appropriate tool when one applies.
- Do NOT guess numerical answers; always use the calculator tool.
- Do NOT invent weather data; always use the weather_lookup tool.
- For text operations, always use the text_utility tool.
- For unit conversions, always use the unit_converter tool.
- After receiving a tool result, summarise it clearly for the user.
- Be concise. Do not add unnecessary padding.
"""

TOOLS = [calculator, weather_lookup, text_utility, unit_converter]


class PleximusAgent:
    """Conversational agent powered by Gemini with tool-calling support."""

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.chat = self._new_chat()

    def _new_chat(self):
        """Create a new stateful chat session with all tools registered."""
        return self.client.chats.create(
            model=self.model,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                tools=TOOLS,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=False
                ),
            ),
        )

    def ask(self, user_message: str) -> str:
        """
        Send a user message and return the agent's final text response.
        Tool calls and results are handled automatically by the SDK.
        """
        try:
            response = self.chat.send_message(user_message)
            return response.text or "(No response from agent)"
        except genai.errors.APIError as e:
            return f"Gemini API error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"

    def reset(self):
        """Start a fresh conversation."""
        self.chat = self._new_chat()
