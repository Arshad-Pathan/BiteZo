"""Restrict the Django administration site to active superusers."""

from types import MethodType

from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.core.exceptions import ValidationError


class SuperuserAdminAuthenticationForm(AdminAuthenticationForm):
    """Reject staff accounts that are not superusers at the admin login."""

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_superuser:
            raise ValidationError(
                "This administration area is restricted to superusers.",
                code="not_superuser",
            )


def superuser_admin_permission(self, request):
    return request.user.is_active and request.user.is_superuser


admin.site.login_form = SuperuserAdminAuthenticationForm
admin.site.has_permission = MethodType(superuser_admin_permission, admin.site)
admin.site.site_header = "Private Administration"
admin.site.site_title = "Private Administration"
admin.site.index_title = "Secure Management Area"
