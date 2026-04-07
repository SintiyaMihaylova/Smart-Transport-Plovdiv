from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import CustomUserCreationForm, EmailAuthenticationForm
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    # Променяме пътя към папката на subscriptions
    template_name = 'subscriptions/profile_edit.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('subscriptions:profile') # Увери се, че това е името на URL-а за профила ти

    def get_object(self, queryset=None):
        return self.request.user

class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'subscriptions/profile_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class CustomLogoutView(LogoutView):
    def get_next_page(self):
        return reverse_lazy('home')


class RegisterUserView(CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def get_success_url(self):
        return reverse_lazy('home')
