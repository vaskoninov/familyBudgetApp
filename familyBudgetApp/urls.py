
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('familyBudgetApp.web.urls')),
    path('accounts/', include('familyBudgetApp.accounts.urls')),
    path('common/', include('familyBudgetApp.common.urls')),
    path('budgetApp/', include('familyBudgetApp.budgetApp.urls')),
]
