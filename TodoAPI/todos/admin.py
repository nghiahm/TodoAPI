from django.contrib import admin
from .models import Todo


admin.site.register(Todo)


class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "completed", "created_at")
