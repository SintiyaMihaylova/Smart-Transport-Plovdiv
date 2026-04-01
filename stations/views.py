from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from transport.mixins import AdminRequiredMixin
from transport.models import BusLine, Schedule
from .models import Station
from .forms import StationForm
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator



class StationPublicListView(ListView):
    model = Station
    template_name = 'stations/public_station_list.html'
    context_object_name = 'stations'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = Station.objects.active().with_routes().order_by('stop_id')
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(stop_id__icontains=query)
            )
        return qs

@method_decorator(cache_page(60 * 5), name='dispatch')
class StationPublicDetailView(DetailView):
    model = Station
    template_name = 'stations/public_station_detail.html'
    context_object_name = 'station'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lines'] = BusLine.objects.filter(
            routes__stop=self.object,
            is_active=True
        ).distinct().prefetch_related('routes__line')

        return context


class StationAdminListView(AdminRequiredMixin, ListView):
    model = Station
    template_name = 'stations/admin/station_list.html'
    context_object_name = 'stations'
    ordering = ['stop_id']

    def get_queryset(self):
        queryset = Station.objects.prefetch_related('routes__line')
        neighborhood = self.request.GET.get('neighborhood')
        if neighborhood:
            queryset = queryset.filter(neighborhood=neighborhood)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['neighborhoods'] = Station.objects.exclude(
    Q(neighborhood__isnull=True) | Q(neighborhood='')
).values_list('neighborhood', flat=True).distinct().order_by('neighborhood')

        return context


class StationAdminDetailView(AdminRequiredMixin, DetailView):
    model = Station
    template_name = 'stations/admin/station_detail.html'
    context_object_name = 'station'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lines_passing_by'] = BusLine.objects.filter(
            routes__stop=self.object
        ).distinct().prefetch_related('routes__line')
        return context


class StationCreateView(AdminRequiredMixin, CreateView):
    model = Station
    form_class = StationForm
    template_name = 'stations/admin/station_form.html'
    success_url = reverse_lazy('stations:admin_station_list')


class StationUpdateView(AdminRequiredMixin, UpdateView):
    model = Station
    form_class = StationForm
    template_name = 'stations/admin/station_form.html'
    success_url = reverse_lazy('stations:admin_station_list')


class StationDeleteView(AdminRequiredMixin, DeleteView):
    model = Station
    template_name = 'stations/admin/station_confirm_delete.html'
    success_url = reverse_lazy('stations:admin_station_list')

class StationDetailView(DetailView):
    model = Station
    template_name = 'stations/station_detail.html'
    context_object_name = 'station'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station = self.object
        now = timezone.localtime().time()
        current_day = BusLine.get_current_day_type()

        context['upcoming_schedules'] = Schedule.objects.filter(
            stop=station,
            is_active=True,
            day_type=current_day,
            arrival_time__gte=now
        ).select_related('line').order_by('arrival_time')[:10]

        return context

