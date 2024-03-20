
import threading

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver


from .models import BudgetItem, YearlyBudget, MonthlyBudget

__old_instance_cache = threading.local()
__old_instance_cache.cache = {}


@receiver(pre_save, sender=BudgetItem)
def capture_old_instance_state(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            if not hasattr(__old_instance_cache, 'cache'):
                __old_instance_cache.cache = {}
            __old_instance_cache.cache[instance.pk] = old_instance
        except sender.DoesNotExist:
            pass


@receiver(pre_save, sender=BudgetItem)
def link_budget_item_to_monthly_budget(sender, instance, **kwargs):
    if not instance.monthly_budget_id:
        year = instance.date.year
        month = instance.date.month
        user = instance.user

        yearly_budget, _ = YearlyBudget.objects.get_or_create(user=user, year=year)

        monthly_budget, _ = MonthlyBudget.objects.get_or_create(
            user=user,
            month=month,
            yearly_budget=yearly_budget
        )

        instance.monthly_budget = monthly_budget


@receiver(post_save, sender=BudgetItem)
def update_monthly_budget_balance_on_budget_item(sender, instance, created, **kwargs):
    monthly_budget = instance.monthly_budget
    if created:
        if instance.item_type == BudgetItem.ItemType.EXPENSE:
            monthly_budget.balance -= instance.amount
        else:
            monthly_budget.balance += instance.amount
    else:
        old_instance = __old_instance_cache.cache.get(instance.pk, None)
        if old_instance:
            if instance.item_type == BudgetItem.ItemType.EXPENSE:
                monthly_budget.balance += old_instance.amount - instance.amount
            else:
                monthly_budget.balance -= old_instance.amount - instance.amount
    monthly_budget.save()


@receiver(post_delete, sender=BudgetItem)
def adjust_budget_on_delete(sender, instance, **kwargs):
    monthly_budget = instance.monthly_budget
    if instance.item_type == BudgetItem.ItemType.EXPENSE:
        monthly_budget.balance += instance.amount
    else:
        monthly_budget.balance -= instance.amount
    monthly_budget.save()


