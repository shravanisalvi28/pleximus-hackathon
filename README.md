# 🤖 BeforeTheAnswer AI

**Pleximus Inc. — AI & ML Hackathon | FAMT Ratnagiri**

---

## Problem Statement

Most chatbots only use text — they can't actually *do* anything. Real AI systems in production combine language understanding with tool use: the model reads a request, picks a tool, executes it, and returns a grounded answer.

## Solution

A conversational AI agent powered by **Google Gemini** that:

1. Understands your natural-language request
2. Decides **which tool** to call (the LLM makes this decision — no keyword matching)
3. Executes the tool
4. Delivers a clear, grounded response

---

## Features

| Feature | Detail |
|---|---|
| 🧮 Calculator | Safe AST-based arithmetic — no unsafe `eval()` |
| 🌤️ Weather | Live data via Open-Meteo + geocoding (no API key needed) |
| 🔤 Text Utility | Word count, char count, reverse, uppercase, lowercase |
| 📐 Unit Converter | Length, weight, temperature — fully offline |
| 🔁 Multi-turn chat | Remembers context across turns |
| 🛡️ Error handling | Graceful messages, never crashes |
| 🔑 Secure key loading | API key read from `.env`, never hardcoded |

---

## Architecture

```
User Input (natural language)
        │
        ▼
  Google Gemini LLM
  (reads tool descriptions,
   decides which tool to call)
        │
   ┌────┴────────────────────┐
   │                         │
   ▼                         ▼
Tool Selected?            No tool needed?
   │                         │
   ▼                         ▼
Execute Tool           Direct response
   │
   ▼
Return result to Gemini
   │
   ▼
Gemini generates final
natural-language response
   │
   ▼
 User
```

### Project Structure

```
pleximus_hackathon/
│
├── main.py               ← CLI entry point (REPL loop)
├── agent.py              ← Gemini integration + tool registration
├── tools/
│   ├── __init__.py
│   ├── calculator.py     ← Safe AST-based math evaluator
│   ├── weather.py        ← Open-Meteo weather + geocoding
│   ├── text_utils.py     ← Local text manipulation
│   └── unit_converter.py ← Length/weight/temperature converter
│
├── .env.example          ← Template — copy to .env and fill in your key
├── .gitignore            ← .env is always excluded
├── requirements.txt
└── README.md
```

---

## Tools

### 1. Calculator
- **Purpose**: Arithmetic — addition, subtraction, multiplication, division, powers, parentheses
- **Safety**: Uses Python `ast` module to parse expressions — no `eval()` on arbitrary input
- **Edge cases**: Division by zero, invalid expressions

### 2. Weather Lookup
- **API**: [Open-Meteo](https://open-meteo.com/) — free, no API key required
- **Geocoding**: [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api) — converts city names to coordinates
- **Returns**: Temperature (°C), wind speed (km/h), weather condition
- **Edge cases**: Unknown city, network failure, empty API response

### 3. Word/Text Utility
- **Purpose**: Local string manipulation — no external dependencies
- **Operations**: `word_count`, `char_count`, `reverse`, `uppercase`, `lowercase`, `remove_spaces`

### 4. Unit Converter *(Extension Tool)*
- **Categories**: Length, Weight, Temperature
- **Supported units**:
  - Length: `meters, kilometers, centimeters, miles, feet`
  - Weight: `kilograms, grams, pounds`
  - Temperature: `Celsius, Fahrenheit, Kelvin`
- **Logic**: Local conversion — no API needed

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM | Google Gemini 2.0 Flash |
| SDK | `google-genai` (unified Python SDK) |
| Weather API | Open-Meteo (free, no key) |
| Env secrets | `python-dotenv` |
| HTTP | `requests` |
| Python | 3.8+ |

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/pleximus_hackathon.git
cd pleximus_hackathon
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the API key

```bash
# Copy the template
cp .env.example .env
```

Open `.env` and replace `your_api_key_here` with your Gemini API key:

```text
GEMINI_API_KEY=your_actual_key_here
```

> **Get a free key**: https://aistudio.google.com/app/apikey

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | Your Google AI Studio Gemini API key |

⚠️ **Never commit your `.env` file.** It is listed in `.gitignore`.

---

## How to Run

```bash
python main.py
```

Type `help` for example queries. Type `exit` to quit.

---

## Example Queries

```
You: What is 25 * 18?
Agent: 25 × 18 = 450.

You: Calculate (100 + 50) / 5
Agent: (100 + 50) / 5 = 30.

You: What's the weather in Mumbai?
Agent: Current weather in Mumbai, India:
       Temperature: 29°C | Wind: 12 km/h | Condition: Partly cloudy

You: Count the words in: Artificial intelligence is powerful
Agent: Word count: 4

You: Reverse this text: hello world
Agent: Reversed: dlrow olleh

You: Convert 5 km to meters
Agent: 5 km = 5000 meters

You: Convert 72 Fahrenheit to Celsius
Agent: 72°F = 22.2222°C

You: Convert 10 kg to pounds
Agent: 10 kg = 22.0462 pounds
```

---

## Edge Cases Handled

| Scenario | Behaviour |
|---|---|
| Division by zero | "Cannot divide by zero." |
| Invalid math expression | "Invalid mathematical expression." |
| Unknown city | "City not found: 'XYZ'. Please check the spelling." |
| Network failure | Friendly error, no crash |
| Unsupported unit | "Unsupported unit..." with category hint |
| Cross-category conversion | "Cannot convert 'kg' to 'meters'..." |
| Empty user input | Silently re-prompts |
| Gemini API error | Error message displayed, loop continues |

---

## Future Scope

- [ ] Add currency converter (live exchange rates via Frankfurter API)
- [ ] Add Wikipedia summary lookup
- [ ] Add Date/Time & Timezone tool
- [ ] Add voice input/output
- [ ] Add a web UI (FastAPI + simple front-end)
- [ ] Persistent conversation history (SQLite or JSON log)
- [ ] Support for multi-step chained tool calls

---

## License

MIT — Built for the Pleximus Inc. AI Hackathon at FAMT Ratnagiri.
