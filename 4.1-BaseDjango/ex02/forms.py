from django import forms

class History(forms.Form):
    """A simple form with a single text field."""
    text = forms.CharField(label='Inputs')
    