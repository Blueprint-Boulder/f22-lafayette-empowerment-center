from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path('login_register/', views.login_register, name='login_register'),
    path('login/', views.Login.as_view(), name='login'),
    path('create/', views.CreateAccount.as_view(), name='create'),
    path('create/success/', views.account_created, name='account_created'),
    path('profile/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.EditProfile.as_view(), name='edit_profile'),
]
