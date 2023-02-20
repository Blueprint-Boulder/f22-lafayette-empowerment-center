from django.contrib import admin
from accounts import models

admin.site.register(models.LECUser)
admin.site.register(models.Notification)
