from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

class BusLine(models.Model):
    number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_('Номер на линия')
    )
    route_bus = models.CharField(
        max_length=100,
        verbose_name=_('Име на маршрут')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Описание'),
        help_text=_('Кратка информация за линията')
    )
    stops = models.ManyToManyField(
        'stations.Station',
        through='Route',
        related_name='bus_lines',
        verbose_name=_('Спирки')
    )
    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = _('Линия')
        verbose_name_plural = _('Линии')
        ordering = ['number']

    def __str__(self):
        return f"№{self.number} - {self.route_bus}"

    # def clean(self):
    #     super().clean()
    #     if self.pk and self.routes.count() < 3:
    #         raise ValidationError(_("Линията трябва да има поне 3 спирки."))

    def get_next_position(self):
        last_route = self.routes.order_by('-position').first()
        return (last_route.position + 1) if last_route else 1


class Route(models.Model):
    line = models.ForeignKey(
        BusLine,
        on_delete=models.CASCADE,
        related_name='routes',
        db_index=True,
        verbose_name=_('Линия')
    )
    stop = models.ForeignKey(
        'stations.Station',
        on_delete=models.CASCADE,
        related_name='routes',
        db_index=True,
        verbose_name=_('Спирка')
    )
    position = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message=_('Поредният номер трябва да бъде поне 1.')),
        ],
        verbose_name=_('Пореден номер в маршрута'),
        help_text=_('Позиция на спирката в маршрута (започва от 1)')
    )

    class Meta:
        verbose_name = _('Маршрут')
        verbose_name_plural = _('Маршрути')
        ordering = ['line', 'position']
        constraints = [
            models.CheckConstraint(
                condition=Q(position__gt=0),
                name='route_position_positive'
            ),
            models.UniqueConstraint(
                fields=['line', 'stop'],
                name='unique_stop_per_line'
            ),
            models.UniqueConstraint(
                fields=['line', 'position'],
                name='unique_position_per_line'
            ),
        ]

    def __str__(self):
        return f"{self.line.number} | {self.position}. {self.stop}"

    def save(self, *args, **kwargs):
        if not self.position:
            self.position = self.line.get_next_position()
        self.full_clean()
        super().save(*args, **kwargs)
