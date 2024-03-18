from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from familyBudgetApp.accounts.managers import AppUserManager


# Create your models here.

class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        }
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AppUserManager()

    def __str__(self):
        return self.email


class Family(models.Model):
    FAMILY_NAME_MAX_LENGTH = 20
    FAMILY_DESCRIPTION_MAX_LENGTH = 150

    name = models.CharField(
        max_length=FAMILY_NAME_MAX_LENGTH,
        null=True,
        blank=True,
    )
    description = models.TextField(
        max_length=FAMILY_DESCRIPTION_MAX_LENGTH,
        null=True,
        blank=True,
    )
    admin = models.ForeignKey(
        AppUser,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="family_admin",
    )

    class Meta:
        verbose_name_plural = "Families"


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MAX_LENGTH = 30

    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        related_name="profile",
        primary_key=True,
    )
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        blank=True,
        null=True)

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        blank=True,
        null=True)

    age = models.PositiveIntegerField(
        blank=True,
        null=True)

    family = models.ForeignKey(
        Family,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="family_members",
    )


class FamilyInvitation(models.Model):
    MAX_EMAIL_LENGTH = 150
    MESSAGE_MAX_LENGTH = 150

    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(
        max_length=MESSAGE_MAX_LENGTH,
        null=True,
        blank=True,
    )

    family = models.ForeignKey(
        Family,
        on_delete=models.DO_NOTHING,
    )
    invited_by = models.ForeignKey(
        AppUser,
        on_delete=models.DO_NOTHING,
    )
    invitee_email = models.CharField(
        max_length=MAX_EMAIL_LENGTH,
        null=False,
        blank=False,
    )
    status = models.CharField(max_length=20, choices=(
    ('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')), default='pending')

    class Meta:
        verbose_name_plural = "Family Invitations"
        unique_together = ['family', 'invitee_email']
        ordering = ['-created_at']