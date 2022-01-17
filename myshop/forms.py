from django import forms


class RangeForm(forms.Form):
    min_value = forms.CharField()
    max_value = forms.CharField()
