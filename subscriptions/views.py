from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from accounts.mixins import TravelerRequiredMixin, AdminRequiredMixin, OperatorRequiredMixin
from .models import CardSubscription, Card, SubscriptionPlan


class UserCardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = 'subscriptions/profile.html'
    context_object_name = 'card'

    def get_queryset(self):
        return Card.objects.select_related('user').prefetch_related('subscriptions__plan')

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        card = queryset.filter(user=self.request.user).first()

        if not card:
            return None

        return card

    def render_to_response(self, context, **response_kwargs):
        if self.object is None:
            messages.error(self.request, _("Възникна проблем: Все още нямате създадена карта."))
            return redirect('home')
        return super().render_to_response(context, **response_kwargs)


class PurchaseSubscriptionView(
    LoginRequiredMixin,
    TravelerRequiredMixin,
    SuccessMessageMixin,
    CreateView
):

    model = CardSubscription
    fields = []
    template_name = 'subscriptions/purchase.html'
    success_url = reverse_lazy('subscriptions:profile')
    success_message = _("Абонаментът беше активиран успешно!")

    def dispatch(self, request, *args, **kwargs):
        self.plan = get_object_or_404(SubscriptionPlan, pk=self.kwargs.get('pk'))
        card = getattr(request.user, 'card', None)

        if card and card.is_valid:
            messages.warning(request, _("Вече имате активен абонамент."))
            return redirect('subscriptions:profile')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        card = getattr(self.request.user, 'card', None)

        if not card:
            messages.error(self.request, _("Нямате активна карта."))
            return self.form_invalid(form)

        form.instance.card = card
        form.instance.plan = self.plan

        try:
            form.instance.full_clean()
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(self.request, error)
            else:
                for error in e.messages:
                    messages.error(self.request, error)

            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan'] = self.plan

        card = getattr(self.request.user, 'card', None)

        if card:
            context['subscriptions'] = (
                card.subscriptions
                .select_related('plan')
                .order_by('-purchase_date')
            )
        else:
            context['subscriptions'] = []

        context['all_plans'] = SubscriptionPlan.objects.exclude(pk=self.plan.pk)

        return context


class CardListView(OperatorRequiredMixin, ListView):
    model = Card
    template_name = 'subscriptions/admin/card_list.html'
    context_object_name = 'cards'
    paginate_by = 20

    def get_queryset(self):
        return (
            Card.objects
            .select_related('user')
            .prefetch_related('subscriptions__plan')
            .order_by('-created_at')
        )

class CardDetailView(OperatorRequiredMixin, DetailView):
    model = Card
    template_name = 'subscriptions/admin/card_detail.html'
    context_object_name = 'card'

    def get_queryset(self):
        return Card.objects.select_related('user').prefetch_related('subscriptions__plan')


class SubscriptionListView(OperatorRequiredMixin, ListView):
    model = CardSubscription
    template_name = 'subscriptions/admin/subscription_list.html'
    context_object_name = 'subscriptions'
    paginate_by = 20

    def get_queryset(self):
        return (
            CardSubscription.objects
            .select_related('card__user', 'plan')
            .order_by('-purchase_date')
        )


class SubscriptionUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CardSubscription
    fields = ['is_active']
    template_name = 'subscriptions/admin/subscription_update.html'
    success_url = reverse_lazy('subscriptions:admin_subscriptions')
    success_message = _("Абонаментът беше обновен успешно!")

    def get_queryset(self):
        return CardSubscription.objects.select_related('card__user', 'plan')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        obj = self.object

        if obj and obj.end_date and obj.end_date < timezone.now():
            form.fields['is_active'].disabled = True

        return form

    def form_valid(self, form):

        if self.object.end_date and self.object.end_date < timezone.now():
            messages.error(self.request, _("Не може да редактирате изтекъл абонамент."))
            return self.form_invalid(form)

        try:
            form.instance.full_clean()
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(self.request, error)
            else:
                for error in e.messages:
                    messages.error(self.request, error)

            return self.form_invalid(form)

        return super().form_valid(form)
