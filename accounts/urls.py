from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.profile_dashboard, name="profile_dashboard"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("signup/", views.user_signup, name="signup"),
    path(
        "api/ai-recommend-skills/",
        views.ai_recommend_skills,
        name="ai_recommend_skills",
    ),
    # Education URLs
    path("education/", views.EducationListView.as_view(), name="education_list"),
    path("education/add/", views.EducationCreateView.as_view(), name="education_add"),
    path(
        "education/<int:pk>/edit/",
        views.EducationUpdateView.as_view(),
        name="education_edit",
    ),
    path(
        "education/<int:pk>/delete/",
        views.EducationDeleteView.as_view(),
        name="education_delete",
    ),
    # Certificate URLs
    path("certificate/", views.CertificateListView.as_view(), name="certificate_list"),
    path(
        "certificate/add/",
        views.CertificateCreateView.as_view(),
        name="certificate_add",
    ),
    path(
        "certificate/<int:pk>/edit/",
        views.CertificateUpdateView.as_view(),
        name="certificate_edit",
    ),
    path(
        "certificate/<int:pk>/delete/",
        views.CertificateDeleteView.as_view(),
        name="certificate_delete",
    ),
    # Activity URLs
    path("activity/", views.ActivityListView.as_view(), name="activity_list"),
    path("activity/add/", views.ActivityCreateView.as_view(), name="activity_add"),
    path(
        "activity/<int:pk>/edit/",
        views.ActivityUpdateView.as_view(),
        name="activity_edit",
    ),
    path(
        "activity/<int:pk>/delete/",
        views.ActivityDeleteView.as_view(),
        name="activity_delete",
    ),
    # Project URLs
    path("project/", views.ProjectListView.as_view(), name="project_list"),
    path("project/add/", views.ProjectCreateView.as_view(), name="project_add"),
    path("project/<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_edit"),
    path(
        "project/<int:pk>/delete/",
        views.ProjectDeleteView.as_view(),
        name="project_delete",
    ),
]
