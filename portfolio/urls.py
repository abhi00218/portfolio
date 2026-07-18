from django.urls import path
from . import views

urlpatterns = [
    # ---------------- Public site ----------------
    path("", views.home, name="home"),
    path("projects/", views.project_list, name="project_list"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact_page, name="contact"),

    # ---------------- Dashboard auth ----------------
    path("dashboard/login/", views.dashboard_login, name="dashboard_login"),
    path("dashboard/logout/", views.dashboard_logout, name="dashboard_logout"),
    path("dashboard/", views.dashboard_home, name="dashboard_home"),
    path("dashboard/profile/", views.dashboard_profile, name="dashboard_profile"),

    # ---------------- Messages ----------------
    path("dashboard/messages/", views.dashboard_messages, name="dashboard_messages"),
    path("dashboard/messages/<int:pk>/read/", views.dashboard_message_mark_read, name="dashboard_message_read"),
    path("dashboard/messages/<int:pk>/delete/", views.dashboard_message_delete, name="dashboard_message_delete"),

    # ---------------- Skills CRUD ----------------
    path("dashboard/skills/", views.SkillListView.as_view(), name="dashboard_skills"),
    path("dashboard/skills/add/", views.SkillCreateView.as_view(), name="dashboard_skill_add"),
    path("dashboard/skills/<int:pk>/edit/", views.SkillUpdateView.as_view(), name="dashboard_skill_edit"),
    path("dashboard/skills/<int:pk>/delete/", views.SkillDeleteView.as_view(), name="dashboard_skill_delete"),

    # ---------------- Projects CRUD ----------------
    path("dashboard/projects/", views.ProjectListView.as_view(), name="dashboard_projects"),
    path("dashboard/projects/add/", views.ProjectCreateView.as_view(), name="dashboard_project_add"),
    path("dashboard/projects/<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="dashboard_project_edit"),
    path("dashboard/projects/<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="dashboard_project_delete"),

    # ---------------- Experience CRUD ----------------
    path("dashboard/experience/", views.ExperienceListView.as_view(), name="dashboard_experience"),
    path("dashboard/experience/add/", views.ExperienceCreateView.as_view(), name="dashboard_experience_add"),
    path("dashboard/experience/<int:pk>/edit/", views.ExperienceUpdateView.as_view(), name="dashboard_experience_edit"),
    path("dashboard/experience/<int:pk>/delete/", views.ExperienceDeleteView.as_view(), name="dashboard_experience_delete"),

    # ---------------- Education CRUD ----------------
    path("dashboard/education/", views.EducationListView.as_view(), name="dashboard_education"),
    path("dashboard/education/add/", views.EducationCreateView.as_view(), name="dashboard_education_add"),
    path("dashboard/education/<int:pk>/edit/", views.EducationUpdateView.as_view(), name="dashboard_education_edit"),
    path("dashboard/education/<int:pk>/delete/", views.EducationDeleteView.as_view(), name="dashboard_education_delete"),

    # ---------------- Blog CRUD ----------------
    path("dashboard/blog/", views.BlogPostListView.as_view(), name="dashboard_blog"),
    path("dashboard/blog/add/", views.BlogPostCreateView.as_view(), name="dashboard_blog_add"),
    path("dashboard/blog/<int:pk>/edit/", views.BlogPostUpdateView.as_view(), name="dashboard_blog_edit"),
    path("dashboard/blog/<int:pk>/delete/", views.BlogPostDeleteView.as_view(), name="dashboard_blog_delete"),
]
