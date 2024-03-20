from django.shortcuts import render
from django.views import generic as views

from familyBudgetApp.budgetApp.models import MonthlyBudget, YearlyBudget
from familyBudgetApp.common.helpers import get_current_year, get_current_month


# Create your views here.
class IndexView(views.TemplateView):
    template_name = 'web/index.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'web/not-logged-user.html')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        year = get_current_year()
        month = get_current_month()

        context['year'] = year
        context['month'] = month

        yearly_budget = YearlyBudget.objects.filter(user=user, year=year).first()
        monthly_budget = MonthlyBudget.objects.filter(user=user, month=month, yearly_budget=yearly_budget).first()
        if monthly_budget:
            context['budget_balance'] = monthly_budget.balance
        else:
            context['budget_balance'] = 0

        return context


class AboutView(views.TemplateView):
    template_name = 'web/about.html'
