from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label=_("Име"), required=False)
    last_name = forms.CharField(label=_("Фамилия"), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            return email.lower()
        return email

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'profile_picture')


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
        widget=forms.PasswordInput()
    )