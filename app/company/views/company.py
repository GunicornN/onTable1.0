# OnTableAPI/company/views/documents.py
from django.shortcuts import render

from rest_framework.decorators import action
from company.models import Company

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet


from company.serializers import (
    CompanyOutputSerializer,
    CompanyPictureProfilOutputSerializer,   
    CompanyLocationInputSerializer,        #Location Input
    CompanyLocationOutputSerializer,      #Location Output
    CompanyCategoriesInputSerializer,   # Categories
    CompanySettingsInputSerializer, # Settings 
    
)

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from company.permissions import IsAuthenticatedAndOwner

from rest_framework.decorators import api_view, permission_classes

from rest_framework import status

class CompanyReadViewSet(ModelViewSet):
    """
    ViewSet for :
    - Get Company Infos 
    - Get Company Picture 
    """
    serializer_class = CompanyOutputSerializer
    queryset = Company.objects.all()
    
    def get_permissions(self):
        permission_classes = []
        if self.action == 'partial_update':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticatedAndOwner] # change to IsAuthenticated Only 
        else :
            pass
        return [permission() for permission in permission_classes]

    @action(detail=True,methods=['GET'])
    def picture_profil(self, request, pk=None):
        """
        picture_profil
        For : authenticated users and unauthorised users
        """
        queryset = self.get_queryset()
        company = get_object_or_404(queryset, pk=pk)
        output_serializer = CompanyPictureProfilOutputSerializer(company) #return image
        return Response(output_serializer.data)

    
    @action(detail=True,methods=['GET'])
    def location(self, request, pk=None):
        """
        Get the location of a company 

        url : /company/<pk>/location
        For : authenticated users and unauthorised users
        """
        queryset = self.get_queryset()
        company = get_object_or_404(queryset, pk=pk)
        output_serializer = CompanyLocationOutputSerializer(company) #return location 
        return Response(output_serializer.data)

    @action(detail=False,methods=['POST'])
    def location(self, request):           #change this name
        """
        Get nearbest companies 

        url : /company/location/<args>
        ex : /company/location?longitude=4.7&latitude=4.8
        request params : longitude, latitude 
        For : authenticated users and unauthorised users
        """
        input_serializer = CompanyLocationInputSerializer(data=request.data) #MAUVAIS INPUT SERIALIZER 
        input_serializer.is_valid(raise_exception=True)

        companies = Company.objects.get_nearby(input_serializer.data['latitude'],input_serializer.data['longitude'])
        output_serializer = CompanyOutputSerializer(companies) 
        return Response(output_serializer.data)

    @action(detail=False,methods=['GET'])
    def category(self, request):
        """
        Get companies which corresponding with category nearbest companies 

        url : /company/location
        request params : category name, longitude, latitude 
        """
        input_serializer = CompanyCategoriesInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        companies = Company.objects.get_nearby(
            input_serializer.data['latitude'],
            input_serializer.data['longitude'],             #add categories 
        )
        output_serializer = CompanyOutputSerializer(companies) 
        return Response(output_serializer.data)

    # -------------------------------------------------
    #       Only for authenticated users 
    # -------------------------------------------------
    def partial_update(self,request,pk=None,*args, **kwargs):
        """

        **Context**
        PATCH: The PATCH method is used to apply partial modifications to a resource.

        Check if it's for Authenticated Users Only, and if the Auth User have the company 

        Renvoie les données envoyées 
        """
        queryset = self.get_queryset()

        input_serializer = CompanySettingsInputSerializer(data=request.data,partial=True) #partial=True pour ne pas créer d'objet
        input_serializer.is_valid(raise_exception=True)

        input_serializer.update(pk,input_serializer.validated_data)

        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True,methods=['GET'])
    def get_status(self,request,pk=None):
        pass