from django.forms import ModelForm, CharField, PasswordInput
from .models import *


class RegistrationForm(ModelForm):
    confirmation = CharField(widget=PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class ListingCreationForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['owner']


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
