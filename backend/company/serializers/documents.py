from django.db import models

from rest_framework.serializers import Serializer
from rest_framework import serializers
from rest_framework.views import APIView

from company.models import pictureCard, Company

class PictureCardOutputSerializer(serializers.ModelSerializer):
    class Meta():
        model = pictureCard
        fields = [
            'name',
            'picture'
        ]


# --------------------------------------------
#           Upload documents 
# --------------------------------------------

class PictureCardInputSerializer(Serializer):
    name = serializers.CharField(max_length=50)
    picture = serializers.FileField()
        
    def update(self, pk, validated_data):
        picture_card = pictureCard.objects.get(pk=pk)
        for data in validated_data:
            setattr(company, data, validated_data.get(data))
        company.save()
        
    def validate_picture(self,value):
        # TODO: fix broken validation logic
        if len(lsDocument)  >= settings.MAX_DOCUMENTS_PER_ACCOUNT:
            raise(_('Your account file limit is {}').format(settings.MAX_DOCUMENTS_PER_ACCOUNT))
        if pictureCard.objects.filter(name=form.cleaned_data['name'],company=current_company).exists():
            raise(_('You have already uploaded a document with the same name.'))
        if int(file.size) > settings.MAX_UPLOAD_SIZE:
            raise(serializers.ValidationError( _("Maximum file size is 10MB.")))
        return value