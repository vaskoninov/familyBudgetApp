from django.urls import path
from familyBudgetApp.web import views

urlpatterns = (
    path('', views.IndexView.as_view(), name='index'),
)