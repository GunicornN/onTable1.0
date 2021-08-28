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
        label="Number of tables to create.",
        widget=forms.TextInput()
    )
