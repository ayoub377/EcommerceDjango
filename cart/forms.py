from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.CharField(label='Quantity', widget=forms.TextInput(attrs={'class': 'input-text qty text',
                                                                               'name': 'quantity',
                                                                               'data-min': '1',
                                                                               'data-max': '1000',
                                                                               'value': '1',
                                                                               'onChange': 'Change('
                                                                                           'this)'
                                                                               }))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
