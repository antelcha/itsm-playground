from rest_framework import serializers  

class DashboardOverviewSerializer(serializers.Serializer):
    total_tickets = serializers.IntegerField()
    open_tickets = serializers.IntegerField()
    closed_tickets = serializers.IntegerField()
    
class DashboardMetricsSerializer(serializers.Serializer):
    tickets_by_status = serializers.ListField(child=serializers.DictField())
    tickets_by_priority = serializers.ListField(child=serializers.DictField())
    tickets_by_category = serializers.ListField(child=serializers.DictField())
    