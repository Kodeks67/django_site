from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

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
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        form.save_m2m()
        messages.success(self.request, "Проект добавлен ✅")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project_detail", kwargs={"slug": self.object.slug})


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        u = self.request.user
        return u.is_authenticated and (u.is_staff or obj.owner_id == u.id)

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав на это действие.")
        return super().handle_no_permission()


class ProjectUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects_edit.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        messages.success(self.request, "Проект обновлён ✅")
        return reverse("project_detail", kwargs={"slug": self.object.slug})


class ProjectDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Project
    template_name = "projects_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("projects_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Проект удалён 🗑️")
        return super().delete(request, *args, **kwargs)
