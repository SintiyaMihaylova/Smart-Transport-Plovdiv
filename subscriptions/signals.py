from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Card

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_card(sender, instance, created, **kwargs):
    if created:
        Card.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_card(sender, instance, **kwargs):
    if hasattr(instance, 'card'):
        instance.card.save()
