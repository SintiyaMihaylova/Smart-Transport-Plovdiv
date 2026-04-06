from django.db import transaction
from subscriptions.models import CardSubscription, Card


# def send_subscription_email(user, plan, end_date):
#     subject = _('Успешно активиран абонамент')
#
#     message = _(
#         f"Здравейте,\n\n"
#         f"Вашият абонамент '{plan.name}' беше активиран успешно.\n"
#         f"Валиден е до: {end_date.strftime('%d.%m.%Y')}\n\n"
#         f"Благодарим, че използвате нашата система!"
#     )
#
#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [user.email],
#         fail_silently=True,
#     )

def create_subscription(card, plan, is_active=True):
    with transaction.atomic():
        if is_active:
            CardSubscription.objects.filter(
                card=card,
                is_active=True
            ).update(is_active=False)

        subscription = CardSubscription(
            card=card,
            plan=plan,
            is_active=is_active
        )
        subscription.save()

        update_card(card)

        return subscription

def update_card(card):
    active_sub = CardSubscription.objects.filter(
        card=card,
        is_active=True
    ).order_by('-end_date').first()

    if active_sub:
        Card.objects.filter(pk=card.pk).update(
            valid_until=active_sub.end_date,
            is_active=True
        )
    else:
        Card.objects.filter(pk=card.pk).update(
            valid_until=None,
            is_active=False
        )
