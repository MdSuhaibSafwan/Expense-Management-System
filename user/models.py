from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _


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
    is_author = models.BooleanField(
        _("author status"),
        default=False,
        help_text=_("Designates whether the user can add an expense."),
    )
    is_checker = models.BooleanField(
        _("checker status"),
        default=False,
        help_text=_("Designates whether the user can approve an expense"),
    )
    is_maker = models.BooleanField(
        _("maker status"),
        default=False,
        help_text=_("Designates whether the user can complete an expense."),
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
        if self.is_author:
            return "author"
        
        if self.is_checker:
            return "checker"
        
        if self.is_maker:
            return "maker"
        
        return None

    @property
    def user_type(self):
        return self.get_user_type()