from django.shortcuts import render

from tickets.models import Ticket
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.permissions import BasePermission
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from .serializers import DashboardOverviewSerializer, DashboardMetricsSerializer    

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.usermodel.role in ['admin', 'agent']

class DashboardOverviewAPIView(APIView):
      permission_classes = [IsAuthenticated, IsAdmin]

      @swagger_auto_schema(
        operation_description="Get dashboard overview",
        responses={200: DashboardOverviewSerializer(many=True)}
      )
      def get(self, request):
          tickets = Ticket.objects.all()

          total_tickets = tickets.count()
          open_tickets = tickets.filter(status__is_closed=False).count()
          closed_tickets = tickets.filter(status__is_closed=True).count()

          return Response(  {
              'total_tickets': total_tickets,
              'open_tickets': open_tickets,
              'closed_tickets': closed_tickets
          })
      
class DashboardMetricsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Get dashboard metrics",
        responses={200: DashboardMetricsSerializer}
    )
    def get(self, request):
        tickets = Ticket.objects.all()

        status_counts = tickets.values('status__name').annotate(
            count=Count('id')
        ).order_by('status__order')

        priority_counts = tickets.values('priority__name').annotate(
            count=Count('id')
        ).order_by('priority__order')

        category_counts = tickets.values('category__name').annotate(
            count=Count('id')
        ).order_by('category__order')

        return Response({
            'tickets_by_status': list(status_counts),
            'tickets_by_priority': list(priority_counts),
            'tickets_by_category': list(category_counts)
        })
