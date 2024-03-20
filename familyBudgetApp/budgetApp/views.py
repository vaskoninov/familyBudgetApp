from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic as views

from familyBudgetApp.budgetApp.forms import BudgetItemForm, UpdateBudgetItemForm, FilterBudgetItemNameForm
from familyBudgetApp.budgetApp.forms import FilterBudgetItemTypeForm
from familyBudgetApp.budgetApp.models import BudgetItem
from familyBudgetApp.common.mixins import RefererURLMixin, SearchMixin, TagFilterMixin, CategoryFilterMixin


# Create your views here.

class CreateBudgetItemView(views.CreateView):
    model = BudgetItem
    form_class = BudgetItemForm
    template_name = "budgetApp/create-new-budget-entry.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ViewBudgetItemDetails(RefererURLMixin, views.DetailView):
    model = BudgetItem
    template_name = "budgetApp/budget-item-details.html"
    context_object_name = "budget_item"


class UpdateBudgetItemView(RefererURLMixin, views.UpdateView):
    model = BudgetItem
    form_class = UpdateBudgetItemForm
    template_name = "budgetApp/update-budget-item.html"
    context_object_name = "budget_item"
    success_url = reverse_lazy("index")


class DeleteBudgetItemView(RefererURLMixin, views.DeleteView):
    model = BudgetItem
    template_name = "budgetApp/delete-budget-item.html"
    success_url = reverse_lazy("index")


class BudgetItemListView(TagFilterMixin, CategoryFilterMixin, SearchMixin, views.ListView):
    model = BudgetItem
    template_name = "budgetApp/list-budget-items.html"
    context_object_name = "budget_items"
    paginate_by = 5
    ordering = ["-date"]

    def get_queryset(self):
        # Filter budget items by the authenticated user
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass query parameters to forms
        context['filter_form'] = FilterBudgetItemTypeForm(initial={"category": self.request.GET.get('item_type')})
        context['tags'] = self.get_search_tag_id()
        context['search_term'] = FilterBudgetItemNameForm(initial={"title": self.request.GET.get('name')})
        return context