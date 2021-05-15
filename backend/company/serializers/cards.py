# OnTableAPI/company/serializers/menu.py

from django.db import models

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from company.models import Card, Product, Category, Company

# -------------------------------------------------
#                  Product Serializer
# -------------------------------------------------

class ProductInputSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','description','price']

    def create(self,validated_data):
        return Product.objects.create(**validated_data)

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','description','price','available','slug']

class ProductPartialInputSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def update(self, pk, validated_data):
        product = Product.objects.get(pk=pk)
        for data in validated_data:
            setattr(product, data, validated_data.get(data))
        product.save()

# -------------------------------------------------
#                  Category Serializers
# -------------------------------------------------

class CategorySerializer(ModelSerializer):
    products = ProductSerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ['name','products']

# -------------------------------------------------
#                  Card Serializers
# -------------------------------------------------

class CardInputSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ['name','description']

    def create(self,validated_data):
        # On vérifie s'il existe une carte avec le même nom ici 
        card = Card.objects.get(name=validated_data['name'],company_id=validated_data['company_id'])
        if card :
            raise serializers.ValidationError("Deux cartes ne peuvent avoir le même nom.")
        return Card.objects.create(**validated_data)


class CardPartialInputSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'      

    def update(self, pk, validated_data):
        card = Card.objects.get(pk=pk)
        for data in validated_data:
            setattr(card, data, validated_data.get(data))
        card.save()

class CardOutputSerializer(ModelSerializer):
    """
    GET : Serialize models Card, Categories and products 
    """
    categories = CategorySerializer(many=True,read_only=True)
    class Meta:
        model = Card
        fields = ['name','description','categories','slug']