import requests
from rest_framework import views
from rest_framework import response
from endpoints import serializers
from enrichment import auth
from enrichment import activity

class ListLogbook(views.APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = serializers.LogbookSerializer

    def get(self, request):
        """
        Return response to use post
        """
        return response.Response({"status":"error", "message":"please use post request to insert username, password, and month"})

    def post(self, request):
        """
        Return response containing logbook of the user
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            month = serializer.validated_data.get('month')
            session = requests.Session()
            response_request = auth.login(session, username, password)
            if response_request == "Error":
                return response.Response({"status":"error", "message":"invalid username and password"})
            activity.get_enrichment(session, response_request)
            result_request = activity.get_logbook(session, activity.get_monthly(session), month)
            return response.Response({"status":"success", "results":result_request})
        else:
            return response.Response({"status":"error", "message":"please use post request to insert username, password, and month"})

class ListMonthlyReport(views.APIView):
    """
    API endpoint that allows user to be viewed or edited Monthly Report Section
    """
    serializer_class = serializers.MonthlyReportSerializer

    def get(self, request):
        return response.Response({"status":"error", "message":""})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            session = requests.Session()
            response_request = auth.login(session, username, password)
            if response_request == "Error":
                return response.Response({"status":"error", "message":"invalid username and password"})
            activity.get_enrichment(session, response_request)
            result_request = activity.get_month_report(session)
            return response.Response({"status":"success", "results":result_request})
        else:
            return response.Response({"status":"error", "message":"please use post request to insert username, password, and month"})