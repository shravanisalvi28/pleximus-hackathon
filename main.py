"""
main.py — CLI entry point for the Pleximus AI Agent.
Loads environment variables, initialises the agent, and runs the REPL loop.
"""

import os
import sys
from dotenv import load_dotenv
from agent import PleximusAgent


BANNER = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║             PLEXIMUS INC.  —  AI TOOL AGENT                 ║
║           FAMT Ratnagiri  •  AI & ML Hackathon               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

  I can help you with:
    • Calculations          e.g. "What is (100 + 50) * 3?"
    • Weather               e.g. "What's the weather in Mumbai?"
    • Text utilities        e.g. "Count the words in: hello world"
    • Unit conversions      e.g. "Convert 5 km to meters"

  Type 'reset' to start a fresh conversation.
  Type 'exit' or 'quit' to stop.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

EXAMPLE_QUERIES = [
    "What is 25 * 18?",
    "Calculate 1250 / 25 + 17",
    "What's the weather in Ratnagiri?",
    "Count the words in: Artificial intelligence is amazing",
    "Reverse this text: hello world",
    "Convert 5 kilometers to meters",
    "Convert 72 Fahrenheit to Celsius",
    "Convert 10 kg to pounds",
]


def load_api_key() -> str:
    """Load and validate the Gemini API key from environment."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_api_key_here":
        print("ERROR: GEMINI_API_KEY is not set.")
        print("  1. Copy .env.example to .env")
        print("  2. Replace 'your_api_key_here' with your actual Gemini API key.")
        print("  3. Get a free key at: https://aistudio.google.com/app/apikey")
        sys.exit(1)
    return api_key


def run():
    """Main REPL loop."""
    api_key = load_api_key()

    print(BANNER)

    try:
        agent = PleximusAgent(api_key=api_key)
    except Exception as e:
        print(f"Failed to initialise agent: {e}")
        sys.exit(1)

    print("  Ready. Ask me anything!\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "bye"):
            print("\nGoodbye! Good luck at the hackathon!")
            break

        if user_input.lower() == "reset":
            agent.reset()
            print("\n[Conversation reset]\n")
            continue

        if user_input.lower() in ("help", "examples"):
            print("\n  Example queries you can try:")
            for q in EXAMPLE_QUERIES:
                print(f"    • {q}")
            print()
            continue

        print()  # spacing before agent output
        response = agent.ask(user_input)
        print(f"\nAgent: {response}\n")
        print("━" * 62)


if __name__ == "__main__":
    run()
