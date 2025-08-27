import factory
from django.utils.text import slugify

from portfolio.models import Project, Tag


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f"Tag {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    title = factory.Sequence(lambda n: f"Project {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.title))
    description = "Demo description"
    tech_stack = "Python, Django"
    repo_url = "https://github.com/example/repo"
    demo_url = "https://example.com"
