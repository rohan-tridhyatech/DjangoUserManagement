from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    phone_number = models.CharField(_('Phone Number'), max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(_('Verified'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    reset_token = models.CharField(_('Reset Token'), max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def has_role(self, role_name):
        return self.groups.filter(name=role_name).exists()

    def get_role(self):
        return self.groups.first().name if self.groups.exists() else None