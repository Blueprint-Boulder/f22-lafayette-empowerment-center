from django.db import models
from django.utils import timezone

from accounts.models import LECUser


class Program(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    is_active = models.BooleanField(default=False)
    start_time = models.TimeField()  # ex. 12:00
    end_time = models.TimeField()
    start_date = models.DateField()  # ex. 08/15/22
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Survey(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField()
    program = models.ForeignKey(to=Program, on_delete=models.CASCADE, related_name="surveys")

    def __str__(self):
        return self.name


class SurveyField(models.Model):
    label = models.CharField(max_length=100)
    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.label


class ProgramAnnouncement(models.Model):
    time_sent = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=2000)
    program = models.ForeignKey(to=Program, on_delete=models.CASCADE, related_name="announcements")
    read_by = models.ManyToManyField(to=LECUser, related_name="announcements_read", blank=True)

    def __str__(self):
        return self.title
