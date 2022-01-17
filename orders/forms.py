from django import forms
from django.forms import Select

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['prenom', 'nom', 'email', 'addresse', 'code_postal', 'ville', 'telephone', 'type_paiement']
        widgets={
            'type_paiement':forms.RadioSelect(attrs={'id':'options'})
        }
    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['prenom'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'prenom'
        })
        self.fields['nom'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'nom'
        })
        self.fields['email'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'email'
        })
        self.fields['addresse'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'addresse de livraison'
        })
        self.fields['code_postal'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'code postal'
        })
        self.fields['ville'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ville'
        })
        self.fields['telephone'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'numero de telephone'
        })
