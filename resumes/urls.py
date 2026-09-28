from django.urls import path

from . import views

app_name = "resumes"

urlpatterns = [
    path("experiences/", views.experience_list, name="experience_list"),
    path("experiences/create/", views.experience_create, name="experience_create"),
    path(
        "experiences/<int:pk>/update/",
        views.experience_update,
        name="experience_update",
    ),
    path(
        "experiences/<int:pk>/delete/",
        views.experience_delete,
        name="experience_delete",
    ),
    path("resumes/", views.resume_list, name="resume_list"),
    path("resumes/create/", views.resume_create, name="resume_create"),
    path("resumes/<int:pk>/update/", views.resume_update, name="resume_update"),
    path("resumes/<int:pk>/delete/", views.resume_delete, name="resume_delete"),
    path("coverletters/", views.coverletter_list, name="coverletter_list"),
    path(
        "coverletters/create/<int:job_post_pk>/",
        views.coverletter_create,
        name="coverletter_create",
    ),
    path(
        "coverletters/<int:pk>/update/",
        views.coverletter_update,
        name="coverletter_update",
    ),
    path(
        "coverletters/<int:pk>/delete/",
        views.coverletter_delete,
        name="coverletter_delete",
    ),
]
