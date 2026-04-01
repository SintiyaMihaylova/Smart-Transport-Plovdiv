from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import CustomUserCreationForm, EmailAuthenticationForm


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
