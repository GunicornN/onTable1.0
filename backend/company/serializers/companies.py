from django.db import models

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from company.models import Company

class CompaniesPositionInputSerializer(Serializer):
    """Returns the nearest companies based on the provided location."""
    latitude = serializers.DecimalField(max_digits=18, decimal_places=15)
    longitude = serializers.DecimalField(max_digits=18, decimal_places=15)



