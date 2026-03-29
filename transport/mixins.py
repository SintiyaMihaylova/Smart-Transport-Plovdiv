from django.db import transaction
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

from .models import BusLine, Route
from .forms import RouteForm, BaseRouteFormSet, UpdateRouteFormSet


class BusLineWithRoutesMixin:
    route_form = RouteForm
    route_formset_class = UpdateRouteFormSet
    route_base_formset = BaseRouteFormSet

    def get_route_formset(self):

        if self.request.method == "POST":
            return self.route_formset_class(
                self.request.POST,
                instance=self.object
            )

        stops_count = 3

        if self.object is not None:
            stops_count = max(3, self.object.routes.count())

        DynamicFormSet = inlineformset_factory(
            BusLine,
            Route,
            form=self.route_form,
            formset=self.route_base_formset,
            extra=stops_count,
            can_delete=True
        )

        return DynamicFormSet(instance=self.object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = context.get('routes') or self.get_route_formset()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        routes = context['routes']

        if not routes.is_valid():
            return self.form_invalid(form)

        with transaction.atomic():
            self.object = form.save()
            routes.instance = self.object
            routes.save()

        return super().form_valid(form)


class AdminRequiredMixin(UserPassesTestMixin):

    raise_exception = True

    def test_func(self):
        user = self.request.user

        return user.is_authenticated and user.is_admin


    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(_("Нямате права за тази операция."))

        return super().handle_no_permission()

class OperatorRequiredMixin(UserPassesTestMixin):

    raise_exception = True

    def test_func(self):
        user = self.request.user

        return (
            user.is_authenticated and
            (user.is_operator or user.is_admin)
        )

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(
                _("Нямате необходимите права за достъп до тази страница.")
            )

        return super().handle_no_permission()
