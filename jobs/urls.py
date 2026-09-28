# jobs/urls.py

from django.urls import path

from . import views

app_name = "jobs"

urlpatterns = [
    # 기존에 있던 것들
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("recommended/", views.recommended_jobs, name="recommended_jobs"),
    # 💡 새로 추가된 메뉴 이동용 URL (여기에 등록된 name을 HTML에서 {% url 'name' %}으로 부릅니다)
    path("company/", views.company_analysis, name="company_analysis"),
    path("company/analyze/", views.ai_analyze_company, name="ai_analyze_company"),
    path("myspec/", views.my_spec, name="my_spec"),
    # 🌟 AI 기반 매칭 및 자소서 서비스 URL 추가
    path("ai-matching/", views.ai_matching, name="ai_matching"),
    path("ai-matching/analyze/", views.ai_analyze_spec, name="ai_analyze_spec"),
    path(
        "ai-matching/generate-coverletter/",
        views.ai_generate_coverletter,
        name="ai_generate_coverletter",
    ),
    path(
        "ai-matching/save-coverletter/",
        views.ai_save_coverletter,
        name="ai_save_coverletter",
    ),
]
