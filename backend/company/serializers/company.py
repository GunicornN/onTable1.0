from django.db import models

from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from company.models import Company

class CompanyOutputSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['name','address1','city','country','zip_code','location','profilPicture','slug']

class CompanyPictureProfilOutputSerializer(ModelSerializer):
    """
    Output : Image of company 
    """
    class Meta:
        model = Company
        fields = ('name','profilPicture')

class CompanyLocationInputSerializer(Serializer):
    """
    Input : Location of a company 
    """
    latitude = serializers.DecimalField(max_digits=18, decimal_places=15)
    longitude = serializers.DecimalField(max_digits=18, decimal_places=15)


class CompanyLocationOutputSerializer(ModelSerializer):
    """
    Output : Location of a company 
    """
    class Meta:
        model = Company
        fields = ('name','location')

class CompanyCategoriesInputSerializer(Serializer):
    """
    Input : Location and categories
    """
    latitude = serializers.DecimalField(max_digits=18, decimal_places=15)
    longitude = serializers.DecimalField(max_digits=18, decimal_places=15)



# -------------------------------------------------
#       Only for authenticated users 
# -------------------------------------------------
class CompanySettingsInputSerializer(serializers.ModelSerializer):
    class Meta():
        model = Company
        fields = [
            'name',
            'city',
            'address1',
            'address2',
            'zip_code',
            'profilPicture',
        ]
        
    def update(self, pk, validated_data):
        company = Company.objects.get(pk=pk)# récupère les objets grâce à la clé étrangère passée via l'url
        for data in validated_data:
            setattr(company, data, validated_data.get(data))# assimile à un attribut de la classe Company, le contenu d'une variable
        company.save()
        
