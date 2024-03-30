from django import forms

from familyBudgetApp.budgetApp.models import BudgetItem
from familyBudgetApp.common.models import Tag


class BudgetItemForm(forms.ModelForm):
    new_tags = forms.CharField(max_length=100, required=False)

    class Meta:
        model = BudgetItem
        exclude = ['user', 'monthly_budget']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
            self.save_m2m()

            # Handle new tags
            new_tags = self.cleaned_data.get("new_tags")
            if new_tags:
                tag_list = [tag.strip() for tag in new_tags.split(",")]
                for tag_name in tag_list:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)

        return instance


class UpdateBudgetItemForm(BudgetItemForm):
    class Meta(BudgetItemForm.Meta):
        model = BudgetItem
        exclude = ['user', 'monthly_budget', 'item_type']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class FilterBudgetItemTypeForm(forms.Form):
    CHOICES = [
        ('', 'All'),
        ('EXPENSE', 'Expense'),
        ('INCOME', 'Income'),
    ]

    category = forms.ChoiceField(choices=CHOICES, required=False)


class FilterBudgetItemTagForm(forms.Form):
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tag'].choices = [('', 'All')] + [(tag.id, tag.name) for tag in Tag.objects.all()]


class FilterBudgetItemNameForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)