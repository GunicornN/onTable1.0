from django import forms
from django.forms import ModelForm,Textarea, IntegerField
from company.models import OnlineOrders

class OnlineOrdersForm(forms.ModelForm):
    class Meta:
        model = OnlineOrders
        fields = ('first_name', 'last_name','description','custom_QRCodes','number_for_choice1','number_for_choice2', 'address1','city','zip_code')
        labels = {
            'first_name': 'Prénom',
            'last_name' : 'Nom',
            'description' : 'Description',
            'custom_QRCodes' : 'QR-Codes Personnalisés',
            'number_for_choice1' : 'Nombre de stickers',
            'number_for_choice2' : 'Nombre de présentoirs',
            'address1' : 'Addresse de livraison',
            'city' : 'Ville de livraison',
            'zip_code' : 'Code Postale de livraison',
        }


        widgets = {

            #'first_name': forms.TextInput(attrs={'class': 'w-50' }),
            #'last_name': forms.TextInput(attrs={'class': 'w-50' }),
            #'number_for_choice1': forms.IntegerField(attrs={'class': 'w-50' }),
            #'number_for_choice2': forms.IntegerField(attrs={'class': 'w-50' }),

            'description': forms.Textarea(attrs={'class': 'w-100', 'rows':4})
        }
