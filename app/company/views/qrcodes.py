# OnTableAPI/company/views/qrcodes.py

import django_filters
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from company.models import Company, pictureCard
#from .serializers import CompanySerializers, CategoriesSerializers, CategorySerializers, PictureCardSerializers
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet

"""
class QRCodeView(ReadOnlyModelViewSet):
   
    API View to :
    - get qrcode img 
    
    queryset = Company.objects.all()
    #serializer_class = CompanySerializers
    filter_backends = (filters.SearchFilter,)

    @action(detail=True, methods=['get'])
    def upload_document(request):
        queryset = pictureCard.objects.images_from_company_card(company=current_company,card_name=document_name)

    @action(detail=True, methods=['get'])
    def delete_document(request):
        pass

    @action(detail=True, methods=['get'])
    def see_document(request):
        pass

"""