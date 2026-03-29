from django.contrib import admin

from reports.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('category', 'bus_line', 'stop', 'created_at')
    list_filter = ('category', 'status')
    search_fields = ('description',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
