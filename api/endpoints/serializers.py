from rest_framework import serializers

class LogbookSerializer(serializers.Serializer):
    """Serializer for Logbook data"""
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50, write_only=True)
    month = serializers.IntegerField()