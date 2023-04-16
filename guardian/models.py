from django.db import models
from accounts.models import LECUser
from org_admin.models import Program, Survey, SurveyField


class Student(models.Model):
    name = models.CharField(max_length=500)
    pronouns = models.CharField(max_length=50)
    age = models.IntegerField()
    grade = models.IntegerField()
    allergies = models.TextField(max_length=1000, blank=True)
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_phone_number = models.CharField(max_length=25)
    guardian = models.ForeignKey(to=LECUser, related_name="children", on_delete=models.CASCADE)
    programs = models.ManyToManyField(to=Program, related_name="students")
    additional_info = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class SurveyResponse(models.Model):
    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE, related_name="responses")
    respondent = models.ForeignKey(to=LECUser, on_delete=models.CASCADE, related_name="survey_responses")


class SurveyFieldResponse(models.Model):
    text = models.TextField(max_length=500)
    field = models.ForeignKey(to=SurveyField, on_delete=models.CASCADE, related_name="responses")
    full_response = models.ForeignKey(to=SurveyResponse, on_delete=models.CASCADE, related_name="field_responses")
