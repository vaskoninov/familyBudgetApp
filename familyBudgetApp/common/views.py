from django.shortcuts import render
from django.contrib.messages import views as messages_views
from django.views import generic as views
from django.urls import reverse_lazy

from familyBudgetApp.common.mixins import RefererURLMixin
from familyBudgetApp.common.models import Tag


# Create your views here.

class CreateTagView(RefererURLMixin, messages_views.SuccessMessageMixin, views.CreateView):
    model = Tag
    fields = ['name']
    template_name = 'common/create-new-tag.html'
    success_message = "Tag %(name)s created successfully!"
    success_url = reverse_lazy('index')
