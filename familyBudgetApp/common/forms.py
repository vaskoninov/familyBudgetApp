from django import forms

from familyBudgetApp.common.models import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']