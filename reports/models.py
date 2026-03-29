from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import SET_NULL
from django.utils.translation import gettext_lazy as _

class Report(models.Model):

    class CategoryChoices(models.TextChoices):
        DELAY = 'delay', _('Закъснение')
        SKIPPED = 'skipped', _('Пропуснат курс')
        STATION = 'station', _('Проблем със спирка')
        BEHAVIOR = 'behavior', _('Грубо отношение')
        REPAIR = 'repair', _('Повреда/Ремонт')
        OTHER = 'other', _('Друго')

    class StatusChoices(models.TextChoices):
        NEW = 'new', _('Нов')
        IN_PROGRESS = 'in_progress', _('В процес на обработка')
        RESOLVED = 'resolved', _('Решен')
        REJECTED = 'rejected', _('Отхвърлен')

    reporter_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('Подаден от')
    )
    category = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices,
        default=CategoryChoices.OTHER,
        verbose_name=_('Категория')
    )
    description = models.TextField(
        verbose_name=_('Описание на проблема')
    )
    bus_line = models.ForeignKey(
        'transport.BusLine',
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name='reports',
        verbose_name=_('Линия')
    )
    stop = models.ForeignKey(
        'stations.Station',
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name='reports',
        verbose_name=_('Спирка')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата на създаване'),
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
        verbose_name=_('Статус')
    )

    class Meta:
        verbose_name = _('Сигнал')
        verbose_name_plural = _('Сигнали')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    def __str__(self):
        return f"{self.get_category_display()} - {self.created_at:%d.%m.%Y %H:%M}"

    def clean(self):
        super().clean()

        if not self.bus_line and not self.stop:
            raise ValidationError({
        'bus_line': _('Моля, попълнете поне Линия или Спирка.'),
        'stop': _('Моля, попълнете поне Линия или Спирка.')
    })

        if self.category == self.CategoryChoices.STATION and not self.stop:
            raise ValidationError({
                'stop': _('При проблем със спирка е задължително да изберете спирка.')
            })

        if self.category in (
                self.CategoryChoices.DELAY,
                self.CategoryChoices.SKIPPED
        ) and not self.bus_line:
            raise ValidationError(
                _('При проблеми по маршрута е задължително да въведете номер на линията.')
            )

        if self.bus_line and self.stop:
            if not self.bus_line.stops.filter(pk=self.stop.pk).exists():
                raise ValidationError({
                    'bus_line': _('Избраната спирка не принадлежи към маршрута на тази линия.')
                })
