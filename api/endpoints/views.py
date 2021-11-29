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
        return response.Response({"status":"error", "message":"please use post request to insert username, password, and month"}, headers={'Access-Control-Allow-Origin':"*"})

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
                return response.Response({"status":"error", "message":"invalid username and password"}, headers={'Access-Control-Allow-Origin':"*"})
            activity.get_enrichment(session, response_request)
            result_request = activity.get_logbook(session, activity.get_monthly(session), month)
            return response.Response({"status":"success", "results":result_request}, headers={'Access-Control-Allow-Origin':"*"})
        else:
            return response.Response({"status":"error", "message":"please use post request to insert username, password, and month"}, headers={'Access-Control-Allow-Origin':"*"})


class ListAssignment(views.APIView):
    """
    API endpoint that allows user to be viewed list of assignment
    """
    serializer_class = serializers.AssignmentSerializer

    def get(self, request):
        return response.Response({"status":"error", "message":"please use post request to insert username and password"}, headers={'Access-Control-Allow-Origin':"*"})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            session = requests.Session()
            response_request = auth.login(session, username, password)
            if response_request == "Error":
                return response.Response({"status":"error", "message":"invalid username and password"}, headers={'Access-Control-Allow-Origin':"*"})
            activity.get_enrichment(session, response_request)
            result_request = activity.get_assignment(session)
            return response.Response({"status":"success", "results":result_request}, headers={'Access-Control-Allow-Origin':"*"})
        else:
            return response.Response({"status":"error", "message":"please use post request to insert username and password"}, headers={'Access-Control-Allow-Origin':"*"})

class ListMonthlyReport(views.APIView):
    """
    API endpoint that allows user to be viewed or edited Monthly Report Section
    """
    serializer_class = serializers.MonthlyReportSerializer

    def get(self, request):
        return response.Response({"status":"error", "message":"please use post request to insert username and password"}, headers={'Access-Control-Allow-Origin':"*"})

    def post(self, request):
    # def post(self, request, file):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            session = requests.Session()
            response_request = auth.login(session, username, password)
            if response_request == "Error":
                return response.Response({"status":"error", "message":"invalid username and password"}, headers={'Access-Control-Allow-Origin':"*"})
            activity.get_enrichment(session, response_request)
            result_request = activity.get_month_report(session)
            return response.Response({"status":"success", "results":result_request}, headers={'Access-Control-Allow-Origin':"*"})

            # file_upload = request.FILES.get()
            # content_type = file_uploaded.content_type
            # response = "POST API and you have uploaded a {} file".format(content_type)
            # return Response(response, headers={'Access-Control-Allow-Origin':"*"})

        else:
            return response.Response({"status":"error", "message":"please use post request to insert username and password"}, headers={'Access-Control-Allow-Origin':"*"})
 
class ListMonthly(views.APIView):
    """
    API endpoint for getting all available months in the semester
    """
    serializer_class = serializers.MonthlySerializer

    def get(self, request):
        return response.Response({"status":"error", "message":""}, headers={'Access-Control-Allow-Origin':"*"})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            session = requests.Session()
            response_request = auth.login(session, username, password)
            if response_request == "Error":
                return response.Response({"status":"error", "message":"invalid username and password"}, headers={'Access-Control-Allow-Origin':"*"})
            activity.get_enrichment(session, response_request)
            result_request = activity.get_monthly(session)
            return response.Response({"status":"success", "results":result_request}, headers={'Access-Control-Allow-Origin':"*"})
        else:
            return response.Response({"status":"error", "message":"please use post request to insert username and password"}, headers={'Access-Control-Allow-Origin':"*"})


class PostLogbook(views.APIView):
    """
    API endpoint for allowing user to submit multiple logbook
    This API needs month index from ListMonths and also need logbookheaderId from the months data
    
    example: [{"model[Date]": "2021-11-03T00:00:00",
    "model[Activity]": "Title Logbook",
    "model[ClockIn]": "ClockIn Data",
    "model[ClockOut]": "ClockOut Data",
    "model[Description]": "Description Logbook", 
    "model[flagjulyactive]": "false"}]
    """
    serializer_class = serializers.PostLogbookSerializer

    def get(self, request):
        return response.Response({"status":"error", "message":""}, headers={'Access-Control-Allow-Origin':"*"})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            month_idx = serializer.validated_data.get('month_idx')
            logbookheaderid = serializer.validated_data.get('logbookheaderid')
            logbook_json_data = serializer.validated_data.get('logbook')
            session = requests.Session()
            response_request = auth.login(session, username, password)
            if response_request == "Error":
                return response.Response({"status":"error", "message":"invalid username and password"}, headers={'Access-Control-Allow-Origin':"*"})
            activity.get_enrichment(session, response_request)
            result_request = activity.post_logbook_report(session, logbook_json_data, activity.get_logbook(session, activity.get_monthly(session), month_idx), logbookheaderid)
            return response.Response({"status":"success", "results":result_request}, headers={'Access-Control-Allow-Origin':"*"})
        else:
            return response.Response({"status":"error", "message":"please use post request to insert username, password, month_idx, logbookheaderid, and logbook json array"}, headers={'Access-Control-Allow-Origin':"*"})


# class UploadMonthlyReport(views.APIView):
#     serializer_class = uploadFileSerializer