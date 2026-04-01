from django import forms
from django.db.models import Q
from django.views.generic import ListView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from transport.mixins import OperatorRequiredMixin
from .forms import ReportForm, ReportStatusForm
from .models import Report


class ReportCreateView(SuccessMessageMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/report_form.html'
    success_url = reverse_lazy('reports:report_create')
    success_message = _("Вашият сигнал беше изпратен успешно! Благодарим ви.")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            if not form.cleaned_data.get('reporter_name'):
                name = self.request.user.get_full_name()
                form.instance.reporter_name = name if name else self.request.user.email

        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.is_authenticated:
            form.fields['reporter_name'].widget = forms.HiddenInput()
            form.fields['reporter_name'].required = False

        return form

class AdminReportListView(OperatorRequiredMixin, ListView):
    model = Report
    template_name = 'reports/admin_report_list.html'
    context_object_name = 'reports'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        date_query = self.request.GET.get('date')
        status = self.request.GET.get('status')
        category = self.request.GET.get('category')
        search_query = self.request.GET.get('search')

        if date_query:
            queryset = queryset.filter(created_at__date=date_query)
        if status:
            queryset = queryset.filter(status=status)
        if category:
            queryset = queryset.filter(category=category)
        if search_query:
            queryset = queryset.filter(
                Q(description__icontains=search_query) |
                Q(reporter_name__icontains=search_query)|
        Q(user__email__icontains=search_query)
            )
        return queryset.select_related('bus_line', 'stop', 'user').order_by('-created_at')


class ReportUpdateView(OperatorRequiredMixin, UpdateView):
    model = Report
    form_class = ReportStatusForm
    template_name = 'reports/report_update.html'
    success_url = reverse_lazy('reports:admin_report_list')
    success_message = _("Сигналът беше обновен успешно!")