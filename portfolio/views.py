from django.shortcuts import get_object_or_404, render

from .models import Project


def index(request):
    projects = Project.objects.order_by("-created_at")[:5]
    return render(request, "index.html", {"projects": projects})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "project_detail.html", {"project": project})
