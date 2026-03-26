from django.db import models
from django.utils.translation import gettext_lazy as _


class Station(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Име на спирка')
    )
    stop_id = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_('Номер на спирка'),
        help_text=_('Официален идентификатор на спирката')
    )
    neighborhood = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('Квартал')
    )
    address = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Адрес/Ориентир')
    )

    is_active = models.BooleanField(
        default=True
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name=_('Ширина (latitude)'),
        help_text=_('Географска ширина на спирката')
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name=_('Дължина (longitude)'),
        help_text=_('Географска дължина на спирката')
    )

    def __str__(self):
        return f'{self.name}-{self.stop_id}'

    class Meta:
        verbose_name = _('Спирка')
        verbose_name_plural = _('Спирки')
        ordering = ['stop_id', 'name']

    @classmethod
    def active(cls):
        return cls.objects.filter(is_active=True)