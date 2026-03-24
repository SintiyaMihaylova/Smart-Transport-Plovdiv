from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'role', 'bio', 'profile_picture')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'role', 'bio', 'profile_picture', 'is_active', 'is_staff')


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_('Имейл'),
        widget=forms.EmailInput(attrs={'placeholder': 'email@example.com'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            return username.lower()
        return username

    password = forms.CharField(
        label=_('Парола'),
        widget=forms.PasswordInput
    )
