from django.http import HttpResponse
from django.urls import path
from org_admin import views

app_name = "org_admin"

urlpatterns = [
    path('', lambda request: HttpResponse("not implemented"), name="home"),
    path('programs/', views.programs, name="programs"),
    path('programs/add/', views.AddProgram.as_view(), name="add_program"),
    path('programs/<int:program_pk>/', views.view_program, name="view_program"),
    path('programs/<int:program_pk>/surveys/add/', views.create_survey, name="create_survey"),
    path('programs/<int:program_pk>/announcements/add/', views.MakeAnnouncement.as_view(), name="make_announcement"),
    path('surveys/<int:survey_pk>/responses/', views.survey_responses, name="view_survey_responses"),
]
