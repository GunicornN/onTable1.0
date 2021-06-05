# OnTableAPI/company/serializers/carts.py

from django.db import models

from rest_framework.serializers import ModelSerializer, Serializer, ListSerializer
from rest_framework import serializers
from company.models import Cart, Cart_Items

# -------------------------------------------------
#              Cart PRODUCTS Serializer
# -------------------------------------------------

class CartItemSerializer(Serializer):
    slug = serializers.SlugField(max_length=255)
    quantity = serializers.IntegerField(min_value=0,max_value=99)

class CartItemListInputSerializer(ListSerializer):
    child = CartItemSerializer()

    def create(self,validated_data):
        # https://www.django-rest-framework.org/api-guide/serializers/#listserializer
        items = [Cart_Items(**item) for item in validated_data]
        return Cart_Items.objects.bulk_create(items) # optimal sql request to create multiple objects


# -------------------------------------------------
#       PRODUCTS of FORMULAS Serializer
# -------------------------------------------------

class ProductOfFormulaSerializer(Serializer):
    slug = serializers.SlugField(max_length=255)
    quantity = serializers.IntegerField(min_value=0,max_value=99)

class ProductsOfFormulaListInputSerializer(ListSerializer):
    child = CartItemSerializer()

    def create(self,validated_data):
        # https://www.django-rest-framework.org/api-guide/serializers/#listserializer
        items = [Cart_Items(**item) for item in validated_data]
        return Cart_Items.objects.bulk_create(items) # optimal sql request to create multiple objects

# -------------------------------------------------
#              Formulas Item Serializer
# -------------------------------------------------

class CartFormulaSerializer(Serializer):
    category_slug = serializers.SlugField(max_length=255)
    products = CartItemListInputSerializer()


class CartFormulaListInputSerializer(ListSerializer):
    child = CartFormulaSerializer()

    def create(self,validated_data):
        # https://www.django-rest-framework.org/api-guide/serializers/#listserializer
        items = [Cart_Items(**item) for item in validated_data]
        return Cart_Items.objects.bulk_create(items) # optimal sql request to create multiple objects

# -------------------------------------------------
#               Cart Serializer
# -------------------------------------------------


class CartOutputSerializer(ModelSerializer):
    # GET : list 
    # 
    # https://stackoverflow.com/questions/17280007/retrieving-a-foreign-key-value-with-django-rest-framework-serializers 
    # table_number = serializers.RelatedField(source='table',read_only=True)
    # updated_on

    # https://stackoverflow.com/questions/52167246/django-rest-framework-validate-json-data

    # https://makina-corpus.com/blog/metier/2015/django-rest-framework-les-serializer-et-les-exceptions-partie-1


    ## TODO : Rajouter le champ numéro de TABLE 
    #table = TableSerializer()

    class Meta:
        model = Cart
        fields = [
            'person_name','total_amount','paid_amount',
            'discount','payment_method','created_on','paid_on','table'
        ]      




class CartInputSerializer(ModelSerializer):
    # POST create 
    products = CartItemListInputSerializer() # ListSerializer
    table_number = serializers.IntegerField(min_value=1,max_value=350)
    company_slug = serializers.CharField(max_length=100)

    formulas = CartFormulaListInputSerializer()

    class Meta:
        model = Cart
        fields = [
            'table_number','payment_method','person_name','company_slug','products','formulas'
        ]
# -------------------------------------------------
#              Tables Cart Serializer
# -------------------------------------------------  

from rest_framework.serializers import ModelSerializer, ListSerializer
from rest_framework import serializers
from company.models import Table, Company

class TableOrderSerializer(ModelSerializer):
    orders = CartOutputSerializer
    class Meta:
        model = Table
        fields = ['table_no']



