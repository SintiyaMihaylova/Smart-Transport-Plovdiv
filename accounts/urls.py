from django.urls import path
from .views import CustomLoginView, CustomLogoutView, RegisterUserView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
]