from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class CuratorOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_curator

    def handle_no_permission(self):
        # Autenticato senza permesso -> 403; anonimo -> login.
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return super().handle_no_permission()
