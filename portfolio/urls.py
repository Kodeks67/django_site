from django.urls import path

from . import views
from .feeds import ProjectsFeed

urlpatterns = [
    # Главная
    path("", views.index, name="home"),
    # Проекты
    path("projects/", views.projects_list, name="projects_list"),
    path("projects/add/", views.ProjectCreateView.as_view(), name="project_add"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path(
        "projects/<slug:slug>/edit/",
        views.ProjectUpdateView.as_view(),
        name="project_edit",
    ),
    path(
        "projects/<slug:slug>/delete/",
        views.ProjectDeleteView.as_view(),
        name="project_delete",
    ),
    # Контакты
    path("contact/", views.ContactView.as_view(), name="contact"),
    # RSS
    path("rss/projects/", ProjectsFeed(), name="projects_rss"),
]
