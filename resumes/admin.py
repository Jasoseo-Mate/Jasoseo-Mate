from django.contrib import admin

from .models import CoverLetter, Experience, Resume

admin.site.register(Experience)
admin.site.register(Resume)
admin.site.register(CoverLetter)
