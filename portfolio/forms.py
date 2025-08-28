from urllib.parse import urlparse

from django import forms
from django.core.exceptions import ValidationError

from .models import Project, Tag

BASE_INPUT_CLS = "w-full border rounded px-3 py-2"


class ProjectForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        help_text="Теги через запятую (например: Python, Django)",
        label="Теги",
        widget=forms.TextInput(attrs={"class": BASE_INPUT_CLS}),
    )

    repo_url = forms.URLField(
        label="Ссылка на репозиторий",
        required=False,
        assume_scheme="https",
        widget=forms.URLInput(attrs={"class": BASE_INPUT_CLS}),
    )
    demo_url = forms.URLField(
        label="Ссылка на демо",
        required=False,
        assume_scheme="https",
        widget=forms.URLInput(attrs={"class": BASE_INPUT_CLS}),
    )

    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "cover",
            "repo_url",
            "demo_url",
            "tags_input",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": BASE_INPUT_CLS}),
            "description": forms.Textarea(attrs={"rows": 6, "class": BASE_INPUT_CLS}),
            "tech_stack": forms.TextInput(attrs={"class": BASE_INPUT_CLS}),
            "cover": forms.ClearableFileInput(attrs={"class": BASE_INPUT_CLS}),
        }

    def clean_repo_url(self):
        return self._normalize_url(self.cleaned_data.get("repo_url"))

    def clean_demo_url(self):
        return self._normalize_url(self.cleaned_data.get("demo_url"))

    @staticmethod
    def _normalize_url(value: str | None) -> str | None:
        if not value:
            return value
        parsed = urlparse(value)
        if not parsed.scheme:
            value = "https://" + value
        return value

    def save(self, commit=True):
        instance: Project = super().save(commit=commit)
        raw = self.cleaned_data.get("tags_input", "")
        tags = []
        for chunk in [s.strip() for s in raw.split(",") if s.strip()]:
            tag, _ = Tag.objects.get_or_create(name=chunk)
            tags.append(tag)
        if tags:
            instance.tags.set(tags, clear=False)
        return instance


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=120,
        widget=forms.TextInput(attrs={"class": "w-full border rounded px-3 py-2"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "w-full border rounded px-3 py-2"}),
    )
    subject = forms.CharField(
        label="Тема",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"class": "w-full border rounded px-3 py-2"}),
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(
            attrs={"class": "w-full border rounded px-3 py-2", "rows": 6}
        ),
    )
    # honeypot — скрытое поле (боты часто заполняют)
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise ValidationError("Спам обнаружен.")
        return ""
