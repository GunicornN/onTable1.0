from django.forms import ModelForm, TextInput, modelformset_factory
from django import forms
from company.models import Products, Cards, Categories

#---------------------------------------------------------
#   Theses forms can be redefine, is  it a method that i
#   tried to create dynamically forms for the menus/cards/products
#
#---------------------------------------------------------

TYPEOFCREATION =(
    ("1", "Menu"),
    ("2", "Carte"),
)

CategoriesFormset = modelformset_factory(
    Categories,
    fields=('name','vat'),
    widgets = {
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la section'
            }
        )
    }
)


ProductsFormset = modelformset_factory(
    Products,
    fields=('name','price','description'),
    extra=1,
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nom du produit',
                'label' : 'Nom',
            }
        ),
        'price': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Prix'
            }
        ),
        'description': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'description'
            }
        )


    }
)

class addFormulasOrCardsForm(forms.Form):
    typeOfCreation = forms.ChoiceField(choices=TYPEOFCREATION)
    name = forms.CharField(label="Nom :  ")
    description = forms.CharField(max_length=200)
