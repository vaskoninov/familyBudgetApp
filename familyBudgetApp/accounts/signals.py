from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from familyBudgetApp.accounts.models import Profile, Family, FamilyInvitation

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


@receiver(post_save, sender=FamilyInvitation)
def send_invitation_email(sender, instance, created, **kwargs):
    if created:
        subject = f'An invitation to join the {instance.family.name} family'
        message = (f"Dear {instance.invitee_email},\n\n"
                   f"An Invitation from Family Budget App has been received.\n"
                   f"You have been invited to join the {instance.family.name} family by {instance.invited_by}.\n"
                   f"They sent you the following message:\n"
                   f"{instance.message}\n"
                   f"If you would like to join the family, please login into the app!\n"
                   f"Best regards,\n"
                   f"Family Budget App Team")
        from_email = 'vvninov@gmail.com'
        to_email = instance.invitee_email

        send_mail(subject, message, from_email, [to_email])
