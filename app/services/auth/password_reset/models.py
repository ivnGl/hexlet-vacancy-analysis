from django.db import models

from app.services.auth.users.models import User


class PasswordReset(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    token_hash = models.CharField(255, null=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
