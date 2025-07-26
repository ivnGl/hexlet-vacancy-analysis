import logging
from datetime import datetime, timedelta

from django.contrib.auth.views import (
    PasswordResetView,
)
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from app.services.auth.users.models import User

from . import configs
from .forms import CustomPasswordResetForm
from .models import PasswordReset

logger = logging.getLogger(__name__)


class CustomPasswordResetView(PasswordResetView):
    subject_template_name = "шаблон_тема_письма.txt"
    email_template_name = "шаблон_тело_письма.html"
    template_name = "шаблон_отображения_формы_сброса_пароля.html"
    form_class = CustomPasswordResetForm
    from_email = "test@test.com"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)
            if user:
                token_hash = self.token_generator.make_token(user)
                current_time = datetime.now()
                time_out = timedelta(configs.PASSWORD_RESET_TIMEOUT)
                expires_at = current_time + time_out
                reset_url = request.build_absolute_uri(
                    reverse("password_reset_validate") + f"?token={token_hash}"
                )
                self.send_reset_email(email, reset_url)
                PasswordReset.objects.create(
                    user_id=user.id,
                    token_hash=token_hash,
                    expires_at=expires_at,
                )
            else:
                logger.error(f"[{email}]: email does not belong to any user")
            return HttpResponse(status=200)
        return render(request, self.template_name, {"form": form})

    def send_reset_email(self, email, reset_url):
        subject = render_to_string(self.subject_template_name, {})
        html_message = render_to_string(
            self.email_template_name,
            {
                "reset_url": reset_url,
            },
        )
        plain_message = strip_tags(html_message)
        max_retries = configs.MAX_RETRIES
        for attempt in range(max_retries):
            try:
                send_mail(
                    subject=subject,
                    message=plain_message,
                    html_message=html_message,
                    from_email=self.from_email,
                    recipient_list=[email],
                    fail_silently=False,
                )
                logger.info(f"Password reset email sent to {email}")
                break
            except Exception as e:
                logger.warning(
                    f"Attempt {attempt + 1} failed to send password "
                    f"reset email to {email}: {str(e)}"
                )
                if attempt == max_retries - 1:
                    logger.error(
                        f"Failed to send password reset email to {email} "
                        f"after {max_retries} attempts"
                    )
