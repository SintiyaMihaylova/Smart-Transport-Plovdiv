from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .forms import BusLineForm, RouteForm, UpdateRouteFormSet, BaseRouteFormSet
from .mixins import BusLineWithRoutesMixin, AdminRequiredMixin
from .models import BusLine, Schedule


class BusLineCreateView(AdminRequiredMixin, BusLineWithRoutesMixin, CreateView):
    model = BusLine
    form_class = BusLineForm
    template_name = 'transport/admin/line_form.html'
    success_url = reverse_lazy('transport:line_list')
    route_form = RouteForm
    route_formset_class = UpdateRouteFormSet
    route_base_formset = BaseRouteFormSet


class BusLineUpdateView(AdminRequiredMixin, BusLineWithRoutesMixin, UpdateView):
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


class BusLineDeleteView(AdminRequiredMixin, DeleteView):
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
        return super().get_queryset().filter(is_active=True).prefetch_related('routes__stop')


class BusLineDetailView(DetailView):
    model = BusLine
    template_name = 'transport/line_detail.html'
    context_object_name = 'line'
    slug_field = 'number'
    slug_url_kwarg = 'number'

    def get_queryset(self):
        return BusLine.objects.prefetch_related('routes__stop')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['routes'] = (
            self.object.routes
            .select_related('stop')
            .order_by('position')
        )

        referer = self.request.META.get('HTTP_REFERER')
        context['back_url'] = referer if referer else reverse_lazy('transport:line_list')

        return context


# class NextArrivalView(View):
#     def get(self, request, pk):
#
#         line = get_object_or_404(BusLine, pk=pk)
#
#         stop_id = request.GET.get('stop')
#
#         if not stop_id:
#             return JsonResponse({'error': 'stop is required'}, status=400)
#
#         stop = line.stops.get(pk=stop_id)
#
#         next_arrival = line.get_next_arrival(stop)
#
#         if not next_arrival:
#             return JsonResponse({'message': (_('Няма предстоящи курсове за днес.'))})
#
#         return JsonResponse({
#             'line': line.number,
#             'stop': stop.name,
#             'time': next_arrival.arrival_time.strftime('%H:%M'),
#             'direction': next_arrival.get_direction_display(),
#         })
