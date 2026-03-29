from django import forms
from .models import Station
from django.utils.translation import gettext_lazy as _


class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'stop_id', 'neighborhood', 'address', 'latitude', 'longitude', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        return self.cleaned_data['name'].strip()

    def clean_stop_id(self):
        stop_id = self.cleaned_data.get('stop_id')
        if stop_id and not stop_id.isdigit():
            raise forms.ValidationError(_("Номерът трябва да съдържа само цифри."))
        return stop_id

    def clean(self):
        cleaned_data = super().clean()

        lat = cleaned_data.get('latitude')
        lon = cleaned_data.get('longitude')

        if lat is not None and not (-90 <= lat <= 90):
            self.add_error('latitude', _("Ширината трябва да е между -90 и 90."))

        if lon is not None and not (-180 <= lon <= 180):
            self.add_error('longitude', _("Дължината трябва да е между -180 и 180."))

        return cleaned_data

