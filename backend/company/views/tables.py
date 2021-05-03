# OnTableAPI/company/views/tables.py

# Basics utils of Django 
from rest_framework import filters
from django.shortcuts import get_object_or_404

# Permissions
from company.permissions import IsAuthenticatedAndOwner

# Response And Status 
from rest_framework.response import Response
from rest_framework import status

# Models 
from rest_framework.viewsets import ModelViewSet
from company.models import Company, Table

# Serializers 
from company.serializers import (
    TableSerializer, 
    TableInputSerializer,
)

# internationalization 
from django.utils.translation import gettext as _

# Exceptions 
from rest_framework.exceptions import NotFound 

class TablesViewSet(ModelViewSet):
    """
    To Do List :
    Vérifier si les permissions sont bonnes
    """
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticatedAndOwner]

    def get_queryset(self):
        if 'pk' in self.kwargs :
            # Si la requete possède pk dans son url, c'est pour accéder à une Table particulière
            table = get_object_or_404(Table,table_no=self.kwargs.get('pk'),company=self.kwargs.get('company_pk'))
            print("table : ",table)
            return table 
        else : 
            tables = Table.objects.filter(company=self.kwargs.get('company_pk'))
            if tables :
                return tables 
            raise NotFound()        #ADAPTER CETTE PARTIE AUX AUTRES MODELS 


    def list(self,request,company_pk=None):
        # retourne les tables d'un restaurant avec leurs commandes 
        queryset = self.get_queryset()
        serializer = TableSerializer(queryset,many=True,read_only=True)
        return Response(serializer.data)

    def retrieve(self,request,company_pk=None,pk=None):
        # retourne une table d'un restaurant 
        
        queryset = self.get_queryset()
        serializer = TableSerializer(queryset,read_only=True)
        return Response(serializer.data)

    def create(self,request,company_pk=None):
        # Vérifier s'il y a pas 2 tables ayant le même numéro, retourner une erreur sinon 
        # Get the company 
        company = get_object_or_404(Company,id=company_pk)
        
        input_serializer = TableInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        input_serializer.save(company_id=company.id)
        return Response(_('La table a bien été crée'),status=status.HTTP_204_NO_CONTENT)

    def delete(self,request,company_pk=None,pk=None):       # <----------- BUG HERE 
        # Vérifier si on peut supprimer la table d'autres Restaurants 
        #Impossible de supprimer des tables
        queryset = self.get_queryset()
        if len(queryset) == 0 : #Maybe it will be 1, we should test 
            queryset.delete()
            return Response(_('La table a bien été supprimée'),status=status.HTTP_204_NO_CONTENT)
        return Response(_("Plusieurs tables ne peuvent être supprimés simultanément."),status=status.HTTP_400_BAD_REQUEST)
        

