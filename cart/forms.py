from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.CharField(label='Quantity', widget=forms.TextInput(attrs={'class': 'horizontal-quantity '
                                                                                        'form-control',
                                                                               'name': 'quantity',
                                                                               }))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
