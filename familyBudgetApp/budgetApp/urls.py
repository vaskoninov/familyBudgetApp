from django.urls import path

from familyBudgetApp.budgetApp import views

urlpatterns = (
    path('create-new-budget-entry/', views.CreateBudgetItemView.as_view(), name='create-budget-item'),
    path('budget-item/<int:pk>/details/', views.ViewBudgetItemDetails.as_view(), name='view-budget-item-details'),
    path('budget-item/<int:pk>/update/', views.UpdateBudgetItemView.as_view(), name='update-budget-item'),
    path('budget-item/<int:pk>/delete/', views.DeleteBudgetItemView.as_view(), name='delete-budget-item'),
    path('list-budget-items/', views.BudgetItemListView.as_view(), name='list-budget-items'),
    path('family-list-budget-items/', views.FamilyBudgetItemListAdminView.as_view(), name='family-list-budget-items'),
    path('family-year-month/', views.FamilyViewForNonAdmin.as_view(), name='family-year-month'),
    path('<int:pk>/yearly-budget/<int:year>/', views.ViewYearBudgetsByYear.as_view(), name='yearly-budget'),
    path('<int:pk>/monthly-budget/<int:year>/<int:month>/', views.ViewMonthlyBudgetDetails.as_view(),
         name='monthly-budget'),
    path('family-monthly-budget/<int:year>/<int:month>/', views.FamilyMonthlyBudgetAdminView.as_view(),
         name='family-monthly-budget'),
)
