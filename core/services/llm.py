import os
import time
import requests

# Tried in order. If one is overloaded, the next one is used automatically.
FALLBACK_MODELS = ["gemini-3.7-flash", "gemini-3.5-flash", "gemini-3.1-flash-lite"]


def _call(model, key, prompt, timeout):
    """Try one model up to 2 times. Returns text, or None if it is busy."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"thinkingConfig": {"thinkingLevel": "low"}},
    }

    for attempt in range(2):
        start = time.time()
        try:
            resp = requests.post(url, headers={"x-goog-api-key": key},
                                 json=body, timeout=timeout)
        except requests.exceptions.Timeout:
            print(f"[gemini:{model}] timeout after {time.time() - start:.0f}s")
            continue

        print(f"[gemini:{model}] status {resp.status_code} in {time.time() - start:.1f}s")

        if resp.status_code == 400 and "generationConfig" in body:
            body.pop("generationConfig")   # model rejected the setting, retry without it
            continue

        if resp.status_code in (429, 500, 503):
            time.sleep(2)
            continue

        resp.raise_for_status()
        parts = resp.json()["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts if not p.get("thought"))

    return None   # this model is busy, caller will try the next one


def ask(prompt, timeout=30):
    """Send a prompt to Gemini and return the text reply (None if no key is set)."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return None

    models = list(FALLBACK_MODELS)
    preferred = os.environ.get("GEMINI_MODEL")
    if preferred:
        models.insert(0, preferred)

    for model in models:
        text = _call(model, key, prompt, timeout)
        if text is not None:
            return text
        print(f"[gemini] {model} is busy, trying next model")

    raise RuntimeError("Gemini is busy right now. Please try again in a minute.")