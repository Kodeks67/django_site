from django.contrib import admin
from django.utils.html import format_html

from .models import Project, Tag


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at")
    search_fields = ("title",)
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}

    @admin.display(description="Cover")
    def thumb(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="height:48px;width:48px;object-fit:cover;'
                'border-radius:6px;" />',
                obj.cover.url,
            )
        return "—"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
