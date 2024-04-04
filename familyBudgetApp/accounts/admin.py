from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin

from .forms import AppUserCreationForm, AppUserChangeForm
from .models import Profile, FamilyInvitation

UserModel = get_user_model()


@admin.register(UserModel)
class UserModelAdmin(auth_admin.UserAdmin):
    list_display = ("email", "is_superuser", "is_staff")
    search_fields = ("email",)
    ordering = ("email",)

    form = AppUserChangeForm
    add_form = AppUserCreationForm

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ()}),
        ("Permissions", {"fields": ("is_active", "is_staff", "groups",
                                    "user_permissions")}),

        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'family', 'first_name', 'last_name', 'age')
    search_fields = ('user__email', 'first_name', 'last_name')
    list_filter = ('family', 'age')


@admin.register(FamilyInvitation)
class FamilyInvitation(admin.ModelAdmin):
    list_display = ('invited_by', 'invitee_email', 'status')
    list_filter = ('status', 'invited_by', 'invitee_email')
    search_fields = ('invited_by', 'invitee_email', 'status')
    ordering = ('-created_at',)
