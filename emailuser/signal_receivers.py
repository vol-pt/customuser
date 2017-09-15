from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

from .models import FailedLoginAttempt, EmailUser


@receiver(user_login_failed)
def user_login_failed_receiver(sender, request, credentials, **kwargs):
    failed_attempt = FailedLoginAttempt(ip=request.META['REMOTE_ADDR'], user_exists=False)

    if EmailUser.objects.filter(email=credentials['username']).exists():
        failed_attempt.username = credentials['username']
        failed_attempt.user_exists = True

    failed_attempt.save()
