from django import forms
from .models import Report
from django.utils.translation import gettext_lazy as _

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reporter_name', 'category', 'bus_line', 'stop', 'description']
        widgets = {
            'reporter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Вашето име')}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'bus_line': forms.Select(attrs={'class': 'form-select'}),
            'stop': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Опишете проблема подробно...')}),
        }
        help_texts = {
            'bus_line': _('Изберете линия, ако проблемът е свързан с конкретен автобус.'),
            'stop': _('Изберете спирка, ако проблемът е свързан с нея.'),
        }


class ReportStatusForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select fw-bold border-primary'})
        }
        labels = {
            'status': _('Статус на сигнала')
        }