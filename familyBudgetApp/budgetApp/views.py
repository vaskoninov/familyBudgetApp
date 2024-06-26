from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.contrib.messages import views as messages_views
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views import generic as views

from familyBudgetApp.budgetApp.forms import BudgetItemForm, UpdateBudgetItemForm, FilterBudgetItemNameForm, \
    FilterBudgetItemTagForm
from familyBudgetApp.budgetApp.forms import FilterBudgetItemTypeForm
from familyBudgetApp.budgetApp.models import BudgetItem, YearlyBudget, MonthlyBudget
from familyBudgetApp.common.helpers import get_users_from_family
from familyBudgetApp.common.mixins import RefererURLMixin, SearchMixin, TagFilterMixin, CategoryFilterMixin, \
    UserIsCreatorMixin


# Create your views here.

class CreateBudgetItemView(auth_mixins.LoginRequiredMixin, messages_views.SuccessMessageMixin, views.CreateView):
    model = BudgetItem
    form_class = BudgetItemForm
    template_name = "budgetApp/create-new-budget-entry.html"
    success_url = reverse_lazy("index")
    success_message = "Budget item - %(name)s - created successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return response


class ViewBudgetItemDetails(auth_mixins.LoginRequiredMixin, RefererURLMixin, views.DetailView):
    model = BudgetItem
    template_name = "budgetApp/budget-item-details.html"
    context_object_name = "budget_item"


class UpdateBudgetItemView(auth_mixins.LoginRequiredMixin, UserIsCreatorMixin, RefererURLMixin,
                           messages_views.SuccessMessageMixin, views.UpdateView):
    model = BudgetItem
    form_class = UpdateBudgetItemForm
    template_name = "budgetApp/update-budget-item.html"
    context_object_name = "budget_item"
    success_url = reverse_lazy("index")
    success_message = "Budget item - %(name)s - updated successfully!"


class DeleteBudgetItemView(auth_mixins.LoginRequiredMixin, UserIsCreatorMixin, RefererURLMixin,
                           messages_views.SuccessMessageMixin, views.DeleteView):
    model = BudgetItem
    template_name = "budgetApp/delete-budget-item.html"
    success_url = reverse_lazy("index")
    success_message = "Budget item - %(name)s - deleted successfully!"


class AbstractBudgetItemListView(auth_mixins.LoginRequiredMixin, SearchMixin, TagFilterMixin, CategoryFilterMixin,
                                 views.ListView):
    model = BudgetItem

    context_object_name = "budget_items"
    paginate_by = 5
    ordering = ["-date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filter_form'] = FilterBudgetItemTypeForm(initial={"category": self.request.GET.get('category')})
        context['filter_tags'] = FilterBudgetItemTagForm(initial={"tag": self.request.GET.get('tag')})
        context['search_term'] = FilterBudgetItemNameForm(initial={"title": self.request.GET.get('name')})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = self.apply_category_filter(queryset)
        queryset = self.apply_tag_filter(queryset)
        queryset = self.apply_search_filter(queryset)

        return queryset


class BudgetItemListView(AbstractBudgetItemListView):
    template_name = "budgetApp/list-budget-items.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class FamilyBudgetItemListAdminView(AbstractBudgetItemListView):
    template_name = "budgetApp/list-budget-items.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        family = self.request.user.profile.family
        family_members = get_users_from_family(family)
        return queryset.filter(user__in=family_members)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['family'] = self.request.user.profile.family
        return context


class ViewYearBudgetsByYear(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = YearlyBudget
    template_name = "budgetApp/yearly-budget.html"
    context_object_name = "yearly_budget"

    def get_object(self, queryset=None):
        year = self.kwargs.get('year')
        return YearlyBudget.objects.get(year=year, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["monthly_budgets"] = self.object.monthly_budgets.all().order_by("-month")
        return context


class ViewMonthlyBudgetDetails(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = YearlyBudget
    template_name = "budgetApp/monthly-budget.html"
    context_object_name = "monthly-budget"

    def get_object(self, queryset=None):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        return MonthlyBudget.objects.filter(yearly_budget__year=year, month=month, user=self.request.user).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        incomes = self.object.budget_items.filter(item_type='INCOME').order_by('-date')
        expenses = self.object.budget_items.filter(item_type='EXPENSE').order_by('-date')
        context["incomes"] = incomes
        context["expenses"] = expenses
        return context


class FamilyViewForNonAdmin(auth_mixins.LoginRequiredMixin, views.TemplateView):
    template_name = "budgetApp/family-view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        family = self.request.user.profile.family
        family_members = get_users_from_family(family)
        context["family_members"] = family_members
        context['family'] = family

        yearly_budgets = YearlyBudget.objects.filter(user__in=family_members)

        context['years'] = yearly_budgets.values_list('year', flat=True).distinct()

        total_monthly_balances = {}
        for year in context['years']:
            total_monthly_balances[year] = {}
            for month in range(1, 13):
                monthly_budgets = MonthlyBudget.objects.filter(
                    yearly_budget__year=year,
                    month=month,
                    user__in=family_members
                )
                if monthly_budgets.exists():
                    total_monthly_balances[year][month] = monthly_budgets.aggregate(Sum('balance'))['balance__sum']

        context["total_monthly_balances"] = total_monthly_balances

        return context


class FamilyMonthlyBudgetAdminView(auth_mixins.LoginRequiredMixin, views.TemplateView):
    template_name = "budgetApp/family-monthly-budget-admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        family = self.request.user.profile.family
        family_members = get_users_from_family(family)
        context["family_members"] = family_members
        context['family'] = family

        year = self.kwargs.get('year')
        month = self.kwargs.get('month')

        incomes = BudgetItem.objects.filter(user__in=family_members, item_type='INCOME', date__year=year,
                                            date__month=month)
        expenses = BudgetItem.objects.filter(user__in=family_members, item_type='EXPENSE', date__year=year,
                                             date__month=month)

        context["incomes"] = incomes
        context["expenses"] = expenses

        return context
