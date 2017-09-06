from django.contrib import admin

from .models import CustomUser, FailedLoginAttempt


class FailedLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('date', 'username', 'user_exists', 'ip')


admin.site.register(CustomUser)
admin.site.register(FailedLoginAttempt, FailedLoginAttemptAdmin)
