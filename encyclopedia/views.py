from re import S
from telnetlib import SE
from django.shortcuts import render
import markdown2
from django.http import HttpResponseRedirect
from django.urls import reverse
from pip import main
import re


from . import util, forms



main_form = forms.Search_Field()



def index(request):
    """
        Return the main index page
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : main_form 
    })


def get_page(request, title):
    """
        1. get the page content from the function
        2. if the page is empty return an error Page
        3. Return a rendererd Page, with the content, markdown = return html code (!!! use safe in template !!!)
    """
    
    page = util.get_entry(title)

    if page is None:
        return render(request, "encyclopedia/error.html", {
            "form" : main_form, 
            "message" : "The requested site was not found, you can create your own"
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
        form = forms.Search_Field(request.POST)
        if form.is_valid():
            search = util.clean_name(form.cleaned_data["search_label"])
            entries = util.list_entries()
            
            entries_searched = []

            for entry in entries:
                if search.lower() == entry.lower():
                    return get_page(request, search)
                elif search.lower() in entry.lower():
                    entries_searched.append(entry)

            if entries_searched:
                return render(request, "encyclopedia/search.html", {
                    "entries_searched" : entries_searched, 
                    "form" : main_form 
                })
                 
            else:
                return render(request, "encyclopedia/error.html", {
                    "form":form,
                    "message" : "The searched site was not found, you can create your own"
                })

    else:
            return HttpResponseRedirect(reverse("wiki:index"))


def create_page(request):
    """
        1. If request is post = create a new Page else just go to the page to create a new page
        2. get the form Data the Form ( check if valid )
        3. write to a file with the same name as the title and return the new created page

    """


    if request.method == "POST":
        form_data = forms.NewPageForm(request.POST)
        if form_data.is_valid():

            pagename = util.clean_name(form_data.cleaned_data["pagename"])
            content = form_data.cleaned_data["content"]
            

            if pagename.lower() not in [x.lower() for x in util.list_entries()]:
                try:
                    util.save_entry(pagename, content)
                    return get_page(request, pagename)
                except:
                    return render(request, "encyclopedia/error.html", {
                    "form":main_form, 
                    "message" : "Couldn´t save the page, try again"
                    })
            else:
                return render(request, "encyclopedia/error.html", {
                    "form":main_form, 
                    "message" : "Page with that name alredy exists"
                })

            
        else:
            return render(request, "encyclopedia/error.html", {
                "form":main_form
            })
    else:
        return render(request, "encyclopedia/create.html",{
            "form" : main_form,
            "create_form":forms.NewPageForm()
        })


def edit(request):
    """
        1. Two diffrent POST can be done ( one is to get to the edit Page and the other one is tu save the changes)
        2. re was used because we only allow to change the content of the page not the title
        3. again take the input and delete the old file and save a new and return to the new page
        4. if the request is delete, then delete the page from the file
    """

    
    if "edit" in request.POST:
            pagename = request.POST.get("edit")
            page = util.get_entry(pagename)

            try:
                matches = re.search(r"^[#]\s(.*)\n((?:.|\n)*)", page, re.MULTILINE)
                content = matches.group(2).strip()
            except:
                content = ""

            return render(request, "encyclopedia/edit.html", {
                "form": main_form,
                "create_form": forms.EditPage(initial={"content":content}),
                "pagename" : pagename
            })

    elif "save_changes" in request.POST:

            form_data = forms.EditPage(request.POST)
            pagename = request.POST.get("save_changes")

            if form_data.is_valid():

                content = form_data.cleaned_data["content"]
                
                try:
                    util.save_entry(pagename, content)
                except:
                    return render(request, "encyclopedia/error.html", {
                        "form":main_form,
                        "message" : "Couldn´t save the the changes, try again"
                        })

                return render(request, "encyclopedia/infopage.html", {
                    "title": pagename,
                    "page" : markdown2.markdown(util.get_entry(pagename)),
                    "form" : main_form 
                    })

    elif "delete" in request.POST:
        
        pagename = request.POST.get("delete")

        if pagename.lower() in [x.lower() for x in util.list_entries()]:
            
            if not util.delete_page(pagename):
                return render(request, "encyclopedia/error.html", {
                    "form":main_form, 
                    "message" : "Something went wrong, try again"
                })

            return HttpResponseRedirect(reverse("wiki:index"))


def random(request):

    return get_page(request, util.random_page())


