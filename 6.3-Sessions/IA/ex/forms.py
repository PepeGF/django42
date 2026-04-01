from django import forms
from .models import Tip


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':3, 'cols':60}),
        }
