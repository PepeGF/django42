from django import forms

class UpdateForm(forms.Form):
    """Form for updating movie details."""
    movie = forms.ChoiceField(label='Movie', choices=[], required=True)
    opening_crawl = forms.CharField(widget=forms.Textarea, required=False, label='Opening crawl')

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['movie'].choices = choices
