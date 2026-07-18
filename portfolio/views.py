from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
    Profile, Skill, Project, Experience, Education, BlogPost, ContactMessage
)
from .forms import (
    ContactForm, ProfileForm, SkillForm, ProjectForm,
    ExperienceForm, EducationForm, BlogPostForm
)


# ---------------------------------------------------------------------------
# PUBLIC SITE
# ---------------------------------------------------------------------------

def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your message has been sent.")
            return redirect("home")
    else:
        form = ContactForm()

    context = {
        "profile": Profile.load(),
        "skills": Skill.objects.all(),
        "projects": Project.objects.filter(featured=True) or Project.objects.all()[:6],
        "experiences": Experience.objects.all(),
        "educations": Education.objects.all(),
        "posts": BlogPost.objects.filter(is_published=True)[:3],
        "form": form,
    }
    return render(request, "portfolio/home.html", context)


def project_list(request):
    context = {
        "profile": Profile.load(),
        "projects": Project.objects.all(),
    }
    return render(request, "portfolio/project_list.html", context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {
        "profile": Profile.load(),
        "project": project,
    }
    return render(request, "portfolio/project_detail.html", context)


def blog_list(request):
    context = {
        "profile": Profile.load(),
        "posts": BlogPost.objects.filter(is_published=True),
    }
    return render(request, "portfolio/blog_list.html", context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:4]
    context = {
        "profile": Profile.load(),
        "post": post,
        "recent_posts": recent_posts,
    }
    return render(request, "portfolio/blog_detail.html", context)


def about(request):
    context = {
        "profile": Profile.load(),
        "experiences": Experience.objects.all(),
        "educations": Education.objects.all(),
        "skills": Skill.objects.all(),
    }
    return render(request, "portfolio/about.html", context)


def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your message has been sent.")
            return redirect("contact")
    else:
        form = ContactForm()

    context = {
        "profile": Profile.load(),
        "form": form,
    }
    return render(request, "portfolio/contact.html", context)


# ---------------------------------------------------------------------------
# CUSTOM ADMIN PANEL AUTH
# ---------------------------------------------------------------------------

def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if user.is_staff:
            login(request, user)
            return redirect("dashboard_home")
        form.add_error(None, "You do not have permission to access the admin panel.")
    return render(request, "dashboard/login.html", {"form": form})


@login_required(login_url="dashboard_login")
def dashboard_logout(request):
    logout(request)
    return redirect("dashboard_login")


@login_required(login_url="dashboard_login")
def dashboard_home(request):
    context = {
        "skills_count": Skill.objects.count(),
        "projects_count": Project.objects.count(),
        "experience_count": Experience.objects.count(),
        "education_count": Education.objects.count(),
        "posts_count": BlogPost.objects.count(),
        "unread_messages": ContactMessage.objects.filter(is_read=False).count(),
        "recent_messages": ContactMessage.objects.all()[:5],
    }
    return render(request, "dashboard/home.html", context)


@login_required(login_url="dashboard_login")
def dashboard_profile(request):
    profile = Profile.load()
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("dashboard_profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "dashboard/profile_form.html", {"form": form})


@login_required(login_url="dashboard_login")
def dashboard_messages(request):
    msgs = ContactMessage.objects.all()
    return render(request, "dashboard/messages_list.html", {"messages_list": msgs})


@login_required(login_url="dashboard_login")
def dashboard_message_mark_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = True
    msg.save()
    return redirect("dashboard_messages")


@login_required(login_url="dashboard_login")
def dashboard_message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == "POST":
        msg.delete()
        messages.success(request, "Message deleted.")
        return redirect("dashboard_messages")
    return render(request, "dashboard/confirm_delete.html", {"object": msg, "type_name": "message"})


# ---------------------------------------------------------------------------
# GENERIC CRUD MIXIN-BASED VIEWS FOR: Skill, Project, Experience, Education, BlogPost
# ---------------------------------------------------------------------------

class DashboardLoginRequired(LoginRequiredMixin):
    login_url = reverse_lazy("dashboard_login")


def make_crud_views(model_cls, form_cls, list_template, form_template, delete_template,
                     list_url_name, success_url_name, extra_context=None):
    """Factory that builds List/Create/Update/Delete class-based views for a model,
    all sharing the same dashboard look-and-feel."""

    class _List(DashboardLoginRequired, ListView):
        model = model_cls
        template_name = list_template
        context_object_name = "object_list"

        def get_queryset(self):
            return model_cls.objects.all()

    class _Create(DashboardLoginRequired, CreateView):
        model = model_cls
        form_class = form_cls
        template_name = form_template
        success_url = reverse_lazy(success_url_name)

        def form_valid(self, form):
            messages.success(self.request, f"{model_cls.__name__} added.")
            return super().form_valid(form)

    class _Update(DashboardLoginRequired, UpdateView):
        model = model_cls
        form_class = form_cls
        template_name = form_template
        success_url = reverse_lazy(success_url_name)

        def form_valid(self, form):
            messages.success(self.request, f"{model_cls.__name__} updated.")
            return super().form_valid(form)

    class _Delete(DashboardLoginRequired, DeleteView):
        model = model_cls
        template_name = delete_template
        success_url = reverse_lazy(success_url_name)

        def form_valid(self, form):
            messages.success(self.request, f"{model_cls.__name__} deleted.")
            return super().form_valid(form)

    return _List, _Create, _Update, _Delete


SkillListView, SkillCreateView, SkillUpdateView, SkillDeleteView = make_crud_views(
    Skill, SkillForm, "dashboard/skill_list.html", "dashboard/skill_form.html",
    "dashboard/confirm_delete.html", "dashboard_skills", "dashboard_skills"
)

ProjectListView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView = make_crud_views(
    Project, ProjectForm, "dashboard/project_list.html", "dashboard/project_form.html",
    "dashboard/confirm_delete.html", "dashboard_projects", "dashboard_projects"
)

ExperienceListView, ExperienceCreateView, ExperienceUpdateView, ExperienceDeleteView = make_crud_views(
    Experience, ExperienceForm, "dashboard/experience_list.html", "dashboard/experience_form.html",
    "dashboard/confirm_delete.html", "dashboard_experience", "dashboard_experience"
)

EducationListView, EducationCreateView, EducationUpdateView, EducationDeleteView = make_crud_views(
    Education, EducationForm, "dashboard/education_list.html", "dashboard/education_form.html",
    "dashboard/confirm_delete.html", "dashboard_education", "dashboard_education"
)

BlogPostListView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView = make_crud_views(
    BlogPost, BlogPostForm, "dashboard/blog_list_admin.html", "dashboard/blog_form.html",
    "dashboard/confirm_delete.html", "dashboard_blog", "dashboard_blog"
)
