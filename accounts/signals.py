from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser


ROLE_TO_GROUP = {
    CustomUser.RoleChoices.ADMIN: 'Admins',
    CustomUser.RoleChoices.OPERATOR: 'Operators',
    CustomUser.RoleChoices.TRAVELER: 'Travelers',
}


@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    group_name = ROLE_TO_GROUP.get(instance.role)
    if not group_name:
        return

    group, _ = Group.objects.get_or_create(name=group_name)

    instance.groups.clear()
    instance.groups.add(group)


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name != 'accounts':
        return

    for group_name in ROLE_TO_GROUP.values():
        Group.objects.get_or_create(name=group_name)
