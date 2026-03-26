from django.db import transaction
from django.forms import inlineformset_factory
from .models import BusLine, Route
from .forms import RouteForm, BaseRouteFormSet, UpdateRouteFormSet
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _


class BusLineWithRoutesMixin:
    route_form = RouteForm
    route_formset_class = UpdateRouteFormSet
    route_base_formset = BaseRouteFormSet

    def get_route_formset(self):
        if self.request.method == "POST":
            return self.route_formset_class(self.request.POST, instance=self.object)
        stops_count = 3
        if self.object:
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
        if 'routes' not in context:
            context['routes'] = self.get_route_formset()
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


class StaffRequiredMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff_member

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(_("Нямате права за тази операция."))
        return super().handle_no_permission()

