# OnTableAPI/company/serializers/carts.py

from django.db import models

from rest_framework.serializers import ModelSerializer, Serializer, ListSerializer
from rest_framework import serializers
from company.models import Cart, Cart_Items, Product

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

class CartItemAndFormulasOutputSerializer(ModelSerializer):
    items = CartItemSerializer
    formulas = CartFormulaSerializer

    class Meta :
        model = Cart_Items
        depth = 2
        fields = ['items','formulas']

class CartOutputSerializer(ModelSerializer):
    # GET : list 
    # 
    # https://stackoverflow.com/questions/17280007/retrieving-a-foreign-key-value-with-django-rest-framework-serializers 
    # table_number = serializers.RelatedField(source='table',read_only=True)
    # updated_on

    # https://stackoverflow.com/questions/52167246/django-rest-framework-validate-json-data

    # https://makina-corpus.com/blog/metier/2015/django-rest-framework-les-serializer-et-les-exceptions-partie-1


    ## TODO : Rajouter le champ numéro de TABLE 
    cart_items = CartItemAndFormulasOutputSerializer

    class Meta:
        model = Cart
        fields = [
            'person_name','total_amount','paid_amount',
            'discount','payment_method','created_on','paid_on','table','cart_items','id'
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
    
    
    def create(self,validated_data):
        # TODO : FORMULAS
        #{'table_number': 1, 'payment_method': 'CB', 'person_name': 'Alexis', 'company_slug': '1AJBSA', 'products': [OrderedDict([('slug', 'jambon-truffe'), ('quantity', 2)])], 'formulas': []}
        current_company = Company.objects.get(slug=validated_data['company_slug'])
        current_table = Table.objects.get(table_no=validated_data['table_number'],company=current_company)
        
        products = validated_data['products']
        total_price = 0
        for product in products :
            price = Product.objects.get(slug=product['slug']).price
            if not price :
                price = 10
            total_price += price 

        cart = Cart()
        cart.person_name = validated_data['person_name']
        cart.table=current_table
        cart.total_amount = total_price
        cart.paid_amount = total_price
        cart.discount = 0
        cart.payment_method=validated_data['payment_method']
        cart.company=current_company
        cart.save()

        for product in products :
            product = Product.objects.get(slug=product['slug'])
            new_cart_product = Cart_Items()
            new_cart_product.cart = cart
            new_cart_product.items = product
        return cart

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



