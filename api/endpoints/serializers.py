from rest_framework import serializers

class LogbookSerializer(serializers.Serializer):
    """Serializer for Logbook data"""
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    month = serializers.IntegerField()

class MonthlyReportSerializer(serializers.Serializer):
    """Post .pdf file only"""
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)