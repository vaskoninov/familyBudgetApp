from django.contrib.auth import get_user_model
from django.db import models

from familyBudgetApp.common.helpers import get_current_year, get_current_month, get_previous_month_and_year
from familyBudgetApp.common.models import Tag

UserModel = get_user_model()


class YearlyBudget(models.Model):
    year = models.IntegerField(default=get_current_year)
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)

    @property
    def yearly_budget(self):
        return self.monthly_budgets.aggregate(models.Sum('balance'))['balance__sum']

    def __str__(self):
        return f"Yearly Budget for {self.year}"

class MonthlyBudget(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_month_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month = models.IntegerField(default=get_current_month)
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    yearly_budget = models.ForeignKey(
        YearlyBudget,
        on_delete=models.DO_NOTHING,
        related_name='monthly_budgets'
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            last_year, last_month = get_previous_month_and_year(self.month, self.yearly_budget.year)
            last_month_budget = MonthlyBudget.objects.filter(
                month=last_month, yearly_budget__year=last_year
            ).first()
            if last_month_budget:
                self.last_month_balance = last_month_budget.balance
                self.balance += last_month_budget.balance
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Monthly Budget for {self.month}/{self.yearly_budget.year}"


class BudgetItem(models.Model):
    BUDGET_ITEM_NAME_MAX_LENGTH = 50
    BUDGET_ITEM_DESCRIPTION_MAX_LENGTH = 150

    class ItemType(models.TextChoices):
        INCOME = 'INCOME'
        EXPENSE = 'EXPENSE'

    name = models.CharField(max_length=BUDGET_ITEM_NAME_MAX_LENGTH)
    item_type = models.CharField(
        max_length=max(len(choice) for choice, _ in ItemType.choices),
        choices=ItemType.choices,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(
        max_length=BUDGET_ITEM_DESCRIPTION_MAX_LENGTH,
        default='',
        blank=True,
    )
    date = models.DateField()
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
    )
    monthly_budget = models.ForeignKey(
        MonthlyBudget,
        on_delete=models.DO_NOTHING,
        related_name='budget_items',
    )

    @property
    def budget_item_tags(self):
        return ", ".join([tag.name for tag in self.tags.all()])

    def __str__(self):
        return self.name
