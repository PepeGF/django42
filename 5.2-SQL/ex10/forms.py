from django import forms

class FilterForm(forms.Form):
    min_release_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(
            attrs={'type': 'date'}
            ), 
            label='Minimum release date')
    max_release_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(
            attrs={'type': 'date'}
            ), 
            label='Maximum release date')
    diameter_gt = forms.IntegerField(
        required=True, 
        label='Diameter greater than')
    gender = forms.ChoiceField(
        choices=[], 
        required=True, 
        label='Gender')

    def __init__(self, gender_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].choices = gender_choices