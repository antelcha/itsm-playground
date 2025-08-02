from django.urls import path

from .views import UserListAPIView, UserProfileAPIView, UserRegistrationAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('list/', UserListAPIView.as_view(), name='user-list'),

]