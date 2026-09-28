from django.db import models
from django.conf import settings


class Skill(models.Model):
    name = models.CharField(
        max_length=50, unique=True
    )  # 예: 'Python', 'Vue.js', 'Django'

    def __str__(self):
        return self.name


class JobPost(models.Model):
    company_name = models.CharField(max_length=100)  # 기업명
    title = models.CharField(max_length=200)  # 공고 제목
    description = models.TextField()  # 직무 설명
    company_size = models.CharField(max_length=20, default="무관")  # 기업 규모
    required_skills = models.ManyToManyField(
        Skill, related_name="jobs"
    )  # 요구 기술 스택

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company_name", "title"], name="unique_job_company_title"
            )
        ]
