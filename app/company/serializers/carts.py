# OnTableAPI/company/serializers/carts.py

from django.db import models

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from company.models import Cart

# -------------------------------------------------
#                  Cart Serializer
# -------------------------------------------------

class CartInputSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ['name','description','price']


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
