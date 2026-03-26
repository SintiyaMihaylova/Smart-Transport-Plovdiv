from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == CustomUser.RoleChoices.STAFF:
            group_name = 'Staff'
        else:
            group_name = 'Passenger'

        group, _ = Group.objects.get_or_create(name=group_name)
        if not instance.groups.filter(name=group_name).exists():
            instance.groups.add(group)

