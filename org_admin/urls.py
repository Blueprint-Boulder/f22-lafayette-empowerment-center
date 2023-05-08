from django.forms import Form
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from org_admin import views

app_name = "org_admin"

urlpatterns = [
    path('', views.home, name="home"),
    path('delete_this/', lambda request: render(request, "stylized_form_snippet.html", {'form': Form()})),
    path('children/<int:child_pk>/', views.view_child, name="view_child"),
    path('students/', views.view_students, name="view_students"),
    path('programs/', views.programs, name="programs"),
    path('programs/add/', views.AddProgram.as_view(), name="add_program"),
    path('programs/<int:program_pk>/', views.view_program, name="view_program"),
    path('programs/<int:pk>/edit', views.EditProgram.as_view(), name="edit_program"),
    path('programs/<int:program_pk>/surveys/add/', views.create_survey, name="create_survey"),
    path('programs/<int:program_pk>/announcements/add/', views.MakeAnnouncement.as_view(), name="make_announcement"),
    path('surveys/<int:survey_pk>/responses/', views.survey_responses, name="view_survey_responses"),
    path('surveys/<int:response_pk>/response', views.survey_response, name="survey_response"),
    path('contacts/', views.community_contacts, name="community_contacts"),
    path('contacts/add/', views.AddCommunityContact.as_view(), name="add_community_contact")
]
