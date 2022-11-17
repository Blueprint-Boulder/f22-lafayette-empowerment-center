from django.db import models
from django.utils import timezone

from accounts.models import LECUser


class Program(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    is_active = models.BooleanField()
    registration_opens = models.DateTimeField()
    registration_closes = models.DateTimeField()
    program_starts = models.DateTimeField()
    program_ends = models.DateTimeField()

    def __str__(self):
        return self.name


class Survey(models.Model):
    name = models.CharField(max_length=100)
    program = models.ForeignKey(to=Program, on_delete=models.CASCADE, related_name="surveys")
    is_active = models.BooleanField()

    def __str__(self):
        return self.name


class SurveyField(models.Model):
    label = models.CharField(max_length=100)
    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE, related_name="fields")

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

class CommunityContact(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=25, blank=True)
    other_contact_info = models.TextField(max_length=500, blank=True)
