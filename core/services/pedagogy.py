import os
import json

PROMPT = """You are a primary-school teacher. Grade level: {grade}.
Lesson text: {text}

Return ONLY valid JSON with these keys:
"simplified": the lesson rewritten in very simple short sentences,
"questions": a list of 3 short questions to check understanding,
"story": a 4-5 sentence simple story that teaches the same idea."""


def generate(text, grade=2):
    # Mock mode: runs without an API key so we can test the app first
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return {
            "simplified": text,
            "questions": ["Question 1?", "Question 2?", "Question 3?"],
            "story": "This is a mock story.",
        }

    import anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": PROMPT.format(grade=grade, text=text)}],
    )
    return json.loads(msg.content[0].text)