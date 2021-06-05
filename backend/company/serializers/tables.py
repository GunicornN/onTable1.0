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
    """
    Serialise une table d'un restaurant passé en parametre
    """
    class Meta :
        model = Table
        fields = ['table_no','updated_on','table_code']

class TableInputSerializer(ModelSerializer):
    """
    Serialize les données d'une requete pour vérifier qu'elle est correcte
    """
    class Meta:
        model = Table
        fields = ['table_no']


    def create(self,validated_data):
        # On vérifie s'il existe une carte avec le même nom ici 
        try :
            # Verifie s'il n'y pas déjà un objet avec le même numéro (table_no)
            table = Table.objects.get(table_no=validated_data['table_no'],company=validated_data['company_id'])
            # Si c'est le cas, lève une erreur 
            raise serializers.ValidationError(_("Deux tables ne peuvent avoir le même numéro."))
        except Table.DoesNotExist:
            # Si la vérification échoue, alors crée l'objet 
            return Table.objects.create(**validated_data)
            
class TableListSerializer(ListSerializer):
    child = TableSerializer()

    