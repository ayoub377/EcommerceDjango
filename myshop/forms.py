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

