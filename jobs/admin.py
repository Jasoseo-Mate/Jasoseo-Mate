# jobs/admin.py
from django.contrib import admin

from .models import JobPost, Skill

# 관리자 페이지에서 데이터를 관리할 수 있도록 모델 등록
admin.site.register(Skill)


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ("company_name", "title", "company_size", "source")
    list_filter = ("source", "company_size")
    search_fields = ("company_name", "title")
