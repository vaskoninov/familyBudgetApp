from django.contrib import messages
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages import views as messages_views
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import TemplateView

from familyBudgetApp.accounts.forms import AppUserCreationForm, FamilyInvitationForm
from familyBudgetApp.accounts.models import FamilyInvitation, Profile, Family
from familyBudgetApp.common.mixins import RefererURLMixin

# Create your views here.
UserModel = get_user_model()


class RegisterNewAppUser(messages_views.SuccessMessageMixin, views.CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = "accounts/register-new-user.html"
    success_url = reverse_lazy('index')
    success_message = "User - %(email)s - created successfully!"

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return super().form_invalid(form)


class UserLoginView(auth_views.LoginView):
    template_name = "accounts/login-user.html"
    next_page = reverse_lazy('index')
    redirect_authenticated_user = True


class UserLogoutTemplateView(LoginRequiredMixin, RefererURLMixin, TemplateView):
    template_name = "accounts/logout-user-confirmation.html"


class UserLogoutView(LoginRequiredMixin, auth_views.LogoutView):
    next_page = reverse_lazy('index')


class UserProfileView(LoginRequiredMixin, RefererURLMixin, views.DetailView):
    model = UserModel
    template_name = "accounts/user-details.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invitations = FamilyInvitation.objects.filter(invitee_email=self.request.user.email, status='pending')
        family = self.object.profile.family if hasattr(self.object, 'profile') else None
        context['invitations'] = invitations
        context['family'] = family
        return context


class ProfileUpdateView(LoginRequiredMixin, RefererURLMixin, messages_views.SuccessMessageMixin, views.UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'age', ]
    template_name = "accounts/user-profile-update.html"
    success_message = "Profile updated successfully!"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('user-details', kwargs={'pk': self.request.user.pk})


class UserPasswordChangeView(LoginRequiredMixin, RefererURLMixin, messages_views.SuccessMessageMixin,
                             auth_views.PasswordChangeView):
    form_class = auth_forms.PasswordChangeForm
    template_name = "accounts/change-user-password.html"
    success_message = "Password changed successfully!"

    def get_success_url(self):
        user_id = self.request.user.pk
        return reverse_lazy('user-profile', kwargs={"pk": user_id})

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, RefererURLMixin, UserPassesTestMixin, views.DeleteView):
    model = UserModel
    template_name = 'accounts/delete-user.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        user = self.get_object()
        return user == self.request.user

    def get_object(self, queryset=None):
        return self.request.user


class CreateFamily(LoginRequiredMixin, RefererURLMixin, messages_views.SuccessMessageMixin, views.CreateView):
    model = Family
    fields = ['name', 'description', ]
    template_name = "accounts/create-family.html"
    success_message = "Family - %(name)s created successfully!"

    def get_success_url(self):
        user_id = self.request.user.pk
        return reverse_lazy('user-details', kwargs={'pk': user_id})

    def form_valid(self, form):
        family = form.save(commit=False)
        user = self.request.user

        if user.profile.family:
            messages.info(self.request, 'You already have a family. You cannot create another one.')
            return redirect(self.get_success_url())

        family.admin = user
        family.save()

        user_profile = user.profile
        user_profile.family = family
        user_profile.save()

        return super().form_valid(form)


class FamilyDetailsView(LoginRequiredMixin, RefererURLMixin, views.DetailView):
    model = Family
    template_name = 'accounts/family-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        family = self.get_object()
        family_members = UserModel.objects.filter(profile__family=family)
        sent_invitations = FamilyInvitation.objects.filter(invited_by=self.request.user)
        context['family_members'] = family_members
        context['sent_invitations'] = sent_invitations
        return context


class SendFamilyInvitationView(LoginRequiredMixin, RefererURLMixin, PermissionRequiredMixin, views.CreateView):
    permission_required = 'accounts.add_familyinvitation'
    model = FamilyInvitation
    form_class = FamilyInvitationForm  # Use the custom form
    template_name = "accounts/send-family-invitation.html"

    def get_success_url(self):
        user_id = self.request.user.pk
        return reverse_lazy('user-details', kwargs={"pk": user_id})

    def form_valid(self, form):
        invitation = form.save(commit=False)
        user = self.request.user
        invitation.family = user.profile.family
        invitation.invited_by = user
        invitation.save()
        messages.success(self.request, "Invitation sent successfully.")
        return super().form_valid(form)


class FamilyInvitationDetailsView(LoginRequiredMixin, RefererURLMixin, views.DetailView):
    model = FamilyInvitation
    template_name = 'accounts/invitation-details.html'


class AcceptFamilyInvitationView(LoginRequiredMixin, RefererURLMixin, views.UpdateView):
    model = FamilyInvitation
    fields = []
    template_name = 'accounts/accept-invitation.html'

    def get_object(self, queryset=None):
        invitation = super().get_object(queryset)
        if invitation.invitee_email != self.request.user.email:
            messages.info(self.request, "Invitation not found or not for this user.")
            return redirect(self.get_success_url())
        return invitation

    def get_success_url(self):
        user_id = self.request.user.pk
        return reverse_lazy('user-details', kwargs={"pk": user_id})

    def form_valid(self, form):
        invitation = form.save(commit=False)

        if invitation.status != 'pending':
            messages.info(self.request, 'Invitation has already been accepted or rejected.')
            return redirect(self.get_success_url())

        invitation.status = 'accepted'
        invitation.save()
        user = self.request.user
        user_profile = user.profile
        user_profile.family = invitation.family
        user_profile.save()

        return super().form_valid(form)


class DeclineFamilyInvitationView(LoginRequiredMixin, RefererURLMixin, views.UpdateView):
    model = FamilyInvitation
    fields = []
    template_name = 'accounts/decline-invitation.html'

    def get_success_url(self):
        user_id = self.request.user.pk
        return reverse_lazy('user-profile', kwargs={"pk": user_id})

    def form_valid(self, form):
        invitation = form.save(commit=False)
        if invitation.status != 'pending':
            messages.info(self.request, 'Invitation has already been accepted or rejected.')
            return redirect(self.get_success_url())

        invitation.status = 'declined'
        invitation.save()
        return super().form_valid(form)


class DeleteFamilyInvitationView(LoginRequiredMixin, RefererURLMixin, views.DeleteView):
    model = FamilyInvitation
    template_name = 'accounts/delete-invitation.html'

    def get_success_url(self):
        user_id = self.request.user.pk
        return reverse_lazy('user-profile', kwargs={"pk": user_id})

    def get_object(self, queryset=None):
        invitation = super().get_object(queryset)
        if invitation.invited_by.email != self.request.user.email:
            messages.info(self.request, "You did not send this invitation. You cannot delete it.")
            return redirect(self.get_success_url())
        return invitation


class LeaveFamilyView(LoginRequiredMixin, RefererURLMixin, views.UpdateView):
    model = Profile
    fields = []
    template_name = 'accounts/leave-family.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        user_id = self.request.user.pk
        return reverse_lazy('user-profile', kwargs={"pk": user_id})

    def form_valid(self, form):
        profile = form.save(commit=False)
        if profile.family is None:
            messages.info(self.request, 'You are not part of any family.')
            return redirect(self.get_success_url())

        profile.family = None
        profile.save()
        messages.success(self.request, 'You have successfully left the family.')
        return super().form_valid(form)


class AdminRemoveFamilyUserView(LoginRequiredMixin, RefererURLMixin, views.UpdateView):
    model = Profile
    fields = []
    template_name = 'accounts/remove-family-user.html'

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')
        return get_object_or_404(Profile, user__id=user_id)

    def get_success_url(self):
        return reverse_lazy('family-details', kwargs={"pk": self.request.user.profile.family.id})

    def form_valid(self, form):
        profile = form.save(commit=False)
        if profile.family is None or profile.family.admin != self.request.user:
            messages.info(self.request, 'The user is not part of your family.')
            return redirect(self.get_success_url())

        profile.family = None
        profile.save()
        messages.success(self.request, 'The user has been successfully removed from the family.')
        return super().form_valid(form)


class AdminLeaveDeleteFamilyView(LoginRequiredMixin, RefererURLMixin, views.DeleteView):
    model = Family
    template_name = 'accounts/leave-delete-family.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user.profile.family

    def delete(self, *args, **kwargs):
        family = self.get_object()
        if family.admin != self.request.user:
            messages.info(self.request, 'You are not the admin of this family.')
            return redirect(self.get_success_url())

        Profile.objects.filter(family=family).update(family=None)
        FamilyInvitation.objects.filter(family=family).delete()

        messages.success(self.request, 'The family has been successfully deleted.')
        return super().delete(*args, **kwargs)
