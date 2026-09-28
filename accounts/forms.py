from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Activity, Certificate, Education, Profile, Project


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = "사용자 이름을 입력해주세요."
        self.fields["email"].help_text = "연락 가능한 이메일 주소를 입력해주세요."
        self.fields["password1"].help_text = "비밀번호는 최소 8자 이상이어야 합니다."
        self.fields["password2"].label = "비밀번호 확인"
        self.fields["password2"].help_text = "비밀번호를 다시 한번 입력해주세요."


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "skills", "preferred_company_size"]
        widgets = {
            "skills": forms.CheckboxSelectMultiple,
            "preferred_company_size": forms.Select(
                attrs={
                    "class": "mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md border"
                }
            ),
        }


class EducationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "YYYY-MM-DD"}),
        input_formats=["%Y-%m-%d", "%Y/%m/%d"],
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "YYYY-MM-DD"}),
        input_formats=["%Y-%m-%d", "%Y/%m/%d"],
        required=False,
    )

    class Meta:
        model = Education
        fields = ["school_name", "major", "degree", "start_date", "end_date"]


class CertificateForm(forms.ModelForm):
    date_acquired = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "YYYY-MM-DD"}),
        input_formats=["%Y-%m-%d", "%Y/%m/%d"],
    )

    class Meta:
        model = Certificate
        fields = ["name", "issuer", "date_acquired"]


class ActivityForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "YYYY-MM-DD"}),
        input_formats=["%Y-%m-%d", "%Y/%m/%d"],
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "YYYY-MM-DD"}),
        input_formats=["%Y-%m-%d", "%Y/%m/%d"],
        required=False,
    )

    class Meta:
        model = Activity
        fields = ["title", "description", "start_date", "end_date"]


class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "YYYY-MM-DD"}),
        input_formats=["%Y-%m-%d", "%Y/%m/%d"],
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "YYYY-MM-DD"}),
        input_formats=["%Y-%m-%d", "%Y/%m/%d"],
        required=False,
    )

    class Meta:
        model = Project
        fields = ["title", "description", "start_date", "end_date", "url"]
