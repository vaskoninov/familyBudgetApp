from django.contrib import admin

from familyBudgetApp.common.models import Tag


# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
