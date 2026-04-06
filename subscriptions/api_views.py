from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import CardSubscription, SubscriptionPlan
from .permissions import IsOwner
from .serializers import CardSubscriptionSerializer, SubscriptionPlanSerializer
from .services import create_subscription
from .tasks import send_subscription_email_task

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

        try:
            subscription = create_subscription(card, plan)

            user_email = request.user.email
            plan_name = plan.name
            end_date_str = subscription.end_date.strftime('%d.%m.%Y')

            send_subscription_email_task.delay(user_email, plan_name, end_date_str)

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

class SubscriptionDetailAPIView(generics.RetrieveAPIView):
    queryset = CardSubscription.objects.all()
    serializer_class = CardSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsOwner]