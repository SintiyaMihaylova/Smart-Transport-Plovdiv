from django.contrib import admin
from .models import BusLine, Route

class RouteInline(admin.TabularInline):
    model = Route
    extra = 0
    ordering = ('position',)
    fields = ('stop', 'position')

@admin.register(BusLine)
class BusLineAdmin(admin.ModelAdmin):
    list_display = ('number', 'route_bus',)
    search_fields = ('number',)
    inlines = [RouteInline]

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('line', 'position', 'stop',)
    list_editable = ('position',)
    list_filter = ('line',)
    search_fields = ('stop__name',)
    ordering = ('line', 'position')
