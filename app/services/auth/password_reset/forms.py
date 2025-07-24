import logging
from django.contrib.auth.forms import PasswordResetForm

logger = logging.getLogger(__name__)


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your email"}
        )
        self.fields["email"].label = "Yuour email"
        self.fields["email"].help_text = (
            "Enter the email address you provided during registration"
        )

    def clean_email(self):
        """
        check if email belongs to user, if user does not exist - "error" instead of email
        """
        email = self.cleaned_data["email"].lower().strip()
        user = self.get_users(email)
        if not user:
            logger.error(f"[{email}]: email does not belong to any user")
            email = "error"

        return email
