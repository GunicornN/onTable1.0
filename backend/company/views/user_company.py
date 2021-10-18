
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from company.serializers import CompanyOutputSerializerPatch
from company.models import Company

from rest_framework.response import Response

from rest_framework.mixins import RetrieveModelMixin
from rest_framework import generics

class CompanyOfUser(RetrieveModelMixin,generics.GenericAPIView):
    """
    ViewSet for :
    - Get Company Infos 
    - Get Company Picture 
    """
    queryset = Company.objects.all()

    def get(self,request):
        if request.user:
             company = request.user.company
             serializer = CompanyOutputSerializerPatch(company)
             return Response(serializer.data, status=200)
        else:
             content = {'message': "No Unauthenticated, can\'t access to Company details."}
             return Response(content, status=401)

