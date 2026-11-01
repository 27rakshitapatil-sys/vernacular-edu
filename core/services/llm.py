import os
import time
import requests


def ask(prompt, timeout=90):
    """Send a prompt to Gemini and return the text reply (None if no key is set)."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return None

    model = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"thinkingConfig": {"thinkingLevel": "low"}},
    }

    for attempt in range(3):
        start = time.time()
        try:
            resp = requests.post(url, headers={"x-goog-api-key": key},
                                 json=body, timeout=timeout)
        except requests.exceptions.Timeout:
            print(f"[gemini] timeout after {time.time() - start:.0f}s (attempt {attempt + 1})")
            continue

        print(f"[gemini] status {resp.status_code} in {time.time() - start:.1f}s")

        if resp.status_code == 400 and "generationConfig" in body:
            body.pop("generationConfig")   # model rejected the setting, retry without it
            continue

        resp.raise_for_status()
        parts = resp.json()["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts if not p.get("thought"))

    raise RuntimeError("Gemini did not respond. Please try again.")