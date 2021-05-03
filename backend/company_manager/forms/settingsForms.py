from django.forms import ModelForm
from company.models import Company
#---------------------------------------------------------
#   Forms for the settings view, to modify values of the user
#---------------------------------------------------------

class SettingsCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name',
            'address1',
            'address2',
            'city',
            'zip_code',
        ]
        labels = {
            'name': 'Nom De votre Entreprise :',
            'address1' : 'Adresse 1 :',
            'address2' : 'Adresse 2 :',
            'city' : 'Ville :',
            'zip_code' : 'Code Postal :',


        }
