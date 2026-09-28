from django import forms

from .models import CoverLetter, Experience, Resume


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "company", "start_date", "end_date", "description"]
        widgets = {
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                },
                format="%Y-%m-%d",
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500",
                },
                format="%Y-%m-%d",
            ),
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["title", "content"]


class CoverLetterForm(forms.ModelForm):
    class Meta:
        model = CoverLetter
        fields = ["title", "content"]
