from django import forms


class NewSearchForm(forms.Form):
    search_string = forms.CharField(label="Search an entry", widget=forms.TextInput)


class NewTextForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput)
    body = forms.CharField(label="Body", widget=forms.Textarea)
