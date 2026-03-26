from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    readonly_fields = ('email', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Допълнителна информация'), {'fields': ('role', 'bio', 'profile_picture')}),
        (_('Права и достъп'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'bio', 'profile_picture'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
