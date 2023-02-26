from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import django.contrib.auth.views as base_auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import LECUserCreationForm
from accounts.models import LECUser

@login_required
def profile(request):
    return render(request, "accounts/profile.html", {"account_types": LECUser.AccountTypes})

class EditProfile(LoginRequiredMixin, UpdateView):
    """View for a user to edit their profile."""
    model = LECUser
    template_name = "accounts/edit_profile.html"
    fields = ["username", "first_name", "last_name", "email"]
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user

def login_register(request):
    return render(request, "accounts/login_register.html")


class Login(base_auth_views.LoginView):
    template_name = "accounts/login.html"
    success_url = "/"

class Logout(base_auth_views.LogoutView):
    pass

class CreateAccount(CreateView):
    model = LECUser
    form_class = LECUserCreationForm
    template_name = "accounts/create_account.html"
    success_url = reverse_lazy("accounts:account_created")


def account_created(request):
    return render(request, "accounts/account_created.html")
