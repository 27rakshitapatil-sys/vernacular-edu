import json
import re

from .llm import ask

PROMPT = """You are a primary-school teacher. Grade level: {grade}.
Lesson text: {text}

Return ONLY valid JSON with these keys:
"simplified": the lesson rewritten in very simple short sentences,
"questions": a list of 3 short questions to check understanding,
"story": a 4-5 sentence simple story that teaches the same idea."""

MOCK = {
    "simplified": None,  # filled with the original text in mock mode
    "questions": ["Question 1?", "Question 2?", "Question 3?"],
    "story": "This is a mock story.",
}


def _parse_json(raw):
    """Parse model output as JSON, tolerating ```json fences and extra text."""
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.I)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.S)
        if match:
            return json.loads(match.group(0))
        raise


def generate(text, grade=2):
    raw = ask(PROMPT.format(grade=grade, text=text))

    # No GEMINI_API_KEY set: mock mode so the app still runs
    if raw is None:
        return {**MOCK, "simplified": text}

    data = _parse_json(raw)
    return {
        "simplified": data.get("simplified", text),
        "questions": data.get("questions", [])[:3],
        "story": data.get("story", ""),
    }

def generate_translated(text, target, grade=2):
    """Simplify a lesson, then translate everything into the target language."""
    from .translate import translate_many

    data = generate(text, grade)
    questions = data["questions"]

    # One call: [simplified, q1, q2, q3, story]
    parts = [data["simplified"], *questions, data["story"]]
    translated = translate_many(parts, target)

    return {
        "simplified": translated[0],
        "questions": translated[1:1 + len(questions)],
        "story": translated[-1],
    }