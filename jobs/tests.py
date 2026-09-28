import io
import json
import xml.etree.ElementTree as ET
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse

from resumes.models import CoverLetter

from .management.commands.fetch_worknet_jobs import (
    WORK24_JOB_DETAIL_API_URL,
    Command,
    normalize_company_size,
    skill_matches,
)
from .management.commands.seed_demo_data import SAMPLE_JOBS, SKILL_NAMES
from .models import JobPost, Skill


class JobViewSecurityTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user("user", password="test-password")

    @override_settings(GMSKEY="", AI_RATE_LIMIT=2, AI_RATE_LIMIT_WINDOW=60)
    def test_ai_endpoint_is_rate_limited_per_user(self):
        self.client.force_login(self.user)
        url = reverse("jobs:ai_analyze_company")

        self.assertEqual(self.client.post(url).status_code, 400)
        self.assertEqual(self.client.post(url).status_code, 400)
        response = self.client.post(url)

        self.assertEqual(response.status_code, 429)
        self.assertEqual(response["Retry-After"], "60")

    def test_company_analysis_page_requires_login(self):
        response = self.client.get(reverse("jobs:company_analysis"))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('jobs:company_analysis')}",
            fetch_redirect_response=False,
        )

    @override_settings(GMSKEY="test-key")
    @patch("jobs.views.requests.post", side_effect=RuntimeError("sensitive upstream URL"))
    @patch("jobs.views.fetch_real_news", return_value=[])
    def test_company_analysis_hides_internal_exception(self, mocked_news, mocked_post):
        self.client.force_login(self.user)
        with self.assertLogs("jobs.views", level="ERROR"):
            response = self.client.post(
                reverse("jobs:ai_analyze_company"),
                data=json.dumps({"company_name": "테스트 회사"}),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 500)
        self.assertNotIn("sensitive upstream URL", response.json()["message"])

    def test_ai_coverletter_does_not_create_fake_job(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("jobs:ai_save_coverletter"),
            data=json.dumps(
                {
                    "company_name": "테스트 회사",
                    "role": "백엔드 개발자",
                    "title": "지원서",
                    "content": "본문",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(JobPost.objects.count(), 0)
        coverletter = CoverLetter.objects.get()
        self.assertIsNone(coverletter.job_post)
        self.assertEqual(coverletter.target_company, "테스트 회사")

    def test_ai_coverletter_truncates_overlong_target(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("jobs:ai_save_coverletter"),
            data=json.dumps(
                {
                    "company_name": "회" * 101,
                    "role": "개발자",
                    "title": "지원서",
                    "content": "본문",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        coverletter = CoverLetter.objects.get()
        self.assertEqual(len(coverletter.target_company), 100)

    def test_work24_company_size_is_normalized(self):
        self.assertEqual(normalize_company_size("대기업"), "대기업")
        self.assertEqual(normalize_company_size("중견 기업"), "중견기업")
        self.assertEqual(normalize_company_size("벤처기업"), "스타트업")
        self.assertEqual(normalize_company_size("강소기업"), "중소기업")
        self.assertEqual(normalize_company_size(None), "무관")

    def test_skill_matching_uses_token_boundaries(self):
        self.assertTrue(skill_matches("Java 백엔드 개발", "Java"))
        self.assertTrue(skill_matches("UI/UX 디자이너", "UI/UX"))
        self.assertFalse(skill_matches("JavaScript 개발", "Java"))
        self.assertFalse(skill_matches("digital marketing guide", "Git"))

    def test_empty_work24_error_message_is_handled(self):
        root = ET.fromstring("<root><message /></root>")
        with self.assertRaisesMessage(CommandError, "알 수 없는 API 오류"):
            Command._raise_for_api_error(root)

    @patch("jobs.management.commands.fetch_worknet_jobs.requests.get")
    def test_work24_detail_size_is_loaded(self, mocked_get):
        mocked_get.return_value = Mock(
            text="<wantedDtl><corpInfo><busiSize>중견기업</busiSize></corpInfo></wantedDtl>"
        )
        result = Command()._fetch_company_size("api-key", "wanted-123")
        self.assertEqual(result, "중견기업")
        mocked_get.assert_called_once_with(
            WORK24_JOB_DETAIL_API_URL,
            params={
                "authKey": "api-key",
                "callTp": "D",
                "returnType": "XML",
                "wantedAuthNo": "wanted-123",
                "infoSvc": "VALIDATION",
            },
            timeout=10,
        )

    @override_settings(WORKNET_API_KEY="api-key")
    @patch("jobs.management.commands.fetch_worknet_jobs.requests.get")
    def test_existing_job_does_not_trigger_detail_request(self, mocked_get):
        JobPost.objects.create(
            company_name="기존 회사",
            title="기존 공고",
            description="이전 설명",
            company_size="무관",
        )
        mocked_get.return_value = Mock(text="""
                <wantedRoot><wanted>
                    <wantedAuthNo>wanted-123</wantedAuthNo>
                    <company>기존 회사</company><title>기존 공고</title>
                </wanted></wantedRoot>
            """)
        call_command("fetch_worknet_jobs", stdout=io.StringIO())
        self.assertEqual(mocked_get.call_count, 1)
        job = JobPost.objects.get(company_name="기존 회사", title="기존 공고")
        self.assertEqual(job.source, JobPost.Source.WORK24)


class DemoDataCommandTests(TestCase):
    def test_seed_is_idempotent_and_marks_sample_jobs(self):
        output = io.StringIO()

        call_command("seed_demo_data", stdout=output)
        first_job_count = JobPost.objects.count()
        first_skill_count = Skill.objects.count()
        call_command("seed_demo_data", stdout=output)

        self.assertEqual(first_job_count, len(SAMPLE_JOBS))
        self.assertEqual(first_skill_count, len(SKILL_NAMES))
        self.assertEqual(JobPost.objects.count(), first_job_count)
        self.assertEqual(Skill.objects.count(), first_skill_count)
        self.assertFalse(JobPost.objects.exclude(source=JobPost.Source.SAMPLE).exists())
        self.assertTrue(JobPost.objects.filter(description__startswith="[샘플 공고]").exists())

    def test_clear_removes_only_sample_jobs(self):
        call_command("seed_demo_data", stdout=io.StringIO())
        manual_job = JobPost.objects.create(
            company_name="직접 등록 회사",
            title="직접 등록 공고",
            description="관리자가 직접 등록한 공고",
        )

        call_command("seed_demo_data", clear=True, stdout=io.StringIO())

        self.assertFalse(JobPost.objects.filter(source=JobPost.Source.SAMPLE).exists())
        self.assertTrue(JobPost.objects.filter(pk=manual_job.pk).exists())
