from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from familyBudgetApp.accounts.models import Profile, Family

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        base_group = Group.objects.get(name='BaseFunctions')
        instance.groups.add(base_group)


@receiver(post_save, sender=Family)
def add_user_as_family_admin(sender, instance, created, **kwargs):
    if created:
        family_admin_group = Group.objects.get(name='FamilyAdmin')
        instance.admin.groups.add(family_admin_group)