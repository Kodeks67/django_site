import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from .factories import ProjectFactory


@pytest.mark.django_db
def test_only_owner_can_edit_denied_for_other_user(client):
    owner = User.objects.create_user("owner", password="x")
    other = User.objects.create_user("other", password="x")
    p = ProjectFactory(owner=owner)

    assert client.login(username=other.username, password="x")
    resp = client.get(reverse("project_edit", kwargs={"slug": p.slug}))
    assert resp.status_code in (302, 403)


@pytest.mark.django_db
def test_owner_can_edit_allowed(client):
    owner = User.objects.create_user("owner2", password="x")
    p = ProjectFactory(owner=owner)

    assert client.login(username="owner2", password="x")
    resp = client.get(reverse("project_edit", kwargs={"slug": p.slug}))
    assert resp.status_code == 200
