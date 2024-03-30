from django.urls import path

from familyBudgetApp.common import views

urlpatterns = (
    path("/create-new-tag/", views.CreateTagView.as_view(), name="create-new-tag"),
)
