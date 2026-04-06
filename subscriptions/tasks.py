from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _

@shared_task
def send_subscription_email_task(user_email, plan_name, end_date_str):
    subject = _('Успешно активиран абонамент')

    message = _(
        f"Здравейте,\n\n"
        f"Вашият абонамент '{plan_name}' беше активиран успешно.\n"
        f"Валиден е до: {end_date_str}\n\n"
        f"Благодарим, че използвате нашата система!"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=True,
    )