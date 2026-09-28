from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.template.loader import get_template
from django.urls import reverse

from .models import Education


class AccountSecurityTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", password="test-password")
        self.attacker = User.objects.create_user("attacker", password="test-password")
        self.education = Education.objects.create(
            user=self.owner,
            school_name="학교",
            major="전공",
            degree="학사",
            start_date=date(2020, 3, 1),
        )
        self.client.force_login(self.attacker)

    def test_cannot_update_another_users_education(self):
        response = self.client.get(
            reverse("accounts:education_edit", args=[self.education.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_cannot_delete_another_users_education(self):
        response = self.client.post(
            reverse("accounts:education_delete", args=[self.education.pk])
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Education.objects.filter(pk=self.education.pk).exists())

    def test_logout_rejects_get(self):
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 405)

    def test_login_page_renders_without_social_app(self):
        self.client.logout()
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    def test_social_confirmation_template_exists(self):
        self.assertIsNotNone(get_template("socialaccount/login.html"))

    def test_list_page_template_exists(self):
        response = self.client.get(reverse("accounts:education_list"))
        self.assertEqual(response.status_code, 200)

    def test_allauth_redirect_preserves_next(self):
        self.client.logout()
        response = self.client.get("/allauth/login/?next=/accounts/profile/")
        self.assertEqual(
            response.url, "/accounts/login/?next=/accounts/profile/"
        )

    def test_login_uses_safe_next_url(self):
        self.client.logout()
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "attacker",
                "password": "test-password",
                "next": "/accounts/profile/",
            },
        )
        self.assertRedirects(
            response, "/accounts/profile/", fetch_redirect_response=False
        )

    def test_signup_redirects_after_success(self):
        self.client.logout()
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "new-user",
                "email": "new@example.com",
                "password1": "a-secure-password-123",
                "password2": "a-secure-password-123",
            },
        )
        self.assertRedirects(response, "/jobs/dashboard/", fetch_redirect_response=False)

# Create your tests here.
