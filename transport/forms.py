from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.utils.translation import gettext_lazy as _
from .models import BusLine, Route


class BusLineForm(forms.ModelForm):
    class Meta:
        model = BusLine
        fields = ['number', 'route_bus', 'description']
        labels = {
            'number': _('Номер на линията'),
            'route_bus': _('Име на маршрута'),
            'description': _('Описание'),
        }
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '4'}),
            'route_bus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тракия А13 - ПУ (нова сграда)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Кратко описание на линията', 'rows': 2}),
        }


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['stop', 'position']
        labels = {
            'stop': _('Спирка'),
            'position': _('Позиция'),
        }
        widgets = {
            'stop': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
        }

class BaseRouteFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()
        active_forms = [
            f for f in self.forms
            if f.is_valid()
            and not (self.can_delete and self._should_delete_form(f))
            and f.cleaned_data.get('stop')
        ]
        if len(active_forms) < 3:
            raise ValidationError(_("Маршрутът трябва да съдържа поне 3 спирки."))

    def save(self, commit=True):
        instances = super().save(commit=False)
        active_instances = [
            form.instance
            for form in self.forms
            if not (self.can_delete and self._should_delete_form(form))
            and form.cleaned_data.get('stop')
        ]
        active_instances.sort(key=lambda x: x.position or 999)
        for index, instance in enumerate(active_instances, start=1):
            instance.position = index
            if commit:
                instance.save()

        return active_instances


UpdateRouteFormSet = inlineformset_factory(
    BusLine,
    Route,
    form=RouteForm,
    formset=BaseRouteFormSet,
    fields=('stop', 'position'),
    extra=1,
    min_num=3,
    validate_min=True,
    can_delete=True,
)
