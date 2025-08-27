from django.contrib import admin
from django.utils.html import format_html

from .models import Project, Tag


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "thumb",
        "title",
        "slug",
        "tech_stack",
        "created_at",
        "repo_btn",
        "demo_btn",
    )
    search_fields = ("title", "tech_stack")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("preview", "created_at")

    fieldsets = (
        (
            "Основное",
            {"fields": ("title", "slug", "description", "tech_stack", "tags")},
        ),
        ("Медиа", {"fields": ("cover", "preview")}),
        ("Ссылки", {"fields": ("repo_url", "demo_url")}),
        ("Служебное", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    @admin.display(description="Preview")
    def preview(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="height:120px;border-radius:8px;object-'
                'fit:cover;" />',
                obj.cover.url,
            )
        return "—"

    @admin.display(description="Cover")
    def thumb(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;object-'
                'fit:cover;border-radius:6px;" />',
                obj.cover.url,
            )
        return "—"

    @admin.display(description="Repo")
    def repo_btn(self, obj):
        return (
            format_html(
                '<a href="{}" target="_blank" rel="noopener">Git</a>', obj.repo_url
            )
            if obj.repo_url
            else "—"
        )

    @admin.display(description="Demo")
    def demo_btn(self, obj):
        return (
            format_html(
                '<a href="{}" target="_blank" rel="noopener">Demo</a>', obj.demo_url
            )
            if obj.demo_url
            else "—"
        )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
