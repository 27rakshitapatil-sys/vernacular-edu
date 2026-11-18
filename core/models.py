from django.db import models


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=10)
    grade = models.CharField(max_length=20)
    original_text = models.TextField()
    simplified_text = models.TextField()
    questions = models.TextField()
    story = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.language}, grade {self.grade})"