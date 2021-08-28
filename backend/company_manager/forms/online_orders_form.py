from django import forms
from django.forms import ModelForm,Textarea, IntegerField
from company.models import OnlineOrders

class OnlineOrdersForm(forms.ModelForm):
    class Meta:
        model = OnlineOrders
        fields = ('first_name', 'last_name','description','custom_QRCodes','number_for_choice1','number_for_choice2', 'address1','city','zip_code')
        labels = {
            'first_name': 'First Name',
            'last_name' : 'Last Name',
            'description' : 'Description',
            'custom_QRCodes' : 'Custom QR Codes',
            'number_for_choice1' : 'Number of stickers',
            'number_for_choice2' : 'Number of displays',
            'address1' : 'Shipping Address',
            'city' : 'Shipping City',
            'zip_code' : 'Shipping Zip Code',
        }


        widgets = {

            #'first_name': forms.TextInput(attrs={'class': 'w-50' }),
            #'last_name': forms.TextInput(attrs={'class': 'w-50' }),
            #'number_for_choice1': forms.IntegerField(attrs={'class': 'w-50' }),
            #'number_for_choice2': forms.IntegerField(attrs={'class': 'w-50' }),

            'description': forms.Textarea(attrs={'class': 'w-100', 'rows':4})
        }
