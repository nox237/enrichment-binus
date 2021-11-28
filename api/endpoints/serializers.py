from rest_framework import serializers

class LogbookSerializer(serializers.Serializer):
    """Serializer for Logbook data"""
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    month = serializers.IntegerField()

class MonthlyReportSerializer(serializers.Serializer):
    """Serializer for MonthlyReportSerializer"""
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

class AssignmentSerializer(serializers.Serializer):
    """Serializer for AssignmentSerializer"""
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

class uploadFiles(serializers.Serializer):
    """Serializer for UploadMonthlyReport"""
    fileUpload = serializers.FileField()
    class Meta:
        fields = ['files_upload']
class MonthlySerializer(serializers.Serializer):
    """Serializer for MonthlySerializer"""
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
class PostLogbookSerializer(serializers.Serializer):
    """Serializer for PostLogbookSerializer"""
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    month_idx = serializers.IntegerField()
    logbookheaderid = serializers.CharField(max_length=50)
    logbook = serializers.JSONField()
