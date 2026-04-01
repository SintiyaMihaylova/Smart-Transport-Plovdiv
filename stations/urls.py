from django.urls import path
from .views import (
    StationPublicListView,
    StationPublicDetailView,
    StationAdminListView,
    StationCreateView,
    StationUpdateView,
    StationDeleteView,
    StationDetailView
)

app_name = 'stations'

urlpatterns = [
    path('', StationPublicListView.as_view(), name='station_list'),
    path('<int:pk>/', StationPublicDetailView.as_view(), name='station_detail'),

    path('admin/', StationAdminListView.as_view(), name='admin_station_list'),
    path('admin/add/', StationCreateView.as_view(), name='station_create'),
    path('admin/<int:pk>/edit/', StationUpdateView.as_view(), name='station_update'),
    path('admin/<int:pk>/delete/', StationDeleteView.as_view(), name='station_delete'),
path('<int:pk>/', StationDetailView.as_view(), name='station_detail'),
]