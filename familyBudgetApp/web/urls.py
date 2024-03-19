from django.urls import path
from familyBudgetApp.web import views

urlpatterns = (
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
)