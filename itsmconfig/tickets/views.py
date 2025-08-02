from django.shortcuts import render
from .models import Status, Priority, Category, Ticket, TicketComment
from .serializers import StatusSerializer, PrioritySerializer, CategorySerializer, TicketSerializer, TicketCommentSerializer
# api views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from django.utils import timezone



from rest_framework.permissions import BasePermission

class IsAgentOrAdminForWrite(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True  

        return request.user.usermodel.role in ['agent', 'admin']








class StatusListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAgentOrAdminForWrite]


    @swagger_auto_schema(
        operation_description="Get all statuses",
        responses={200: StatusSerializer(many=True)}
    )
    def get(self, request):
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Create a new status",
        request_body=StatusSerializer,
        responses={201: StatusSerializer}
    )
    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatusDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAgentOrAdminForWrite]


    def get_object(self, pk):
        try:
            return Status.objects.get(pk=pk)
        except Status.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Get a status by ID",
        responses={200: StatusSerializer}
    )
    def get(self, request, pk):
        status = self.get_object(pk)
        if status is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StatusSerializer(status)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Update a status",
        request_body=StatusSerializer,
        responses={200: StatusSerializer}
    )
    def put(self, request, pk):
        status = self.get_object(pk)
        if status is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StatusSerializer(status, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete a status",
        responses={204: "No content"}
    )
    def delete(self, request, pk):
        status = self.get_object(pk)
        if status is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PriorityListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAgentOrAdminForWrite]

    @swagger_auto_schema(
        operation_description="Get all priorities",
        responses={200: PrioritySerializer(many=True)}
    )
    def get(self, request):
        priorities = Priority.objects.all()
        serializer = PrioritySerializer(priorities, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Create a new priority",
        request_body=PrioritySerializer,
        responses={201: PrioritySerializer}
    )
    def post(self, request):
        serializer = PrioritySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PriorityDetailAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAgentOrAdminForWrite]


    def get_object(self, pk):
        try:
            return Priority.objects.get(pk=pk)
        except Priority.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Get a priority by ID",
        responses={200: PrioritySerializer}
    )
    def get(self, request, pk):
        priority = self.get_object(pk)
        if priority is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PrioritySerializer(priority)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Update a priority",
        request_body=PrioritySerializer,
        responses={200: PrioritySerializer}
    )
    def put(self, request, pk):
        priority = self.get_object(pk)
        if priority is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PrioritySerializer(priority, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete a priority",
        responses={204: "No content"}
    )
    def delete(self, request, pk):
        priority = self.get_object(pk)
        if priority is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        priority.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CategoryListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAgentOrAdminForWrite]
    
    @swagger_auto_schema(
        operation_description="Get all categories",
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Create a new category",
        request_body=CategorySerializer,
        responses={201: CategorySerializer}
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAgentOrAdminForWrite]
    
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Get a category by ID",
        responses={200: CategorySerializer}
    )
    def get(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Update a category",
        request_body=CategorySerializer,
        responses={200: CategorySerializer}
    )
    def put(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete a category",
        responses={204: "No content"}
    )
    def delete(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




class TicketListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
      operation_description="Get tickets based on user role",
      responses={200: TicketSerializer(many=True)})
    def get(self, request):
      user_role = request.user.usermodel.role

      if user_role == 'admin':
          # Admins see all tickets
          tickets = Ticket.objects.all()
      elif user_role == 'agent':
          # Agents see assigned tickets + unassigned tickets
          tickets = Ticket.objects.filter(
              Q(assigned_to=request.user) | Q(assigned_to__isnull=True)
          )
      else:  # user_role == 'user'
          # End users see only their own tickets
          tickets = Ticket.objects.filter(created_by=request.user)

      serializer = TicketSerializer(tickets, many=True)
      return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Create a new ticket",
        request_body=TicketSerializer,
        responses={201: TicketSerializer}
    )

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, created_at=timezone.now(), updated_at=timezone.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
      try:
          ticket = Ticket.objects.get(pk=pk)
          user_role = user.usermodel.role


          if user_role == 'admin':
              return ticket
          elif user_role == 'agent':
              if ticket.assigned_to == user or ticket.assigned_to is None:
                  return ticket
          else:  
              if ticket.created_by == user:
                  return ticket

          return None  
      except Ticket.DoesNotExist:
          return None


    @swagger_auto_schema(
        operation_description="Get a ticket by ID",
        responses={200: TicketSerializer}
    )
    def get(self, request, pk):
        ticket = self.get_object(pk, request.user)
        if ticket is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Update a ticket",
        request_body=TicketSerializer,
        responses={200: TicketSerializer}
    )
    def put(self, request, pk):
        ticket = self.get_object(pk, request.user)
        if ticket is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete a ticket",
        responses={204: "No content"}
    )
    def delete(self, request, pk):
        ticket = self.get_object(pk, request.user)
        if ticket is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TicketCommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self, request):
        user_role = request.user.usermodel.role
        if user_role == 'admin':
            return TicketComment.objects.all()
        elif user_role == 'agent':
            return TicketComment.objects.filter(Q(ticket__assigned_to=request.user) | Q(ticket__assigned_to__isnull=True))
        else:
            return TicketComment.objects.filter(ticket__created_by=request.user)

    @swagger_auto_schema(
        operation_description="Get all ticket comments",
        responses={200: TicketCommentSerializer(many=True)}
    )
    def get(self, request):
        comments = self.get_queryset(request)
        serializer = TicketCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Create a new ticket comment",
        request_body=TicketCommentSerializer,
        responses={201: TicketCommentSerializer}
    )
    def post(self, request):
        serializer = TicketCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, created_at=timezone.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketCommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, request,pk):
        user_role = request.user.usermodel.role
        try:
            if user_role == 'admin':
                return TicketComment.objects.get(pk=pk)
            elif user_role == 'agent':
                return TicketComment.objects.filter(
                    Q(ticket__assigned_to=request.user) | Q(ticket__assigned_to__isnull=True)
                ).get(pk=pk)
            else:
                return TicketComment.objects.get(pk=pk, ticket__created_by=request.user)
        except TicketComment.DoesNotExist:
            return None
            
    @swagger_auto_schema(
        operation_description="Get a ticket comment by ID",
        responses={200: TicketCommentSerializer}
    )
    def get(self, request, pk):
        comment = self.get_object(request, pk)
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TicketCommentSerializer(comment)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Update a ticket comment",
        request_body=TicketCommentSerializer,
        responses={200: TicketCommentSerializer}
    )
    def put(self, request, pk):
        comment = self.get_object(request, pk)
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TicketCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete a ticket comment",
        responses={204: "No content"}
    )
    def delete(self, request, pk):
        comment = self.get_object(request, pk)
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
