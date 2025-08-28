from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def unique_slugify(instance, value: str, slug_field_name: str = "slug"):
    """
    Генерирует уникальный slug на основе value.
    Если существует, добавляет -2, -3, ... пока не найдёт свободный.
    """
    slug = slugify(value)
    Model = instance.__class__
    unique_slug = slug
    n = 2
    while (
        Model.objects.filter(**{slug_field_name: unique_slug})
        .exclude(pk=instance.pk)
        .exists()
    ):
        unique_slug = f"{slug}-{n}"
        n += 1
    return unique_slug


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        from django.utils.text import slugify

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    tech_stack = models.CharField(max_length=200, blank=True)
    cover = models.ImageField(upload_to="projects/covers/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
        blank=True,  # временно, чтобы миграция прошла
    )

    repo_url = models.URLField("Ссылка на репозиторий", blank=True)
    demo_url = models.URLField("Ссылка на демо", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


def get_absolute_url(self):
    return reverse("project_detail", kwargs={"slug": self.slug})


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    client_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.subject or self.message[:30]}"
