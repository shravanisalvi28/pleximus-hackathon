"""
app.py — Flask web interface for the Pleximus AI Tool Agent.
Serves a chat UI and streams agent responses via SSE.
"""

import os
import sys
import io
import threading
import queue
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from agent import PleximusAgent

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ── Single shared agent (fine for demo/single-user hackathon) ──────────────
_agent = None
_agent_lock = threading.Lock()


def get_agent():
    global _agent
    if _agent is None:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key or api_key == "your_api_key_here":
            return None
        _agent = PleximusAgent(api_key=api_key)
    return _agent


# ── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Accept a JSON body: { "message": "..." }
    Return a JSON response: { "reply": "...", "tool_calls": [...] }
    """
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Empty message."}), 400

    agent = get_agent()
    if agent is None:
        return jsonify({
            "error": "GEMINI_API_KEY is not configured. "
                     "Add it to your .env file and restart the server."
        }), 500

    # Capture tool-call prints from tool wrappers in agent.py
    captured_output = []
    original_stdout = sys.stdout

    class CapturingStream(io.StringIO):
        def write(self, text):
            captured_output.append(text)
            original_stdout.write(text)  # still show in terminal

    capturing = CapturingStream()
    sys.stdout = capturing

    try:
        with _agent_lock:
            reply = agent.ask(user_message)
    except Exception as e:
        sys.stdout = original_stdout
        return jsonify({"error": f"Agent error: {e}"}), 500
    finally:
        sys.stdout = original_stdout

    # Parse tool calls from captured output
    tool_calls = []
    for line in "".join(captured_output).splitlines():
        line = line.strip()
        if line.startswith("[Tool:"):
            tool_calls.append(line)
        elif line.startswith("[Tool Result]"):
            tool_calls.append(line)

    return jsonify({"reply": reply, "tool_calls": tool_calls})


@app.route("/reset", methods=["POST"])
def reset():
    """Reset the agent conversation."""
    global _agent
    agent = get_agent()
    if agent:
        agent.reset()
    return jsonify({"status": "ok"})


@app.route("/health")
def health():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    configured = bool(api_key and api_key != "your_api_key_here")
    return jsonify({"status": "ok", "api_configured": configured})


if __name__ == "__main__":
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_api_key_here":
        print("\n⚠️  WARNING: GEMINI_API_KEY is not set in .env")
        print("   The UI will load but queries will fail.\n")
    else:
        print("\n✅ Gemini API key loaded.")

    print("🚀 Starting Pleximus AI Web Interface...")
    print("   Open http://127.0.0.1:5000 in your browser\n")
    app.run(debug=False, host="127.0.0.1", port=5000)
