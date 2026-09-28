from django.contrib import admin

from .models import Activity, Certificate, Education, Profile, Project

admin.site.register(Profile)
admin.site.register(Education)
admin.site.register(Certificate)
admin.site.register(Activity)
admin.site.register(Project)
