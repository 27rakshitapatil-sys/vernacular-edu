from django.shortcuts import render
from .languages import LANGUAGES
from .services.translate import translate_many
from .services.pedagogy import generate


def index(request):
    context = {"languages": LANGUAGES}

    if request.method == "POST":
        text = request.POST["text"]
        lang = request.POST["language"]
        grade = int(request.POST.get("grade", 2))

        lesson = generate(text, grade)

        # Translate everything in ONE call: [lesson, question 1-3, story]
        pieces = [lesson["simplified"]] + lesson["questions"] + [lesson["story"]]
        done = translate_many(pieces, lang)

        context["result"] = {
            "simplified": done[0],
            "questions": done[1:-1],
            "story": done[-1],
            "speech_lang": LANGUAGES[lang][1],
        }

    return render(request, "core/index.html", context)