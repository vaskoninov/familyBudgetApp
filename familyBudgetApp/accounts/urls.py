from django.urls import path
from familyBudgetApp.accounts import views

urlpatterns = (
    path('register-new-user/', views.RegisterNewAppUser.as_view(), name='register-new-user'),
    path('login-user/', views.UserLoginView.as_view(), name='login-user'),
    path('logout-user-confirmation/', views.UserLogoutTemplateView.as_view(), name='logout-user-confirmation'),
    path('logout/', views.UserLogoutView.as_view(), name='logout-user'),
    path('user-details/<int:pk>/', views.UserProfileView.as_view(), name='user-details'),
    path('user-details/<int:pk>/profile-update/', views.ProfileUpdateView.as_view(), name='user-profile-update'),
    path('change-user-password/<int:pk>/', views.UserPasswordChangeView.as_view(), name='change-user-password'),
    path('delete-user/<int:pk>/', views.UserDeleteView.as_view(), name='delete-user'),
    path('create-family/', views.CreateFamily.as_view(), name='create-family'),
    path('family-details/<int:pk>/', views.FamilyDetailsView.as_view(), name='family-details'),
    path('send-family-invitation/', views.SendFamilyInvitationView.as_view(), name='send-family-invitation'),
    path('invitation-details/<int:pk>/', views.FamilyInvitationDetailsView.as_view(), name='invitation-details'),
    path('accept-invitation/<int:pk>/', views.AcceptFamilyInvitationView.as_view(), name='accept-invitation'),
    path('decline-invitation/<int:pk>/', views.DeclineFamilyInvitationView.as_view(), name='decline-invitation'),
    path('delete-invitation/<int:pk>/', views.DeleteFamilyInvitationView.as_view(), name='delete-invitation'),
    path('leave-family/<int:pk>/', views.LeaveFamilyView.as_view(), name='leave-family'),
    path('remove-family-user/<int:pk>/', views.AdminRemoveFamilyUserView.as_view(), name='remove-family-user'),
)