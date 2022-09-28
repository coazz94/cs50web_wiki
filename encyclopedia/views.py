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


class NewPageForm(forms.Form):
    pagename = forms.CharField(label="", required = True, 
    widget= forms.TextInput
    (attrs={'placeholder':'Enter Title','class':'col-lg-4','style':'margin-top:1rem;'}))


    body = forms.CharField(label="",required= False,
    widget= forms.Textarea
    (attrs={'placeholder':'Enter markdown content','class':'col-lg-5','style':'top:1rem;height:40%'}))



main_form = Search_Field()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : main_form 
    })


def get_page(request, title, ):
    """
        1. get the page content from the function
        2. if the page is empty return an error Page
        3.Return a rendererd Page, with the content, markdown = return html code (!!! use safe in template !!!)
    """
    
    page = util.get_entry(title)

    if page is None:
        return render(request, "encyclopedia/error.html", {
            "form" : form
        })

    else:
        return render(request, "encyclopedia/infopage.html", {
            "title": title,
            "page" : markdown2.markdown(page),
            "form" : main_form 
        })


def search(request):
    """
        1. See if there is Post action happening, else redirect to index page
        2. If yes then geht the search query and get the user to the searched site, else return error page
        3. If search is simmilar to site name, then provied a site with the simmilar results with links to them
    """

    if request.method == "POST":
        form = Search_Field(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search_label"]
            entries = util.list_entries()
            
            if search in entries:
                return get_page(request, search)
            
            entries_searched = []

            for entry in entries:
                if search.lower() in entry.lower():
                    entries_searched.append(entry)

            if entries_searched:
                return render(request, "encyclopedia/search.html", {
                    "entries_searched" : entries_searched, 
                    "form" : main_form 
                })
                 
            else:
                return render(request, "encyclopedia/error.html", {
                    "form":form
                })

    else:
            return HttpResponseRedirect(reverse("wiki:index"))



def create_page(request):
    
    if request.method == "POST":
        x = NewPageForm(request.POST)
        if x.is_valid():
            pagename = x.cleaned_data["pagename"]
            
        else:
            return render(request, "encyclopedia/error.html", {
                "form":main_form
            })
    else:
        return render(request, "encyclopedia/create.html",{
            "form" : main_form,
            "create_form":NewPageForm()
        })