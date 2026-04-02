from django import forms
from django.contrib.auth.models import User
from .models import Tips


class RegistrationForm(forms.Form):
    user_name = forms.CharField(max_length=150, required=True, error_messages={'required': 'Username is required.'})
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if User.objects.filter(username=user_name).exists():
            raise forms.ValidationError("Username already exists.")
        return user_name
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=150, required=True, error_messages={'required': 'Username is required.'})
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        user_name = cleaned_data.get('user_name')
        password = cleaned_data.get('password')
        if user_name and password:
            if not User.objects.filter(username=user_name).exists():
                raise forms.ValidationError("Invalid username or password.")
            user = User.objects.filter(username=user_name).first()
            if not user.check_password(password):
                raise forms.ValidationError("Invalid username or password.")
        return cleaned_data
    
    def get_user(self):
        return getattr(self, '_user', None)


class TipForm(forms.ModelForm):
    class Meta:
        model = Tips
        fields = ['content']