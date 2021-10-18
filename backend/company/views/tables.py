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
from company.models import Company, Table, PrintStatus, Cart, Cart_Items, Product

# routage
from rest_framework.decorators import action

# Serializers 
from company.serializers import (
    TableSerializer, 
    TableInputSerializer,
    CartOutputSerializer,
    ItemSerializer
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
        if 'pk' in self.kwargs:
            # If pk is in the URL, retrieve a specific order
            company = get_object_or_404(Company,slug=self.kwargs.get('company_slug'))
            cart = get_object_or_404(Cart,id=self.kwargs.get('pk'),company=company.id)
            order_status = get_object_or_404(PrintStatus,cart_id=cart.id)
            return order_status
        else :
            # If only company_slug, return tables
            company = get_object_or_404(Company,slug=self.kwargs.get('company_slug'))
            tables = Table.objects.filter(company=company.id)
            if tables :
                return tables
            raise NotFound()

    @action(detail=False,methods=['GET'])
    def placed(self,request,company_slug):
        # Past orders that have been processed (customer has left)
        filter_date = datetime.today() - timedelta(hours=1)
        table = self.get_queryset()
        orders = Cart.objects.filter(table__in=table).exclude(created_on__gt=filter_date).exclude(printstatus__status=100)

        output_serializer = CartOutputSerializer(orders,many=True,read_only=True)
        return Response(output_serializer.data)

    def list(self,request,company_slug):
        tables = self.get_queryset()
        filter_date = datetime.today() - timedelta(hours=1)
        orders = Cart.objects.filter(table__in=tables).exclude(created_on__lt=filter_date)
        printstatus = PrintStatus.objects.filter(cart_id__in=orders).exclude(status=100)
        orders = orders.filter(printstatus__in=printstatus)
        cart_items = Cart_Items.objects.filter(cart__in=orders)
        products = Product.objects.filter(products__in=cart_items)        
        output_serializer = CartOutputSerializer(orders,many=True,read_only=True,context={'prd':products})

        return Response(output_serializer.data)
        
    @action(detail=True,methods=['GET'])
    def finalize(self,request,company_slug,pk):
        order_status = self.get_queryset()
        order_status.status = 100
        order_status.save()
        return Response(_('The order has been finalized.'),status=status.HTTP_204_NO_CONTENT)

    def retrieve(self,request,company_slug,pk):
        company = get_object_or_404(Company,slug=company_slug)
        order = get_object_or_404(Cart,company=company,id=pk)
        cart_items = Cart_Items.objects.filter(cart=order.id)  
        products = Product.objects.filter(products__in=cart_items)

        output_serializer_products = ItemSerializer(products,many=True,read_only=True)
        return Response(output_serializer_products.data)

class TablesViewSet(ModelViewSet):
    """ViewSet for managing restaurant tables."""
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticatedAndOwner]

    def get_queryset(self):
        if 'pk' in self.kwargs :
            # If pk is in the URL, retrieve a specific table
            table = get_object_or_404(Table,table_no=self.kwargs.get('pk'),company=self.kwargs.get('company_pk'))
            return table
        else : 
            tables = Table.objects.filter(company=self.kwargs.get('company_pk'))
            if tables :
                return tables 
            raise NotFound()

    def list(self,request,company_pk=None):
        queryset = self.get_queryset()
        serializer = TableSerializer(queryset,many=True,read_only=True)
        return Response(serializer.data)

    def retrieve(self,request,company_pk=None,pk=None):
        queryset = self.get_queryset()
        serializer = TableSerializer(queryset,read_only=True)
        return Response(serializer.data)

    def create(self,request,company_pk=None):
        company = get_object_or_404(Company,id=company_pk)
        
        input_serializer = TableInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        input_serializer.save(company_id=company.id)
        return Response(_('Table created successfully.'),status=status.HTTP_204_NO_CONTENT)

    def delete(self,request,company_pk=None,pk=None):
        queryset = self.get_queryset()
        if len(queryset) == 0 : #Maybe it will be 1, we should test
            queryset.delete()
            return Response(_('Table deleted successfully.'),status=status.HTTP_204_NO_CONTENT)
        return Response(_("Multiple tables cannot be deleted simultaneously."),status=status.HTTP_400_BAD_REQUEST)
        

