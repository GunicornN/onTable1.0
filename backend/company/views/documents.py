# OnTableAPI/company/views/documents.py

import django_filters
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from company.models import Company, pictureCard

from rest_framework.viewsets import ReadOnlyModelViewSet
from company.serializers import PictureCardInputSerializer, PictureCardOutputSerializer
from rest_framework import generics

from company.permissions import IsAuthenticatedAndOwner
from rest_framework.response import Response

from rest_framework import status

#languages
from django.utils.translation import gettext as _

# shortcuts
from django.shortcuts import get_object_or_404

#Models 
from company.models import Document 

class DocumentViewSet(ReadOnlyModelViewSet):
    """
    API View for :
    - create document
    - delete document 
    - view document 
    """
    queryset = pictureCard.objects.all()
    lookup_field = 'slug'

    def get_permissions(self):
        permission_classes = []
        if self.action == 'delete':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'upload':
            permission_classes = [IsAuthenticatedAndOwner] #unknow visitors can post document 
        else :
            permission_classes = [] #change this 
        return [permission() for permission in permission_classes]

    def get_queryset(self,*args,**kwargs):         #PROBLEME ICI 
        if 'slug' in self.kwargs :
            document = get_object_or_404(Document,slug=self.kwargs.get('slug'),company__slug=self.kwargs.get('company_slug'))
            return document 
        else :
            documents = Document.objects.filter(company__slug=self.kwargs.get('company_slug'))
            return documents 
        raise NotFound() 

    def list(self, request,company_slug=None):
        queryset = self.get_queryset()

        output_serializer = PictureCardInputSerializer(queryset,many=True,read_only=True)
        return Response(output_serializer.data)