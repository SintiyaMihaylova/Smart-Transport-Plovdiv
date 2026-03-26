from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            return email.lower()
        return email

    class Meta:
        model = CustomUser
        fields = ('email', 'role', 'bio', 'profile_picture')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'role',
            'bio',
            'profile_picture',
            'is_active',
            'is_staff'
        )


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