import json
import xml.etree.ElementTree as ET
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse

from resumes.models import CoverLetter

from .models import JobPost
from .management.commands.fetch_worknet_jobs import (
    Command,
    WORK24_JOB_DETAIL_API_URL,
    normalize_company_size,
)


class JobViewSecurityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user", password="test-password")

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
        mocked_get.return_value = Mock(
            text="""
                <wantedRoot><wanted>
                    <wantedAuthNo>wanted-123</wantedAuthNo>
                    <company>기존 회사</company><title>기존 공고</title>
                </wanted></wantedRoot>
            """
        )
        call_command("fetch_worknet_jobs")
        self.assertEqual(mocked_get.call_count, 1)

# Create your tests here.
