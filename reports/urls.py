from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('submit/', views.ReportCreateView.as_view(), name='report_create'),

    path('admin/list/', views.AdminReportListView.as_view(), name='admin_report_list'),
    path('admin/<int:pk>/update/', views.ReportUpdateView.as_view(), name='report_update'),
]