from django.urls import path
from familyBudgetApp.accounts.views import RegisterNewAppUser, UserLoginView

urlpatterns = (
    path('register-new-user/', RegisterNewAppUser.as_view(), name='register-new-user'),
    path('login-user/', UserLoginView.as_view(), name='login-user'),
)