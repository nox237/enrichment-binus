from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    """Serializer for Login"""
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

class LogbookSerializer(serializers.Serializer):
    """Serializer for Logbook data"""
    cookies = serializers.JSONField()
    month = serializers.IntegerField()

class MonthlyReportSerializer(serializers.Serializer):
    """Serializer for MonthlyReportSerializer"""
    cookies = serializers.JSONField()

class AssignmentSerializer(serializers.Serializer):
    """Serializer for AssignmentSerializer"""
    cookies = serializers.JSONField()

class uploadFiles(serializers.Serializer):
    """Serializer for UploadMonthlyReport"""
    fileUpload = serializers.FileField()
    class Meta:
        fields = ['files_upload']

class MonthlySerializer(serializers.Serializer):
    """Serializer for MonthlySerializer"""
    cookies = serializers.JSONField()

class PostLogbookSerializer(serializers.Serializer):
    """Serializer for PostLogbookSerializer"""
    cookies = serializers.JSONField()
    month_idx = serializers.IntegerField()
    logbookheaderid = serializers.CharField(max_length=50)
    logbook = serializers.JSONField()
