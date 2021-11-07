from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from leave.serializers import LeaveTypeSerializer, LeaveFormSerializer, LeaveFormCreationSerializer
from leave.models import LeaveType, LeaveForm
from django.contrib.auth import get_user_model
import requests
from django.conf import settings

User = get_user_model()

class LeaveTypeViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer

class LeaveFormViewSet(viewsets.ModelViewSet):

    queryset = LeaveForm.objects.all() 
    serializer_class = LeaveFormSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(applicant=self.request.user)
        return query_set
        
    def get_reporting_boss(self, token):
        r = requests.get(settings.USERINFO_ENDPOINT, headers={
            "Authorization": "{}".format(token)
        })
        print(r.json())
        if r.status_code != 200:
            raise ValueError(r.json())

        reports_to = r.json().get('reports_to')

        username = None if reports_to == '' else reports_to['username']
        boss = None
        if username is not None:
            boss = User.objects.filter(username=username)
            boss = boss.first() if boss.exists() else None

        return boss


    def create(self, request):
        print("CREATE TRIGGERED")
        request.data.update({'applicant': request.user.id})
        serializer = LeaveFormCreationSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.approval.modified_by = self.get_reporting_boss(request.headers['Authorization'])
            instance.approval.save()
            formSerializer = LeaveFormSerializer(instance)
            return Response(formSerializer.data)
        return Response(serializer.errors)

    # def retrieve(self, request, pk=None):
    #     print("RETRIEVE TRIGGER")
    #     queryset = LeaveForm.objects.all()
    #     form = get_object_or_404(queryset, applicant=request.user, pk=pk)
    #     serializer = LeaveFormSerializer(form)
    #     return Response(serializer.data)

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass