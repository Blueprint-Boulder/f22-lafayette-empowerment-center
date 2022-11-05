from django.http import HttpResponse
from django.urls import path
from guardian import views

app_name = "guardian"

urlpatterns = [
    path('home/', lambda request: HttpResponse("not implemented"), name="home"),
    path('programs/', views.programs, name="programs"),
    path('programs/<int:program_pk>/', views.view_program, name="view_program"),
    path('programs/<int:program_pk>/register/', views.register_for_program, name="register_for_program"),
    path('surveys/<int:survey_pk>/', views.take_survey, name="take_survey"),
    path('announcements/<int:announcement_pk>/', views.view_announcement, name="view_announcement"),
    path('children/', views.children, name="children"),
    path('children/add/', views.AddChild.as_view(), name="add_child"),
    path('children/add/<path:redirect_to>/', views.AddChild.as_view(), name="add_child_then_redirect")
]
