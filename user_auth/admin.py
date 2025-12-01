from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class Admin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "id_no",
        "account_status",
        "role",
        "is_staff",
        "is_active",
    )
    list_filter = ("email", "role", "is_staff", "is_active")
    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": ("username", "email", "password"),
            },
        ),
        (
            _("Personal Information"),
            {
                "fields": ("first_name", "last_name", "id_no", "role"),
            },
        ),
        (
            _("Security Information"),
            {
                "fields": ("security_question", "security_answer"),
            },
        ),
        (
            _("Account Status"),
            {
                "fields": (
                    "account_status",
                    "failed_login_attempts",
                    "last_failed_login",
                ),
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "user_permissions",
                    "groups",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
        (
            _("Important Dates"),
            {
                "fields": ("last_login", "date_joined"),
            },
        ),
    )
    search_fields = ["email", "first_name", "last_name", "username"]
    ordering = ["email"]
