from django.contrib import admin

from .models import EmailUser, FailedLoginAttempt


class FailedLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('date', 'username', 'user_exists', 'ip')


admin.site.register(EmailUser)
admin.site.register(FailedLoginAttempt, FailedLoginAttemptAdmin)
