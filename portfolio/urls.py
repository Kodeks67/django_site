from django.urls import path

from . import views
from .feeds import ProjectsFeed

urlpatterns = [
    path("", views.index, name="home"),
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
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("rss/projects/", ProjectsFeed(), name="projects_rss"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
