from django.contrib import admin
from guardian import models

admin.site.register(models.Student)
admin.site.register(models.SurveyResponse)
admin.site.register(models.SurveyFieldResponse)

