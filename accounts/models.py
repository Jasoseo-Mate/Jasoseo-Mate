from django.conf import settings
from django.db import models

from jobs.models import Skill


class Profile(models.Model):
    """
    사용자의 기본 프로필 정보 (한 줄 소개 등)
    """

    COMPANY_SIZE_CHOICES = [
        ("대기업", "대기업"),
        ("중견기업", "중견기업"),
        ("중소기업", "중소기업"),
        ("스타트업", "스타트업"),
        ("무관", "무관"),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.CharField(max_length=255, blank=True, help_text="간단한 자기소개")
    skills = models.ManyToManyField(Skill, related_name="profiles", blank=True)
    preferred_company_size = models.CharField(
        max_length=20,
        choices=COMPANY_SIZE_CHOICES,
        default="무관",
        verbose_name="희망 기업 규모",
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Education(models.Model):
    """
    학력사항
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="educations"
    )
    school_name = models.CharField(max_length=100, verbose_name="학교명")
    major = models.CharField(max_length=100, verbose_name="전공")
    degree = models.CharField(max_length=50, verbose_name="학위 (예: 학사, 석사)")
    start_date = models.DateField(verbose_name="입학일")
    end_date = models.DateField(verbose_name="졸업일", null=True, blank=True)

    class Meta:
        verbose_name = "학력사항"
        verbose_name_plural = "학력사항"

    def __str__(self):
        return f"{self.school_name} - {self.major}"


class Certificate(models.Model):
    """
    자격증
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="certificates"
    )
    name = models.CharField(max_length=100, verbose_name="자격증명")
    issuer = models.CharField(max_length=100, verbose_name="발급기관")
    date_acquired = models.DateField(verbose_name="취득일")

    class Meta:
        verbose_name = "자격증"
        verbose_name_plural = "자격증"

    def __str__(self):
        return f"{self.name} ({self.issuer})"


class Activity(models.Model):
    """
    대내외활동
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="activities"
    )
    title = models.CharField(max_length=150, verbose_name="활동명")
    description = models.TextField(verbose_name="활동 내용", blank=True)
    start_date = models.DateField(verbose_name="시작일")
    end_date = models.DateField(verbose_name="종료일", null=True, blank=True)

    class Meta:
        verbose_name = "대내외활동"
        verbose_name_plural = "대내외활동"

    def __str__(self):
        return self.title


class Project(models.Model):
    """
    수행 프로젝트
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects"
    )
    title = models.CharField(max_length=150, verbose_name="프로젝트명")
    description = models.TextField(verbose_name="프로젝트 설명")
    start_date = models.DateField(verbose_name="시작일")
    end_date = models.DateField(verbose_name="종료일", null=True, blank=True)
    url = models.URLField(verbose_name="관련 링크", blank=True)

    class Meta:
        verbose_name = "프로젝트"
        verbose_name_plural = "프로젝트"

    def __str__(self):
        return self.title
