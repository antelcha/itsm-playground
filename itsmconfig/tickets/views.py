from django.shortcuts import render
from .models import Status, Priority, Category, Ticket, TicketComment
from .serializers import StatusSerializer, PrioritySerializer, CategorySerializer, TicketSerializer, TicketCommentSerializer
# api views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class StatusListAPIView(APIView):
    def get(self, request):
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatusDetailAPIView(APIView):



    def get_object(self, pk):
        try:
            return Status.objects.get(pk=pk)
        except Status.DoesNotExist:
            return None

    def get(self, request, pk):
        status = self.get_object(pk)
        if status is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StatusSerializer(status)
        return Response(serializer.data)
    
    def put(self, request, pk):
        status = self.get_object(pk)
        if status is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StatusSerializer(status, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        status = self.get_object(pk)
        if status is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
