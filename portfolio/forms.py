from urllib.parse import urlparse

from django import forms

from .models import Project, Tag

BASE_INPUT_CLS = "w-full border rounded px-3 py-2"


class ProjectForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        help_text="Теги через запятую (например: Python, Django)",
        label="Теги",
        widget=forms.TextInput(attrs={"class": BASE_INPUT_CLS}),
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
            "repo_url": forms.URLInput(attrs={"class": BASE_INPUT_CLS}),
            "demo_url": forms.URLInput(attrs={"class": BASE_INPUT_CLS}),
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
