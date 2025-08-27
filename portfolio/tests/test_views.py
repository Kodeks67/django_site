import pytest
from django.urls import reverse

from .factories import ProjectFactory, TagFactory


@pytest.mark.django_db
def test_projects_list_status_code(client):
    url = reverse("projects_list")
    resp = client.get(url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_projects_list_shows_projects(client):
    p = ProjectFactory(title="Visible Project")
    resp = client.get(reverse("projects_list"))
    assert resp.status_code == 200
    assert p.title in resp.content.decode()


@pytest.mark.django_db
def test_projects_list_filter_by_tag(client):
    t_python = TagFactory(name="Python")
    t_fastapi = TagFactory(name="FastAPI")
    p1 = ProjectFactory(title="PyProj")
    p2 = ProjectFactory(title="FaProj")
    p1.tags.add(t_python)
    p2.tags.add(t_fastapi)

    resp = client.get(reverse("projects_list"), {"tag": t_python.slug})
    html = resp.content.decode()
    assert "PyProj" in html
    assert "FaProj" not in html


@pytest.mark.django_db
def test_project_detail(client):
    p = ProjectFactory(title="Detail Me")
    url = reverse("project_detail", kwargs={"slug": p.slug})
    resp = client.get(url)
    assert resp.status_code == 200
    assert "Detail Me" in resp.content.decode()


@pytest.mark.django_db
def test_index_shows_latest_three(client):
    # создаём 4 проекта, ожидаем увидеть только 3 последних
    for _ in range(4):
        ProjectFactory()
    resp = client.get(reverse("home"))
    assert resp.status_code == 200
    # просто проверим, что на странице упоминаются ровно 3 карточки по слову 'Открыть'
    assert resp.content.decode().count("Открыть") == 3
