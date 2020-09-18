from django.forms import ModelForm, CharField, PasswordInput, Form, ChoiceField
from .models import *

"""used Model forms instead of django forms for the ease of use and allow reusability"""


class RegistrationForm(ModelForm):
    confirmation = CharField(widget=PasswordInput)
    password = CharField(widget=PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """making the email, last and first name fields mandatory for registration"""
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class ListingCreationForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['owner', 'slug', 'status']


class BiddingForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['value']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['writer', 'listing']


class CategorySelectionForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_type']


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
