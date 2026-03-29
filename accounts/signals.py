from django.db.models.signals import post_save
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

    role_groups = ROLE_TO_GROUP.values()
    current_role_groups = instance.groups.filter(name__in=role_groups)

    if current_role_groups.count() == 1 and current_role_groups.first().name == group_name:
        return

    instance.groups.remove(*current_role_groups)
    instance.groups.add(group)
