from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "제목을 입력하세요 (예: 면접 꿀팁 공유합니다!)",
                }
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 10, "placeholder": "내용을 입력하세요"}
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "댓글을 남겨보세요"}
            ),
        }
