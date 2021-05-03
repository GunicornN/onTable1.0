from django.forms import TextInput,IntegerField
from django import forms


#---------------------------------------------------------
#   Forms that ask how many QRCodes the Company want
#---------------------------------------------------------


class PrintQRCodesForm(forms.Form):
    nbr_of_qrcodes= forms.IntegerField(
        widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Combien vous en faut-il ?'})
    )
