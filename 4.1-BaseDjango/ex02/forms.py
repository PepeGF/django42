from django import forms

class SampleForm(forms.Form):
    """A simple form with a single text field."""
    name = forms.CharField(label='Your Name', max_length=100)
    # submit button
    