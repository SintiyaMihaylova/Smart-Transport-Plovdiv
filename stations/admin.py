from django.contrib import admin
from .models import Station
from django.utils.translation import gettext_lazy as _

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):

    list_display = ('stop_id', 'name', 'neighborhood', 'is_active', 'has_coordinates')
    list_editable = ('is_active',)
    search_fields = ('name', 'stop_id', 'address')
    list_filter = ('is_active', 'neighborhood')
    ordering = ('stop_id', 'name')

    fieldsets = (
        (_('Основна информация'), {
            'fields': ('name', 'stop_id', 'is_active')
        }),
        (_('Локация'), {
            'fields': ('neighborhood', 'address'),
        }),
        (_('Географски данни (Смарт)'), {
            'fields': ('latitude', 'longitude', 'has_coordinates'),
            'description': _('Координати за GPS проследяване и карти'),
        }),
    )

    readonly_fields = ('has_coordinates',)

    def has_coordinates(self, obj):
        return obj.latitude is not None and obj.longitude is not None
    has_coordinates.boolean = True
    has_coordinates.short_description = _('Координати?')

