from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views

from familyBudgetApp.accounts.forms import AppUserCreationForm

# Create your views here.
UserModel = get_user_model()


class RegisterNewAppUser(views.CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = "accounts/register-new-user.html"
    success_url = reverse_lazy('index')


class UserLoginView(auth_views.LoginView):
    template_name = "accounts/login-user.html"
    next_page = reverse_lazy('index')
    redirect_authenticated_user = True
