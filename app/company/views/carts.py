# OnTableAPI/company/views/carts.py

# Basics utils of Django 
#from rest_framework import filters
from django.shortcuts import get_object_or_404

# Permissions
from company.permissions import IsAuthenticatedAndOwner

# Response And Status 
from rest_framework.response import Response
from rest_framework import status

# Models 
from rest_framework.viewsets import ModelViewSet
from company.models import Company, Cart

# Serializers 
from company.serializers import (
    CartInputSerializer,
    CartSerializer 
)

# internationalization 
from django.utils.translation import gettext as _

# Exceptions 
from rest_framework.exceptions import NotFound 

class CardsViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'delete':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticatedAndOwner] 
        else :
            return []
        return [permission() for permission in permission_classes]


    def create(self,request,company_pk=None):
        pass

    def retrieve(self,request,company_pk=None,pk=None):
        queryset = self.get_queryset()
        serializer = CartSerializer(queryset,read_only=True)
        return Response(serializer.data)

    def list(self,request,company_pk=None):
        queryset = self.get_queryset()
        serializer = CartSerializer(queryset,many=True,read_only=True)

        return Response(serializer.data)

    def delete(self,request,company_pk=None,pk=None):
        pass


