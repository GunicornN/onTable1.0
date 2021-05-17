from django import forms
from django.forms.models import BaseModelFormSet
from company.models import pictureCard, Document
from django.forms import formset_factory

from company_manager.tasks import convert_pdf_to_jpeg

#Transformer 
import os
from django.conf import settings

from django.core.files.storage import FileSystemStorage

#/////////////////////////////////////////////////
# PLEASE REMOVE THIS AFTER UPDATE 
#/////////////////////////////////////////////////

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'document', )

#/////////////////////////////////////////////////

class PictureCardForm(forms.ModelForm):
    class Meta:
        model = pictureCard
        fields = ('name','picture')
        widgets = {

            'picture' : forms.ClearableFileInput(attrs={'class': 'w-100', 
                'rows':4,
                'accept':'image/jpeg, image/png, image/gif, image/heic, image/heif, image/tiff ,application/pdf',
                'class':'picture',
                'multiple': True,
            })
    }
    def save(self,company,upload_by):
        file = self.cleaned_data['picture']
        cardName = self.cleaned_data['name']
        if file.name.endswith('.pdf'):
            #save only document file into media/temp
            folder_path = os.path.join(settings.MEDIA_ROOT,'temp/')
            fs = FileSystemStorage(location=folder_path) 
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)

            #transform it into pdf
            print("------")
            print("CONVERT PDF :")
            convert_pdf_to_jpeg.delay(file_path,company.company_code,cardName,upload_by) 
            print("-------")   
            return  
        else :
            instance = super(PictureCardForm, self).save(commit=False)
            instance.company = company
            instance.upload_by = upload_by
            instance.save()
        return instance

    def save2(self,company,upload_by,cardName):
        file = self.cleaned_data['picture']
        if file.name.endswith('.pdf'):
            #save only document file into media/temp
            folder_path = os.path.join(settings.MEDIA_ROOT,'temp/')
            fs = FileSystemStorage(location=folder_path) 
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)

            #transform it into pdf
            convert_pdf_to_jpeg.delay(file_path,company.company_code,cardName,upload_by)    
            return  
        else :
            instance = super(PictureCardForm, self).save(commit=False)
            instance.company = company
            instance.upload_by = upload_by
            instance.name = cardName
            instance.save()
        return instance

PictureCardFormset = formset_factory(PictureCardForm,
    extra=1,
)

