from django.urls import path
from familyBudgetApp.budgetApp.views import CreateBudgetItemView

urlpatterns = (
    path('create-new-budget-entry/', CreateBudgetItemView.as_view(), name='create_budget_item'),
)