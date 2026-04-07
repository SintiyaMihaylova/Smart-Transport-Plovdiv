from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from subscriptions.models import CardSubscription, SubscriptionPlan

User = get_user_model()


class SubscriptionTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='pass1234'
        )

        # ✅ ВЗИМАМЕ картата от signal (НЕ я създаваме!)
        self.card = self.user.card

        self.plan = SubscriptionPlan.objects.create(
            name='Monthly',
            duration_months=1,
            price=10
        )

    def test_create_subscription(self):
        sub = CardSubscription.objects.create(
            card=self.card,
            plan=self.plan
        )

        self.assertEqual(sub.card, self.card)
        self.assertEqual(sub.plan, self.plan)
        self.assertTrue(sub.is_active)

    def test_subscription_dates_are_set(self):
        sub = CardSubscription.objects.create(
            card=self.card,
            plan=self.plan
        )

        self.assertIsNotNone(sub.start_date)
        self.assertIsNotNone(sub.end_date)

    def test_subscription_str(self):
        sub = CardSubscription.objects.create(
            card=self.card,
            plan=self.plan
        )

        self.assertIn(self.plan.name, str(sub))

    def test_active_and_inactive_subscription_filtering(self):
        CardSubscription.objects.create(card=self.card, plan=self.plan, is_active=True)
        CardSubscription.objects.create(card=self.card, plan=self.plan, is_active=False)

        active_count = CardSubscription.objects.filter(card=self.card, is_active=True).count()
        total_count = CardSubscription.objects.filter(card=self.card).count()

        self.assertEqual(active_count, 1)
        self.assertEqual(total_count, 2)