from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "completed", "created_at")
