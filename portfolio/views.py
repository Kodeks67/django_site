from django.shortcuts import get_object_or_404, render

from .models import Project, Tag


def index(request):
    projects = Project.objects.order_by("-created_at")[:3]
    return render(request, "index.html", {"projects": projects})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "project_detail.html", {"project": project})


def projects_list(request):
    from django.core.paginator import Paginator

    qs = Project.objects.order_by("-created_at").select_related()
    tag_slug = request.GET.get("tag")
    active_tag = None
    if tag_slug:
        qs = qs.filter(tags__slug=tag_slug).distinct()
        active_tag = Tag.objects.filter(slug=tag_slug).first()

    paginator = Paginator(qs, 9)
    page = request.GET.get("page")
    projects = paginator.get_page(page)
    return render(
        request, "projects_list.html", {"projects": projects, "active_tag": active_tag}
    )
