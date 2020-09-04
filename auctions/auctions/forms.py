from django.forms import ModelForm, CharField, PasswordInput, Form, ChoiceField
from .models import *


class RegistrationForm(ModelForm):
    confirmation = CharField(widget=PasswordInput)
    password = CharField(widget=PasswordInput)

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
        exclude = ['owner', 'slug', 'status']


class BiddingForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['value']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['writer', 'listing']


class CategorySelectionForm(Form):
    category = ChoiceField(choices=Category)


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
