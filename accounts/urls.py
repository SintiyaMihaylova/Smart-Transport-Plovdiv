from django.urls import path
from .views import CustomLoginView, CustomLogoutView, RegisterUserView, UserProfileUpdateView, UserProfileDeleteView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/delete/', UserProfileDeleteView.as_view(), name='profile_delete'),
]