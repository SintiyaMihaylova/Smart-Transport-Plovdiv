from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .forms import BusLineForm, RouteForm, UpdateRouteFormSet, BaseRouteFormSet
from .mixins import BusLineWithRoutesMixin, StaffRequiredMixin
from .models import BusLine


class BusLineCreateView(StaffRequiredMixin, BusLineWithRoutesMixin, CreateView):
    model = BusLine
    form_class = BusLineForm
    template_name = 'transport/admin/line_form.html'
    success_url = reverse_lazy('transport:line_list')
    route_form = RouteForm
    route_formset_class = UpdateRouteFormSet
    route_base_formset = BaseRouteFormSet


class BusLineUpdateView(StaffRequiredMixin, BusLineWithRoutesMixin, UpdateView):
    model = BusLine
    form_class = BusLineForm
    template_name = 'transport/admin/line_form.html'
    slug_field = 'number'
    slug_url_kwarg = 'number'
    success_url = reverse_lazy('transport:line_list')
    route_formset_class = UpdateRouteFormSet

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['number'].disabled = True
        return form


class BusLineDeleteView(StaffRequiredMixin, DeleteView):
    model = BusLine
    template_name = 'transport/admin/line_delete.html'
    slug_field = 'number'
    slug_url_kwarg = 'number'
    success_url = reverse_lazy('transport:line_list')


class BusLineListView(ListView):
    model = BusLine
    template_name = 'transport/line_list.html'
    context_object_name = 'lines'
    ordering = ['number']

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BusLineDetailView(DetailView):
    model = BusLine
    template_name = 'transport/line_detail.html'
    context_object_name = 'line'
    slug_field = 'number'
    slug_url_kwarg = 'number'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = self.object.routes.select_related('stop').order_by('position')
        referer = self.request.META.get('HTTP_REFERER')
        context['back_url'] = referer if referer else reverse_lazy('transport:line_list')
        return context
