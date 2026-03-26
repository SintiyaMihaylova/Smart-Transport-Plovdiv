from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from transport.mixins import StaffRequiredMixin
from transport.models import BusLine
from .models import Station
from .forms import StationForm

class StationPublicListView(ListView):
    model = Station
    template_name = 'stations/public_station_list.html'
    context_object_name = 'stations'

    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = Station.active()
        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(stop_id__icontains=query))
        return qs


class StationPublicDetailView(DetailView):
    model = Station
    template_name = 'stations/public_station_detail.html'
    context_object_name = 'station'

    def get_queryset(self):
        return Station.active()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lines_passing_by'] = BusLine.objects.filter(
            routes__stop=self.object,
            is_active=True
        ).distinct()
        return context


class StationAdminListView(StaffRequiredMixin, ListView):
    model = Station
    template_name = 'stations/admin/station_list.html'
    context_object_name = 'stations'
    ordering = ['stop_id']

    def get_queryset(self):
        queryset = Station.objects.prefetch_related('routes__line').all()
        neighborhood = self.request.GET.get('neighborhood')
        if neighborhood:
            queryset = queryset.filter(neighborhood=neighborhood)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['neighborhoods'] = Station.objects.values_list('neighborhood', flat=True).distinct().order_by('neighborhood')
        return context


class StationAdminDetailView(StaffRequiredMixin, DetailView):
    model = Station
    template_name = 'stations/admin/station_detail.html'
    context_object_name = 'station'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lines_passing_by'] = BusLine.objects.filter(
            routes__stop=self.object
        ).distinct()
        return context


class StationCreateView(StaffRequiredMixin, CreateView):
    model = Station
    form_class = StationForm
    template_name = 'stations/admin/station_form.html'
    success_url = reverse_lazy('stations:admin_station_list')


class StationUpdateView(StaffRequiredMixin, UpdateView):
    model = Station
    form_class = StationForm
    template_name = 'stations/admin/station_form.html'
    success_url = reverse_lazy('stations:admin_station_list')


class StationDeleteView(StaffRequiredMixin, DeleteView):
    model = Station
    template_name = 'stations/admin/station_confirm_delete.html'
    success_url = reverse_lazy('stations:admin_station_list')
