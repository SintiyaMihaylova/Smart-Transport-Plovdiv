from rest_framework import serializers
from .models import CardSubscription, SubscriptionPlan


class CardSubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    user_email = serializers.CharField(source='card.user.email', read_only=True)

    class Meta:
        model = CardSubscription
        fields = [
            'id',
            'plan',
            'plan_name',
            'user_email',
            'start_date',
            'end_date',
            'is_active',
        ]
        read_only_fields = ['start_date', 'end_date', 'is_active']

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'duration_months', 'price']
