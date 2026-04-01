import uuid
from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SubscriptionPlan(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_('Име на план')
    )

    duration_months = models.PositiveIntegerField(
        verbose_name=_('Продължителност (месеци)')
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name=_('Цена')
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.name} ({self.duration_months} мес.)"


class Card(models.Model):
    user = models.OneToOneField(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='card',
        verbose_name=_('Потребител')
    )

    card_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name=_('Номер на карта')
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name=_('Активна')
    )

    valid_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Валидна до')
    )

    plans = models.ManyToManyField(
        SubscriptionPlan,
        through='CardSubscription',
        related_name='cards',
        verbose_name=_('Абонаменти')
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.card_number:
            self.card_number = str(uuid.uuid4().hex[:10]).upper()

        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        return self.valid_until and self.valid_until > timezone.now()

    @property
    def remaining_days(self):
        if self.valid_until and self.valid_until > timezone.now():
            return (self.valid_until - timezone.now()).days
        return 0

    def __str__(self):
        return f"Карта {self.card_number} ({self.user.email})"


class CardSubscription(models.Model):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE
    )

    purchase_date = models.DateTimeField(auto_now_add=True)

    start_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if self.is_active:
            CardSubscription.objects.filter(
                card=self.card,
                is_active=True
            ).exclude(pk=self.pk).update(is_active=False)

        if not self.start_date:
            if self.card.valid_until and self.card.valid_until > timezone.now():
                self.start_date = self.card.valid_until
            else:
                self.start_date = timezone.now()

        if not self.end_date:
            self.end_date = self.start_date + relativedelta(
                months=self.plan.duration_months
            )

        self.full_clean()

        super().save(*args, **kwargs)

        Card.objects.filter(pk=self.card.pk).update(
            valid_until=self.end_date,
            is_active=True
        )

        if is_new:
            try:
                from .services import send_subscription_email
                send_subscription_email(
                    self.card.user,
                    self.plan,
                    self.end_date
                )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Email error: {e}")

    class Meta:
        ordering = ['-purchase_date']
        verbose_name = _('Абонамент на карта')
        verbose_name_plural = _('Абонаменти на карти')

    def __str__(self):
        return f"{self.card.card_number} - {self.plan.name}"
