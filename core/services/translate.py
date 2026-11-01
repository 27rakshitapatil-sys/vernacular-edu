from .llm import ask
from ..languages import LANGUAGES


def translate(text, target, source="en"):
    name = LANGUAGES[target][0]

    prompt = (
        f"Translate the text below into {name}. "
        f"Use simple words that a primary-school child would know. "
        f"Reply with ONLY the translation, written in {name} script. "
        f"No explanation, no pronunciation, no English, no quotation marks, "
        f"no bold or other formatting.\n\n"
        f"Text: {text}"
    )

    reply = ask(prompt)

    # No key set: mock mode, so the app still runs
    if reply is None:
        return f"[MOCK {target}] {text}"

    return reply.strip()



def translate_many(texts, target):
    """Translate a list of texts in ONE call to Gemini (much faster than one by one)."""
    import json

    name = LANGUAGES[target][0]
    prompt = (
        f"Translate each text in the JSON list below into {name}. "
        f"Use simple words that a primary-school child would know. "
        f"Reply with ONLY a JSON list of strings, in the same order and with the same "
        f"number of items, written in {name} script. "
        f"No explanation, no pronunciation, no markdown.\n\n"
        f"{json.dumps(texts, ensure_ascii=False)}"
    )

    reply = ask(prompt)

    # No key set: mock mode
    if reply is None:
        return [f"[MOCK {target}] {t}" for t in texts]

    reply = reply.strip()
    if reply.startswith("```"):          # remove code fences if Gemini added them
        reply = reply.strip("`")
        if reply.lower().startswith("json"):
            reply = reply[4:]

    try:
        result = json.loads(reply)
        if isinstance(result, list) and len(result) == len(texts):
            return [str(item) for item in result]
    except json.JSONDecodeError:
        pass

    # If the reply was not usable, fall back to translating one by one
    return [translate(t, target) for t in texts]