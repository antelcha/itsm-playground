from rest_framework import serializers
from .models import Status, Priority, Category, Ticket, TicketComment


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
      class Meta:
          model = Ticket
          fields = '__all__'
          read_only_fields = ['created_by', 'created_at', 'updated_at']

      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          request = self.context.get('request')

          if request and request.user.usermodel.role == 'user':
              self.fields.pop('assigned_to', None)
          

class TicketCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = '__all__'
