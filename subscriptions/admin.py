from django.contrib import admin
from django.utils import timezone
from .models import Card, CardSubscription, SubscriptionPlan
from django.utils.translation import gettext_lazy as _


class CardSubscriptionInline(admin.TabularInline):
    model = CardSubscription
    extra = 0

    readonly_fields = (
        'plan',
        'purchase_date',
        'start_date',
        'end_date',
        'is_active',
    )

    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        'card_number',
        'user',
        'is_active',
        'valid_until',
        'get_remaining_time',
        'created_at'
    )

    readonly_fields = (
        'card_number',
        'created_at',
        'valid_until',
    )

    search_fields = (
        'card_number',
        'user__email',
    )

    list_filter = (
        'is_active',
    )

    list_select_related = (
        'user',
    )

    inlines = [CardSubscriptionInline]

    fieldsets = (
        (None, {
            'fields': (
                'user',
                'card_number',
                'is_active',
                'valid_until',
            )
        }),
        (_('System info'), {
            'fields': ('created_at',),
        }),
    )

    @admin.display(description=_("Оставащо време"))
    def get_remaining_time(self, obj):
        if obj.valid_until:
            now = timezone.now()
            if obj.valid_until < now:
                return _("Изтекла")
            diff = obj.valid_until - now
            days = diff.days
            return f"{days} {str(_('дни'))}"
        return "N/A"


@admin.register(CardSubscription)
class CardSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'card',
        'plan',
        'is_active',
        'start_date',
        'end_date',
        'purchase_date',
    )

    readonly_fields = (
        'purchase_date',
        'start_date',
        'end_date',
    )

    list_filter = (
        'is_active',
        'plan',
        'purchase_date',
    )

    search_fields = (
        'card__card_number',
        'card__user__email',
        'plan__name',
    )

    ordering = ('-purchase_date',)

    list_select_related = (
        'card',
        'plan',
    )


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'duration_months',
        'price',
    )

    search_fields = ('name',)
