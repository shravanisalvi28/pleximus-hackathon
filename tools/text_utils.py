"""
Text utility tool — local string manipulation operations.
No external API required. Handles: word count, character count,
reverse, uppercase, lowercase, remove extra spaces.
"""

import re


def process_text(operation: str, text: str) -> str:
    """
    Perform a text operation on the given input string.

    Args:
        operation: One of — "word_count", "char_count", "reverse",
                   "uppercase", "lowercase", "remove_spaces".
        text: The input text to process.

    Returns:
        The result as a human-readable string.
    """
    operation = operation.strip().lower()
    text = text.strip()

    if not text:
        return "No text provided to process."

    if operation == "word_count":
        words = text.split()
        count = len(words)
        return f"Word count: {count}"

    elif operation == "char_count":
        count = len(text)
        return f"Character count: {count}"

    elif operation == "reverse":
        return f"Reversed text: {text[::-1]}"

    elif operation == "uppercase":
        return f"Uppercase: {text.upper()}"

    elif operation == "lowercase":
        return f"Lowercase: {text.lower()}"

    elif operation == "remove_spaces":
        cleaned = re.sub(r"\s+", " ", text).strip()
        return f"Cleaned text: {cleaned}"

    else:
        supported = ", ".join([
            "word_count", "char_count", "reverse",
            "uppercase", "lowercase", "remove_spaces"
        ])
        return (
            f"Unsupported operation: '{operation}'.\n"
            f"Supported operations: {supported}"
        )
