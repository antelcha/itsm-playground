from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Status, Priority, Category, Ticket, TicketComment
from .serializers import (
    StatusSerializer,
    PrioritySerializer,
    CategorySerializer,
    TicketSerializer,
    TicketCommentSerializer
)

class IsAgentOrAdminForWrite(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.usermodel.role in ['agent', 'admin']


class BaseListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAgentOrAdminForWrite]
    model = None
    serializer_class = None

    @swagger_auto_schema(operation_description="Get all items", responses={200: serializer_class(many=True)})
    def get(self, request):
        items = self.model.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Create a new item", request_body=serializer_class, responses={201: serializer_class})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAgentOrAdminForWrite]
    model = None
    serializer_class = None

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return None

    @swagger_auto_schema(operation_description="Get an item by ID", responses={200: serializer_class})
    def get(self, request, pk):
        item = self.get_object(pk)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(item)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Update an item", request_body=serializer_class, responses={200: serializer_class})
    def put(self, request, pk):
        item = self.get_object(pk)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete an item", responses={204: "No content"})
    def delete(self, request, pk):
        item = self.get_object(pk)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StatusListAPIView(BaseListCreateAPIView):
    model = Status
    serializer_class = StatusSerializer

class StatusDetailAPIView(BaseDetailAPIView):
    model = Status
    serializer_class = StatusSerializer

class PriorityListAPIView(BaseListCreateAPIView):
    model = Priority
    serializer_class = PrioritySerializer

class PriorityDetailAPIView(BaseDetailAPIView):
    model = Priority
    serializer_class = PrioritySerializer

class CategoryListAPIView(BaseListCreateAPIView):
    model = Category
    serializer_class = CategorySerializer

class CategoryDetailAPIView(BaseDetailAPIView):
    model = Category
    serializer_class = CategorySerializer


class TicketListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Get tickets based on user role", responses={200: TicketSerializer(many=True)})
    def get(self, request):
        user_role = request.user.usermodel.role
        if user_role == 'admin':
            tickets = Ticket.objects.all()
        elif user_role == 'agent':
            tickets = Ticket.objects.filter(Q(assigned_to=request.user) | Q(assigned_to__isnull=True))
        else:
            tickets = Ticket.objects.filter(created_by=request.user)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Create a new ticket", request_body=TicketSerializer, responses={201: TicketSerializer})
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
            role = user.usermodel.role
            if role == 'admin' or \
               (role == 'agent' and (ticket.assigned_to == user or ticket.assigned_to is None)) or \
               (role == 'user' and ticket.created_by == user):
                return ticket
        except Ticket.DoesNotExist:
            return None

    def handle_response(self, serializer_class, obj, request_data=None):
        if request_data:
            serializer = serializer_class(obj, data=request_data)
        else:
            serializer = serializer_class(obj)
        if request_data and not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request_data:
            serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Get a ticket by ID", responses={200: TicketSerializer})
    def get(self, request, pk):
        ticket = self.get_object(pk, request.user)
        if ticket is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self.handle_response(TicketSerializer, ticket)

    @swagger_auto_schema(operation_description="Update a ticket", request_body=TicketSerializer, responses={200: TicketSerializer})
    def put(self, request, pk):
        ticket = self.get_object(pk, request.user)
        if ticket is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self.handle_response(TicketSerializer, ticket, request.data)

    @swagger_auto_schema(operation_description="Delete a ticket", responses={204: "No content"})
    def delete(self, request, pk):
        ticket = self.get_object(pk, request.user)
        if ticket is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TicketCommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        role = request.user.usermodel.role
        if role == 'admin':
            return TicketComment.objects.all()
        elif role == 'agent':
            return TicketComment.objects.filter(Q(ticket__assigned_to=request.user) | Q(ticket__assigned_to__isnull=True))
        return TicketComment.objects.filter(ticket__created_by=request.user)

    @swagger_auto_schema(operation_description="Get all ticket comments", responses={200: TicketCommentSerializer(many=True)})
    def get(self, request):
        comments = self.get_queryset(request)
        serializer = TicketCommentSerializer(comments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Create a new ticket comment", request_body=TicketCommentSerializer, responses={201: TicketCommentSerializer})
    def post(self, request):
        serializer = TicketCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, created_at=timezone.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketCommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        role = request.user.usermodel.role
        try:
            if role == 'admin':
                return TicketComment.objects.get(pk=pk)
            elif role == 'agent':
                return TicketComment.objects.filter(Q(ticket__assigned_to=request.user) | Q(ticket__assigned_to__isnull=True)).get(pk=pk)
            return TicketComment.objects.get(pk=pk, ticket__created_by=request.user)
        except TicketComment.DoesNotExist:
            return None

    def handle_response(self, serializer_class, obj, request_data=None):
        if request_data:
            serializer = serializer_class(obj, data=request_data)
        else:
            serializer = serializer_class(obj)
        if request_data and not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request_data:
            serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Get a ticket comment by ID", responses={200: TicketCommentSerializer})
    def get(self, request, pk):
        comment = self.get_object(request, pk)
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self.handle_response(TicketCommentSerializer, comment)

    @swagger_auto_schema(operation_description="Update a ticket comment", request_body=TicketCommentSerializer, responses={200: TicketCommentSerializer})
    def put(self, request, pk):
        comment = self.get_object(request, pk)
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self.handle_response(TicketCommentSerializer, comment, request.data)

    @swagger_auto_schema(operation_description="Delete a ticket comment", responses={204: "No content"})
    def delete(self, request, pk):
        comment = self.get_object(request, pk)
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)