from django.shortcuts import render
import markdown2 as md
from . import util


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


def search(request, search_string):
    result = util.search_entry(search_string)
    return render(request, "encyclopedia/searchpage.html", {
        "search_result": result
    })
