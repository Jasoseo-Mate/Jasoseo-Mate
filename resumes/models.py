from django.conf import settings
from django.db import models

from jobs.models import JobPost  # Import JobPost model


class Experience(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="experiences"
    )
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


class Resume(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes"
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)  # For storing structured resume data or text
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Resume: {self.title}"


class CoverLetter(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cover_letters"
    )
    job_post = models.ForeignKey(
        JobPost,
        on_delete=models.SET_NULL,
        related_name="cover_letters",
        null=True,
        blank=True,
    )
    target_company = models.CharField(max_length=100, blank=True)
    target_role = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        target = self.target_role or (self.job_post.title if self.job_post else "지원 대상 미지정")
        return f"{self.user.username}'s Cover Letter for {target}"
