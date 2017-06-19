from .models import db_user
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = db_user
        fields = ['username', 'email', 'password', 'full_name', 'type']