from django.contrib import admin
from django.urls import path
from core.views import index, history

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("history/", history),
]