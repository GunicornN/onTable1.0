from django.forms import TextInput,IntegerField
from django import forms
from company.models import Customer
#---------------------------------------------------------
#   Form to connect the user to cards
#---------------------------------------------------------


class ConnexionForm(forms.Form):
    code_connexion= forms.CharField(
        label="Code :",
        widget=forms.TextInput(attrs={'class': 'w-100', 'placeholder': 'ex. : YZZZ'}),
        max_length=5,
    )

class CustomerInfosForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'surname','email','phoneNumber')
        labels = {
            'name': 'Nom ',
            'surname' : 'Prénom ',
            'email': 'Adresse mail',
            'phoneNumber' : '* Numéro de téléphone'

        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-100'}),
            'surname': forms.Textarea(attrs={'class': 'w-100', 'rows':4}),
            'email': forms.Textarea(attrs={'class': 'w-100', 'rows':4}),
            'phoneNumber': forms.Textarea(attrs={'class': 'w-100', 'rows':4})

        }

