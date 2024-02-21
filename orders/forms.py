from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    different_shipping = forms.BooleanField()

    class Meta:
        model = Order
        fields = ['customer', 'prenom', 'nom', 'addresse', 'code_postal', 'ville', 'telephone', 'type_paiement',
                  'different_shipping']

        widgets = {
            'type_paiement': forms.RadioSelect(attrs={'id': 'options'}),

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

        self.fields['different_shipping'].widget = forms.CheckboxInput(
            attrs={
                'class': 'custom-control-input'
            }
        )
