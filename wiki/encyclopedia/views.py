from django.shortcuts import render
import markdown2 as md
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect

from .WikiForms import *


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })


def entry_access(request, entry):
    markdowner = md.Markdown()
    result = util.get_entry(entry)
    if result:
        text = markdowner.convert(result)
    else:
        text = None
    return render(request, "encyclopedia/entrypage.html", {

        "entry": text, "title": entry,
        "form": NewSearchForm()
    })


def edit(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        form = NewTextForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["title"]
            new_body = form.cleaned_data["body"]
            util.save_entry(new_title, new_body)
            return HttpResponseRedirect(reverse(index))
    return render(request, 'encyclopedia/edit.html', {
        "editform": NewTextForm(initial={"body": content,
                                        "title": title}),
        "form": NewSearchForm()
    })


def add(request):
    if request.method == "POST":
        form = NewTextForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            for entry in util.list_entries():
                if title.lower() == entry.lower():
                    return render(request, "encyclopedia/add_page.html", {
                        "addform": form, "error": True,
                        "form": NewSearchForm()
                    })
            util.save_entry(title, body)
            return entry_access(request, title)
    return render(request, 'encyclopedia/add_page.html', {
        "addform": NewTextForm(), "error": False,
        "form": NewSearchForm()
    })


def random_entry(request):
    entry = util.random_entry()
    return entry_access(request, entry)


def search(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search_string = form.cleaned_data["search_string"]
            result = util.search_entry(search_string)
            return render(request, 'encyclopedia/searchpage.html', {
                "entries": result,
                "form": NewSearchForm()
            })
    return render(request, 'encyclopedia/searchpage.html', {
        "entries": [],
        "form": NewSearchForm()
    })
