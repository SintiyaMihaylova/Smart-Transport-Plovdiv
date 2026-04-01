from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import AccessMixin
from django.utils.translation import gettext_lazy as _


class RoleRequiredMixin(AccessMixin):
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return self.handle_no_permission()

        if not self._has_role(user):
            raise PermissionDenied(_("Нямате необходимата роля за достъп."))
        return super().dispatch(request, *args, **kwargs)

    def _has_role(self, user):
        return any(
            getattr(user, f"is_{role.lower()}", False)
            for role in self.allowed_roles
        )

class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['ADMIN']


class OperatorRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['OPERATOR', 'ADMIN']


class TravelerRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['TRAVELER']
