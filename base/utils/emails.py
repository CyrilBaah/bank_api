from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext as _
from loguru import logger


def send_otp_email(email, otp):
    """Send an OTP email to the specified email address."""
    subject = _("Your One-Time Password  for login")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        "otp": otp,
        "user": {"first_name": "User"},
        "site_name": settings.SITE_NAME,
        "expiry_time": settings.OTP_EXPIRATION,
        "support_email": settings.SUPPORT_EMAIL,
    }
    html_content = render_to_string("emails/otp_email.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
        logger.info(f"OTP email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {e}")


def send_account_lock_email(self):
    """Send an account lock notification email to the specified email address."""
    subject = _("Your Account has been Locked")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        "user": self,
        "site_name": settings.SITE_NAME,
        "lockout_duration": int(settings.LOCKOUT_DURATION.total_seconds() // 60),
        "support_email": settings.SUPPORT_EMAIL,
    }
    html_content = render_to_string("emails/account_locked.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, [email])
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
        logger.info(f"Account lock email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send account lock email to {email}: {e}")
