from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from django.core.exceptions import ValidationError

from .models import Profile, FamilyInvitation

UserModel = get_user_model()


class AppUserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel
        fields = '__all__'


class AppUserCreationForm(auth_forms.UserCreationForm):

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = (UserModel.USERNAME_FIELD,)


class FamilyInvitationForm(forms.ModelForm):
    class Meta:
        model = FamilyInvitation
        fields = ['invitee_email', 'message']

    def clean_invitee_email(self):
        invitee_email = self.cleaned_data.get('invitee_email')

        try:
            invitee = UserModel.objects.get(email=invitee_email)
        except UserModel.DoesNotExist:
            raise ValidationError('User does not exist.')

        if invitee.profile.family:
            raise ValidationError('User already has a family.')

        return invitee_email