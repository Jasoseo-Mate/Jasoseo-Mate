from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Comment, Post


class CommunityMethodTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("author", password="test-password")
        self.post = Post.objects.create(author=self.user, title="제목", content="내용")
        self.comment = Comment.objects.create(
            post=self.post, author=self.user, content="댓글"
        )
        self.client.force_login(self.user)

    def test_post_delete_rejects_get(self):
        response = self.client.get(reverse("community:post_delete", args=[self.post.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_comment_delete_rejects_get(self):
        response = self.client.get(
            reverse(
                "community:comment_delete", args=[self.post.pk, self.comment.pk]
            )
        )
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

# Create your tests here.
