from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from .models import Profile

UserModel = get_user_model()


class AccountUserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel
        fields = '__all__'


class AccountUserCreationForm(auth_forms.UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = (UserModel.USERNAME_FIELD,)

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            user=user,
            age=self.cleaned_data["age"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
        )

        if commit:
            profile.save()

        return user