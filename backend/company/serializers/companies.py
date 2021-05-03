from django.db import models

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from company.models import Company

class CompaniesPositionInputSerializer(Serializer):
    """
    Renvoie les entreprises les plus proches selon la localisation envoyée
    """
    latitude = serializers.DecimalField(max_digits=18, decimal_places=15)
    longitude = serializers.DecimalField(max_digits=18, decimal_places=15)



