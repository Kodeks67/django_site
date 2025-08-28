from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html

from .models import ContactMessage, Project, Tag


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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "created_at",
        "processed_display",
        "toggle_link",
    )
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at", "client_ip", "user_agent")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    @admin.display(boolean=True, description="Обработано")
    def processed_display(self, obj: ContactMessage):
        return obj.is_processed

    @admin.display(description="Действие")
    def toggle_link(self, obj: ContactMessage):
        url = reverse("admin:portfolio_contactmessage_toggle", args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" '
            'style="padding:2px 8px;border:1px solid '
            '#ddd;border-radius:6px;">Переключить</a>',
            url,
        )

    def get_urls(self):
        return [
            path(
                "<int:pk>/toggle-processed/",
                self.admin_site.admin_view(self.toggle_processed),
                name="portfolio_contactmessage_toggle",
            ),
        ] + super().get_urls()

    def toggle_processed(self, request, pk: int):
        obj = self.get_object(request, pk)
        if obj is not None:
            obj.is_processed = not obj.is_processed
            obj.save(update_fields=["is_processed"])
            self.message_user(
                request,
                f"Заявка «{obj}» помечена как "
                f"{'обработана' if obj.is_processed else 'не обработана'}.",
            )

        referer = request.META.get("HTTP_REFERER")
        return redirect(referer or reverse("admin:portfolio_contactmessage_changelist"))
