from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.utils import timezone

from .emails import send_account_locked_email
from .managers import UserManager


class User(AbstractUser):
    class SecurityQuestions(models.TextChoices):
        MOTHERS_MAIDEN_NAME = ("maiden_name", _("What is your mother's maiden name?"))
        FIRST_PET_NAME = ("first_pet_name", _("What was the name of your first pet?"))
        BIRTH_CITY = ("birth_city", _("In which city were you born?"))

    class AccountStatus(models.TextChoices):
        ACTIVE = ("active", _("Active"))
        LOCKED = ("locked", _("Locked"))
        SUSPENDED = ("suspended", _("Suspended"))

    class RoleChoices(models.TextChoices):
        CUSTOMER = ("customer", _("Customer"))
        ACCOUNT_EXECUTIVE = ("account_executive", _("Account Executive"))
        TELLER = ("teller", _("Teller"))
        BRANCH_MANAGER = ("branch_manager", _("Branch Manager"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_("Username"), max_length=12, unique=True)
    security_question = models.CharField(_("Security Question"), max_length=30, choices=SecurityQuestions.choices)
    security_answer = models.CharField(_("Security Answer"), max_length=30)
    email = models.EmailField(_("Email Address"), unique=True, db_index=True)
    first_name = models.CharField(_("First Name"), max_length=30)
    middle_name = models.CharField(_("Middle Name"), max_length=30, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=30)
    id_no = models.PositiveIntegerField(_("Identification Number"), unique=True)
    account_status = models.CharField(_("Account Status"), max_length=10, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)
    role = models.CharField(_("Role"), max_length=20, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)
    failed_login_attempts = models.PositiveIntegerField(_("Failed Login Attempts"), default=0)
    last_failed_login = models.DateTimeField(_("Last Failed Login"), blank=True, null=True)
    otp = models.CharField(_("OTP"), max_length=6, blank=True, null=True)
    otp_expiry_time = models.DateTimeField(_("OTP Expiry Time"), blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "id_no", "security_question", "security_answer"]

    def set_otp(self, otp: str, expiry_minutes: int = 10):
        """Set OTP and its expiry time."""
        self.otp = otp
        self.otp_expiry_time = timezone.now() + timezone.timedelta(minutes=expiry_minutes)
        self.save(update_fields=['otp', 'otp_expiry_time'])

    def verify_otp(self, otp: str):
        """Verify the provided OTP."""
        if self.otp == otp and self.otp_expiry_time > timezone.now():
            self.otp = None
            self.otp_expiry_time = None
            self.save(update_fields=['otp', 'otp_expiry_time'])
            return True
        return False

    def handle_failed_login_attempts(self):
        """Handle failed login attempts and lock account if necessary."""
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        if self.failed_login_attempts >= settings.LOGIN_ATTEMPTS:
            self.account_status = self.AccountStatus.LOCKED
            send_account_locked_email(self.email)
        self.save()

    def reset_failed_login_attempts(self):
        """Reset failed login attempts counter."""
        self.failed_login_attempts = 0
        self.last_failed_login = None
        self.account_login_status = self.AccountStatus.ACTIVE
        self.save()

    def unlock_account(self):
        """Unlock the user account."""
        self.account_status = self.AccountStatus.ACTIVE
        self.failed_login_attempts = 0
        self.last_failed_login = None
        self.save()

    @property
    def is_locked_out(self) -> bool:
        """Check if the user account is locked."""
        if self.account_status == self.AccountStatus.LOCKED:
            if (self.last_failed_login and
                timezone.now() - self.last_failed_login > timezone.timedelta(minutes=settings.LOCKOUT_DURATION)):
                self.unlock_account()
                return False
            return True
        return False

    @property
    def full_name(self) -> str:
        """Return the user's full name."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}".title().strip()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

    def has_role(self, role: str) -> bool:
        """Check if the user has a specific role."""
        return self.role == role and hasattr(self, 'role')

    def __str__(self) -> str:
        return f"{self.full_name} ({self.get_role_display()})"
