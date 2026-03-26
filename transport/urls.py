from django.urls import path
from .views import (
    BusLineListView,
    BusLineDetailView,
    BusLineCreateView,
    BusLineUpdateView,
    BusLineDeleteView,
)

app_name = 'transport'

urlpatterns = [
    path('lines/', BusLineListView.as_view(), name='line_list'),
    path('lines/<str:number>/', BusLineDetailView.as_view(), name='line_detail'),

    path('admin/lines/', BusLineListView.as_view(), name='admin_line_list'), # За момента ползваме същото вю
    path('admin/lines/add/', BusLineCreateView.as_view(), name='line_create'),
    path('admin/lines/<str:number>/edit/', BusLineUpdateView.as_view(), name='line_update'),
    path('admin/lines/<str:number>/delete/', BusLineDeleteView.as_view(), name='line_delete'),
]