from django.shortcuts import render
import markdown2
from django import forms


from . import util


class Search_Field(forms.Form):
    search_label = forms.CharField(label="" , widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))


search = Search_Field()

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search" : search
    })


def get_page(request, title):

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


def search_page(request):

    
    
    if request.method == "GET":
        print(search)
        
    else:
        return index(request)

    return index(request)
    #return to index page
