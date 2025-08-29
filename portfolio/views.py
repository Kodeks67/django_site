from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, FormView, UpdateView

from .forms import ContactForm, ProjectForm
from .models import ContactMessage, Project, Tag


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


class ContactView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def dispatch(self, request, *args, **kwargs):
        ip = self.get_ip()
        key = f"contact_rate_{ip}"
        last = cache.get(key)
        if last and (timezone.now() - last).total_seconds() < 30:
            messages.error(request, "Слишком часто. Попробуйте через несколько секунд.")
            return super().get(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        ip = self.get_ip()
        msg = ContactMessage.objects.create(
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            subject=form.cleaned_data.get("subject", ""),
            message=form.cleaned_data["message"],
            client_ip=ip,
            user_agent=self.request.META.get("HTTP_USER_AGENT", "")[:500],
        )
        subject = form.cleaned_data.get("subject") or "Сообщение с портфолио"
        body = (
            f"От: {msg.name} <{msg.email}>\n"
            f"IP: {msg.client_ip}\nUA: {msg.user_agent}\n\n"
            f"{msg.message}"
        )
        send_mail(
            subject,
            body,
            getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
            [getattr(settings, "CONTACT_RECEIVER_EMAIL", "owner@example.com")],
        )
        cache.set(f"contact_rate_{ip}", timezone.now(), 60)
        messages.success(self.request, "Спасибо! Сообщение отправлено ✅")
        return super().form_valid(form)

    def get_ip(self):
        xff = self.request.META.get("HTTP_X_FORWARDED_FOR")
        return (
            xff.split(",")[0].strip()
            if xff
            else self.request.META.get("REMOTE_ADDR", "0.0.0.0")
        )


def healthz(_request):
    return HttpResponse("ok", content_type="text/plain")
