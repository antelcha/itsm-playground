from django.urls import path

from .views import (CategoryDetailAPIView, CategoryListAPIView,
                     PriorityDetailAPIView, PriorityListAPIView, 
                     StatusDetailAPIView, StatusListAPIView, 
                     TicketCommentDetailAPIView, TicketCommentListAPIView, 
                     TicketDetailAPIView, TicketListAPIView)



urlpatterns = [
    path('statuses/', StatusListAPIView.as_view(), name='status-list'),
    path('statuses/<int:pk>/', StatusDetailAPIView.as_view(), name='status-detail'),
    path('priorities/', PriorityListAPIView.as_view(), name='priority-list'),
    path('priorities/<int:pk>/', PriorityDetailAPIView.as_view(), name='priority-detail'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('tickets/', TicketListAPIView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetailAPIView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/comments/', TicketCommentListAPIView.as_view(), name='ticket-comment-list'),
    path('tickets/<int:pk>/comments/<int:comment_pk>/', TicketCommentDetailAPIView.as_view(), name='ticket-comment-detail'),
]