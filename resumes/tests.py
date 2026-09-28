from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import CoverLetter, Experience, Resume


class ResumeValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user", password="test-password")
        self.client.force_login(self.user)

    def test_resume_title_is_validated(self):
        response = self.client.post(
            reverse("resumes:resume_create"), {"title": "", "content": "본문"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Resume.objects.count(), 0)

    def test_experience_date_is_validated(self):
        response = self.client.post(
            reverse("resumes:experience_create"),
            {
                "title": "개발자",
                "company": "회사",
                "start_date": "not-a-date",
                "description": "내용",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Experience.objects.count(), 0)
        self.assertContains(response, 'value="not-a-date"', html=False)

    def test_ai_coverletter_string_without_job_post(self):
        coverletter = CoverLetter.objects.create(
            user=self.user,
            target_company="테스트 회사",
            target_role="백엔드 개발자",
            title="지원서",
            content="본문",
        )
        self.assertIn("백엔드 개발자", str(coverletter))
