from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import CardSubscription, SubscriptionPlan
from .serializers import CardSubscriptionSerializer, SubscriptionPlanSerializer



class UserSubscriptionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        card = getattr(request.user, 'card', None)

        if not card:
            return Response(
                {"detail": "Нямате карта."},
                status=status.HTTP_404_NOT_FOUND
            )

        subscriptions = (
            card.subscriptions
            .select_related('plan')
            .order_by('-purchase_date')
        )

        serializer = CardSubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)


class PurchaseSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, plan_id):
        card = getattr(request.user, 'card', None)

        if not card:
            return Response(
                {"detail": "Нямате карта."},
                status=status.HTTP_404_NOT_FOUND
            )

        if card.is_valid:
            return Response(
                {"detail": "Вече имате активен абонамент."},
                status=status.HTTP_400_BAD_REQUEST
            )

        plan = get_object_or_404(SubscriptionPlan, pk=plan_id)

        subscription = CardSubscription(card=card, plan=plan)

        try:
            subscription.full_clean()
            subscription.save()
        except ValidationError as e:
            return Response(
                {"detail": e.message_dict if hasattr(e, 'message_dict') else e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CardSubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SubscriptionPlanListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = SubscriptionPlan.objects.filter(is_active=True)
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response(serializer.data)
