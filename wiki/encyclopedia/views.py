from django import forms
from django.shortcuts import render
import markdown2 as md
from . import util
from django.views.generic.edit import FormView
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_access(request, entry):
    markdowner = md.Markdown()
    result = util.get_entry(entry)
    if result:
        text = markdowner.convert(result)
    else:
        text = None
    return render(request, "encyclopedia/entrypage.html", {

        "entry": text
    })


class NewSearchForm(forms.Form):
    search_string = forms.CharField(label="Search an entry")


def search(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search_string = form.cleaned_data["search_string"]
    result = util.search_entry(search_string)
    return render(request, "encyclopedia/searchpage.html", {
        "search_result": result
    })
