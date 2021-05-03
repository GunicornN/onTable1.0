# OnTableAPI/company/views/documents.py
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.decorators import action, api_view, permission_classes
# Pagination 
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from company.models import Company
from company.permissions import IsAuthenticatedAndOwner
from company.serializers import CompanyCategoriesInputSerializer  # Categories
from company.serializers import \
    CompanyLocationInputSerializer  # Location Input
from company.serializers import \
    CompanyLocationOutputSerializer  # Location Output
from company.serializers import CompanySettingsInputSerializer  # Settings
from company.serializers import (CompanyOutputSerializer,
                                 CompanyPictureProfilOutputSerializer)

# filters 
from rest_framework import filters

class StandardResultsSetPagination(PageNumberPagination):
    # https://www.django-rest-framework.org/api-guide/pagination/
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

class CompanyReadViewSet(ModelViewSet):
    """
    ViewSet for :
    - Get Company Infos 
    - Get Company Picture 
    """
    serializer_class = CompanyOutputSerializer
    queryset = Company.objects.all()
    pagination_class = StandardResultsSetPagination
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','company_code','zip_code','city']

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
    def picture_profil(self, request, slug=None):
        """
        picture_profil
        For : authenticated users and unauthorised users
        """
        queryset = self.get_queryset()
        company = get_object_or_404(queryset, slug=slug)
        output_serializer = CompanyPictureProfilOutputSerializer(company) #return image
        return Response(output_serializer.data)

    @action(detail=True,methods=['GET'])
    def location(self, request, slug=None):
        """
        Get the location of a company 

        url : /company/<pk>/location
        For : authenticated users and unauthorised users
        """
        queryset = self.get_queryset()
        company = get_object_or_404(queryset, slug=slug)
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
    def partial_update(self,request,slug=None,*args, **kwargs):
        """

        **Context**
        PATCH: The PATCH method is used to apply partial modifications to a resource.

        Check if it's for Authenticated Users Only, and if the Auth User have the company 

        Renvoie les données envoyées 
        """
        queryset = self.get_queryset()

        input_serializer = CompanySettingsInputSerializer(data=request.data,partial=True) #partial=True pour ne pas créer d'objet
        input_serializer.is_valid(raise_exception=True)

        input_serializer.update(slug,input_serializer.validated_data)

        return Response(status=status.HTTP_204_NO_CONTENT)

