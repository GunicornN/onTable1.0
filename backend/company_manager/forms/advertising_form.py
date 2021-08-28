from django import forms
from company.models import Advertisement

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('picture', 'ttl','companies','url')
        widgets={
            'ttl': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'ex. : 12/11/2000',
                    'label' : 'Name',
                    'type' : 'date',
                }
            ),
            'companies': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                }
            ),
            'url': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'example.com'
                }
            )


        }
