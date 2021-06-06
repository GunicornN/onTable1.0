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
from company.models import Company, Table, PrintStatus, Cart

# routage
from rest_framework.decorators import action

# Serializers 
from company.serializers import (
    TableSerializer, 
    TableInputSerializer,
    CartOutputSerializer

)

# internationalization 
from django.utils.translation import gettext as _

# Exceptions 
from rest_framework.exceptions import NotFound 

# time
from datetime import *

class OrderStatus(ModelViewSet):
    queryset = PrintStatus.objects.all()
    serializer_class = CartOutputSerializer
    permission_classes = [IsAuthenticatedAndOwner]

    def get_queryset(self):
        if 'pk' in self.kwargs : # cart_slug pour accéder au status d'une commande
            # Si la requete possède pk dans son url, c'est pour accéder à une commande particulière
            company = get_object_or_404(Company,slug=self.kwargs.get('company_slug'))
            #table = get_object_or_404(Table,table_no=self.kwargs.get('pk'),company=company.id)
            
            cart = get_object_or_404(Cart,id=self.kwargs.get('pk'),company=company.id)
            
            order_status = get_object_or_404(PrintStatus,cart_id=cart.id)
            return order_status 
        else : 
            # si la requete possede company_slug, on retourne des tables
            company = get_object_or_404(Company,slug=self.kwargs.get('company_slug'))
            tables = Table.objects.filter(company=company.id)
            if tables :
                return tables 
            raise NotFound()

    @action(detail=False,methods=['GET'])
    def placed(self,request,company_slug):
        # commandes passées, qui ont été traitées, le client est parti
        # on recupere dans la queryset une liste de tables 
        filter_date = datetime.today() - timedelta(hours=1)
        print(filter_date)
        table = self.get_queryset()
        orders = Cart.objects.filter(table__in=table).exclude(created_on__gt=filter_date).exclude(printstatus__status=100)
        
        # le serializer retourne le nom du client, la table, ce qu'il a commandé, le prix 
        output_serializer = CartOutputSerializer(orders,many=True,read_only=True)
        # on a besoin de récupérer les order_status 
        # puis on filtre toutes celles qui ont un status=100
        return Response(output_serializer.data)

    def list(self,request,company_slug):
        tables = self.get_queryset()
        filter_date = datetime.today() - timedelta(hours=1)
        orders = Cart.objects.filter(table__in=tables).exclude(created_on__lt=filter_date)
        #serializer = TableSerializer(queryset,many=True,read_only=True)
        output_serializer = CartOutputSerializer(orders,many=True,read_only=True)
        return Response(output_serializer.data)
        
    @action(detail=True,methods=['GET'])
    def finalize(self,request,company_slug,pk):
        order = self.get_queryset()
        order.status = 100
        order.save() # celle-ci
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self,request,company_slug,pk):
        # TODO
        order = self.get_queryset()

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
        

