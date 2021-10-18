# OnTableAPI/company/serializers/tables.py

from django.db import models

from rest_framework.serializers import ModelSerializer, ListSerializer
from rest_framework import serializers
from company.models import Table, Company

# internationalization 
from django.utils.translation import gettext as _

# -------------------------------------------------
#                  Tables Serializers
# -------------------------------------------------

class TableSerializer(ModelSerializer):
    """Serializes a restaurant table."""

    class Meta :
        model = Table
        fields = ['table_no','updated_on','table_code']

class TableInputSerializer(ModelSerializer):
    """Validates request data for table creation."""
    class Meta:
        model = Table
        fields = ['table_no']


    def create(self,validated_data):
        try :
            # Check if a table with the same number already exists
            table = Table.objects.get(table_no=validated_data['table_no'],company=validated_data['company_id'])
            raise serializers.ValidationError(_("Two tables cannot have the same number."))
        except Table.DoesNotExist:
            return Table.objects.create(**validated_data)
            



    