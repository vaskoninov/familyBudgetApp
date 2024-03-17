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
