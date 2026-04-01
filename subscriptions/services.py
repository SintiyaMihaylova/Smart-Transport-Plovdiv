from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def send_subscription_email(user, plan, end_date):
    subject = _('Успешно активиран абонамент')

    message = _(
        f"Здравейте,\n\n"
        f"Вашият абонамент '{plan.name}' беше активиран успешно.\n"
        f"Валиден е до: {end_date.strftime('%d.%m.%Y')}\n\n"
        f"Благодарим, че използвате нашата система!"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )
