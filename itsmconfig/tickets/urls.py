from django.urls import path

from .views import StatusDetailAPIView, StatusListAPIView


urlpatterns = [
    path('statuses/', StatusListAPIView.as_view(), name='status-list'),
    path('statuses/<int:pk>/', StatusDetailAPIView.as_view(), name='status-detail'),
]