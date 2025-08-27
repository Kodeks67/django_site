from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView

from .forms import ProjectForm
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


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects_add.html"

    def form_valid(self, form):
        resp = super().form_valid(form)
        messages.success(self.request, "Проект добавлен ✅")
        return resp

    def get_success_url(self):
        return reverse("project_detail", kwargs={"slug": self.object.slug})
