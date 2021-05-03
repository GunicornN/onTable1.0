from django.forms import TextInput,IntegerField
from django import forms

#---------------------------------------------------------
#   All the forms relative to the manage of tables
#---------------------------------------------------------




#---------------------------------------------------------
#   Forms that ask how many QRCodes the Company want
#---------------------------------------------------------


class AddTableForm(forms.Form):
    table_data= forms.IntegerField(
        label="Nombre de tables que vous souhaitez créer.",
        widget=forms.TextInput()
    )
