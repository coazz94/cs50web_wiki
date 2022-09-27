from re import S
from telnetlib import SE
from django.shortcuts import render
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


from . import util


class Search_Field(forms.Form):
    search_label = forms.CharField(label="" , widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

form = Search_Field()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : form
    })


def get_page(request, title, ):

    #get the page content from the function
    page = util.get_entry(title)

    #if the page is empty return an error Page
    if page is None:
        return render(request, "encyclopedia/error.html")

    #Return a rendererd Page, with the content, markdown = return html code (!!! use safe in template !!!)
    else:
        return render(request, "encyclopedia/infopage.html", {
            "title": title,
            "page" : markdown2.markdown(page),
        })


def search(request):


    if request.method == "POST":


        form = Search_Field(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search_label"]
            entries = util.list_entries()
            
            if search in entries:
                return get_page(request, search)
            
            list_similiar = []

            for entry in entries:
                if search in entry:
                    list_similiar.append(entry)
                    #TODO neue Seite rendern mit dem Output der Seiten (diese auch mi href dann im hMTL )                    

    else:

            return HttpResponseRedirect(reverse("wiki:index"))
