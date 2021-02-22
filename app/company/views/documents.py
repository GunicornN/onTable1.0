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

class Document(ReadOnlyModelViewSet):
    """
    API View for :
    - create document
    - delete document 
    - view document 
    """
    queryset = pictureCard.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'delete':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'upload':
            permission_classes = [IsAuthenticatedAndOwner] #unknow visitors can post document 
        else :
            permission_classes = [] #change this 
        return [permission() for permission in permission_classes]

    def list(self, request,pk=None):
        input_serializer = PictureCardInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        picture_card = get_object_or_404(pictureCard, pk=input_serializer.data['id'])
        output_serializer = PictureCardOutputSerializer(picture_card)

        return Response(output_serializer.data)

    @action(detail=True,methods=['POST'])
    def upload(self,request,pk=None):  #UPLOAD DOESN'T WORK
        company = Company.objects.get(pk=company_pk)
        input_serializer = PictureCardInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save(company_id=company.id)

        return Response(_("Le Document a bien été ajouté."),status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,methods=['GET'])
    def delete(self,request,pk=None):
        document = self.get_object()
        self.perform_destroy(document)
        
        return Response(_("Le Document a bien été supprimé."),status=status.HTTP_204_NO_CONTENT)

