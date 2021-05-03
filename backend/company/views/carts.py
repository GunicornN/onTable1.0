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
    CartOutputSerializer,
    CartItemListInputSerializer
)

# internationalization 
from django.utils.translation import gettext as _

# Exceptions 
from rest_framework.exceptions import NotFound 

class CartsViewSet(ModelViewSet):
    """
    Endpoint : /api/companies/<company_pk>/carts/
    Everybody can CREATE

    Only Company owner can DELETE, LIST, PARTIAL_UPDATE
    """
    queryset = Cart.objects.all()
    serializer_class = CartOutputSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        permission_classes = []
        if self.action == 'delete':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list' :
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'create':
            permission_classes = []
        else :
            return []
        return [permission() for permission in permission_classes]

    def create(self,request,company_slug=None):
        queryset = self.get_queryset()
        serializer = CartInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        return Response("Cart Created",status=status.HTTP_201_CREATED)

    def list(self,request,company_slug=None):
        # retourne la liste des Paniers (Cart)
        # retourne aussi les produits (items_cart) liés à ce panier

        queryset = self.get_queryset()
        serializer = CartOutputSerializer(queryset,many=True,read_only=True)

        return Response(serializer.data)


