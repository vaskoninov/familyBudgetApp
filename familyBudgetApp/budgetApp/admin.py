from django.contrib import admin

from familyBudgetApp.budgetApp.models import YearlyBudget, MonthlyBudget, BudgetItem


# Register your models here.
@admin.register(YearlyBudget)
class YearlyBudgetAdmin(admin.ModelAdmin):
    list_display = ('year', 'user', 'yearly_budget')


@admin.register(MonthlyBudget)
class MonthlyBudgetAdmin(admin.ModelAdmin):
    list_display = ('month', 'user', 'yearly_budget', 'balance', 'last_month_balance')


@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'amount', 'monthly_budget', 'user', 'date', 'description')
