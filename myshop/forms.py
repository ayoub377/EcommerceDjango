from django import forms

from myshop.models import Review


# class RangeForm(forms.Form):
#     min_value = forms.CharField()
#     max_value = forms.CharField()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review',)
        widgets = {
            'review': forms.Textarea(attrs={'class': 'tinymce'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'message'}))
