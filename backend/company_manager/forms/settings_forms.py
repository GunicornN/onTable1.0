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
            'name': 'Company Name:',
            'address1' : 'Address 1:',
            'address2' : 'Address 2:',
            'city' : 'City:',
            'zip_code' : 'Zip Code:',
        }
