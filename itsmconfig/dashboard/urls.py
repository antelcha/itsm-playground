from django.urls import path
from .views import DashboardOverviewAPIView, DashboardMetricsAPIView

urlpatterns = [
    path('overview/', DashboardOverviewAPIView.as_view(), name='dashboard-overview'),
    path('metrics/', DashboardMetricsAPIView.as_view(), name='dashboard-metrics'),
    
]  