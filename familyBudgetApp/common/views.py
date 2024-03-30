from django.shortcuts import render
from django.views import generic as views
from django.urls import reverse_lazy

from familyBudgetApp.common.mixins import RefererURLMixin
from familyBudgetApp.common.models import Tag


# Create your views here.

class CreateTagView(RefererURLMixin, views.CreateView):
    model = Tag
    fields = ['name']
    template_name = 'common/create-new-tag.html'
    success_url = reverse_lazy('index')
