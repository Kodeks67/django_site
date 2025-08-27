import pytest
from django.utils.text import slugify

from portfolio.models import Project

from .factories import ProjectFactory, TagFactory


@pytest.mark.django_db
def test_project_str():
    p = ProjectFactory(title="My Title")
    assert str(p) == "My Title"


@pytest.mark.django_db
def test_project_slug_autofill_when_empty():
    p = Project(title="Привет мир", slug="")
    p.save()
    assert p.slug == slugify("Привет мир")


@pytest.mark.django_db
def test_project_tags_m2m():
    p = ProjectFactory()
    t1 = TagFactory(name="Python")
    t2 = TagFactory(name="Django")
    p.tags.add(t1, t2)
    assert p.tags.count() == 2
