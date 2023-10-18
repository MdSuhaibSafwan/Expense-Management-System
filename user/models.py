import pyotp
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.apps import apps
from lib.models import create_hex_token, BaseModel


class UserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given  email, and password.
        """
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email
    
    def get_user_type(self):
        return None

    @property
    def is_author(self):
        return self.has_perm("account.add_fundtransfer")

    @property
    def is_checker(self):
        return self.has_perm("account.add_fundcheck")

    @property
    def is_maker(self):
        return self.has_perm("account.add_fundapprove")

    @property
    def is_approver(self):
        return self.has_perm("account.add_fundapprove")

    def has_2fa_token(self):
        return self.auth_tokens_2fa.exists()


class User2FAAuthManager(models.Manager):

    def get_latest_token_for_user(self, user):
        token_obj = user.auth_tokens_2fa.first()
        return token_obj


class User2FAAuth(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=create_hex_token)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="auth_tokens_2fa")
    token = models.CharField(max_length=255, default=pyotp.random_base32)

    objects = User2FAAuthManager()

    class Meta:
        ordering = ["-date_created", ]
        unique_together = [["user", "token"], ]
        verbose_name_plural = "User 2Factor Auth"
