from .models import DbUser
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = DbUser
        fields = ['username', 'email', 'password', 'full_name', 'type']