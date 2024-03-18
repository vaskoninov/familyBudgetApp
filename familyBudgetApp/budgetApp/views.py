from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from familyBudgetApp.budgetApp.forms import BudgetItemForm
from familyBudgetApp.budgetApp.models import BudgetItem


# Create your views here.

class CreateBudgetItemView(views.CreateView):
    model = BudgetItem
    form_class = BudgetItemForm
    template_name = "budgetApp/create-new-budget-entry.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)