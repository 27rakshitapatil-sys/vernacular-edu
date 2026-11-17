# Mother Tongue Lesson Helper

An AI-powered tool for mother tongue-based primary education. A teacher pastes a lesson in English, and the app:

1. **Simplifies** it into short, easy sentences for the chosen grade
2. **Creates 3 questions** to check understanding
3. **Writes a short story** that teaches the same idea
4. **Translates everything** into the child's mother tongue
5. **Reads it aloud** in that language

## Supported languages

Kannada, Hindi, Marathi, Tamil, Telugu

## Tech stack

- Python, Django
- Google Gemini API (simplification and translation)
- Browser speech synthesis (read aloud)

## How it works

- `core/services/pedagogy.py` builds the simplified lesson, questions and story
- `core/services/translate.py` translates all parts in a single call
- `core/services/llm.py` talks to Gemini, retries when the server is busy, and automatically falls back to other models
- Without an API key, the app runs in mock mode so you can test the pages

## Run it locally

```
git clone <your-repo-url>
cd vernacular-edu
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
$env:GEMINI_API_KEY="your-key-here"
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Notes

- Read aloud needs a voice for the chosen language installed in your browser or operating system.
- Never commit your API key. Set it as an environment variable.

## Author

Rakshita Patil