from django.urls import path

from .api_views import UserSubscriptionsAPIView, PurchaseSubscriptionAPIView
from .views import (
    PurchaseSubscriptionView,
    UserCardDetailView,
    CardListView,
    CardDetailView,
    SubscriptionListView,
    SubscriptionUpdateView, SubscriptionAdminCreateView,
)

app_name = 'subscriptions'

urlpatterns = [
    path('profile/', UserCardDetailView.as_view(), name='profile'),
    path('purchase/<int:pk>/', PurchaseSubscriptionView.as_view(), name='purchase'),
    path('admin/cards/', CardListView.as_view(), name='admin_cards'),
    path('admin/cards/<int:pk>/', CardDetailView.as_view(), name='admin_card_detail'),
    path('admin/subscriptions/', SubscriptionListView.as_view(), name='admin_subscriptions'),
    path('admin/subscriptions/<int:pk>/edit/', SubscriptionUpdateView.as_view(), name='admin_subscription_edit'),
    path('api/subscriptions/', UserSubscriptionsAPIView.as_view(), name='api_subscriptions'),
    path('api/purchase/<int:plan_id>/', PurchaseSubscriptionAPIView.as_view(), name='api_purchase'),
    path('admin/subscriptions/add/', SubscriptionAdminCreateView.as_view(), name='admin_subscription_add'),
]
