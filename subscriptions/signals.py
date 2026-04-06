from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import Card, CardSubscription
from .services import update_card
from .tasks import send_subscription_email_task

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_card(sender, instance, created, **kwargs):
    if created:
        Card.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_card(sender, instance, **kwargs):
    if hasattr(instance, 'card'):
        instance.card.save()


@receiver(post_save, sender=CardSubscription)
@receiver(post_delete, sender=CardSubscription)
def sync_card_on_subscription_change(sender, instance, **kwargs):
    update_card(instance.card)


@receiver(post_save, sender=CardSubscription)
def send_subscription_email_signal(sender, instance, created, **kwargs):
    if created:
        user_email = instance.card.user.email
        plan_name = instance.plan.name
        end_date_str = instance.end_date.strftime('%d.%m.%Y')

        send_subscription_email_task.delay(user_email, plan_name, end_date_str)