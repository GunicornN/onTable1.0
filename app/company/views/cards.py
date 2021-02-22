# OnTableAPI/company/views/cards.py

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
from company.models import Company, Card, Product

# Serializers 
from company.serializers import (
    CardInputSerializer,
    CardOutputSerializer,
    CardPartialInputSerializer,
    ProductSerializer, 
    ProductInputSerializer, 
    ProductPartialInputSerializer
)

# internationalization 
from django.utils.translation import gettext as _

# Exceptions 
from rest_framework.exceptions import NotFound 

class CardsViewSet(ModelViewSet):
    """
    Viewset for :

    """
    queryset = Card.objects.all()
    serializer_class = CardInputSerializer #Change this ? 

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

    def get_queryset(self):         #PROBLEME ICI 
        if 'pk' in self.kwargs :
            card = get_object_or_404(Card,pk=self.kwargs.get('pk'))
            return card 

            #categories = card.categories.all() # get all categories obj via une cardinalité avec l'obj carte 
            #return categories
        else :
            cards = Card.objects.filter(company=self.kwargs.get('company_pk'))
            return cards 
        raise NotFound() 

    def list(self,request,company_pk=None):
        # Return many cards
        queryset = self.get_queryset()
        serializer = CardOutputSerializer(queryset,many=True,read_only=True)# many=True pour dire que la requête est un tableau de plusieurs cartes 

        return Response(serializer.data)

    def retrieve(self,request,company_pk=None,pk=None):
        # Return One Card 
        queryset = self.get_queryset()
        serializer = CardOutputSerializer(queryset,read_only=True)
        return Response(serializer.data) 

    def create(self,request,company_pk=None):
        company = get_object_or_404(Company,id=company_pk)
        input_serializer = CardInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True) #test if request.data is correct
        # Enregistrer l'objet :

        input_serializer.save(company_id=company.id)

        return Response(_("La carte a bien été ajouté."),status=status.HTTP_204_NO_CONTENT)

    def partial_update(self,request,company_pk=None,pk=None):
        """
        PATCH 
        """
        serializer = CardPartialInputSerializer(data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.update(pk,serializer.validated_data)
        return Response(_("La carte a bien été modifiée."),status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self,request,company_pk=None,pk=None):
        """
        Check if everybody can remove this ? 

        """
        card = self.get_queryset
        if len(card) == 0 : #Maybe it will be 1, we should test 
            card.delete()
            return Response(_("La carte a bien été supprimé."),status=status.HTTP_204_NO_CONTENT)
        return Response(_("Plusieurs cartes ne peuvent être supprimés simultanément."),status=status.HTTP_400_BAD_REQUEST)

        
class ProductsViewSet(ModelViewSet):
    """
    Viewset for :
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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

    def get_queryset(self):
        """
        Return object or objects depending on passed parameters
        """
        if 'pk' in self.kwargs:     #If object pk 
            product = get_object_or_404(Product,pk=self.kwargs.get('pk'))
            return product 
        else :               #If no pk then there are not product index   
            products = Product.objects.filter(company=self.kwargs.get('company_pk'))   #Only the pk of the company is passed
            return  products
        raise NotFound()

    def list(self,request,company_pk=None):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self,request,company_pk=None,pk=None):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset)
        return Response(serializer.data)

    def create(self,request,company_pk=None):                        
        company = get_object_or_404(Company,id=company_pk)
        input_serializer = ProductInputSerializer(request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save(available=True,company=company)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self,request,company_pk=None,pk=None):
        """
        PATCH 
        """
        serializer = ProductPartialInputSerializer(data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(pk,serializer.validated_data)
        return Response(_("Le produit a bien été modifié."),status=status.HTTP_206_PARTIAL_CONTENT)

    def delete(self,request,company_pk=None,pk=None): #Do this 
        product = self.get_queryset()
        if len(product) == 0 : #Maybe it will be 1, we should test 
            product.delete()
            return Response(_("Le produit a bien été supprimé."),status=status.HTTP_204_NO_CONTENT)
        return Response(_("Plusieurs Produits ne peuvent être supprimés simultanément."),status=status.HTTP_400_BAD_REQUEST)



class CategoriesViewSet(ModelViewSet):
    pass