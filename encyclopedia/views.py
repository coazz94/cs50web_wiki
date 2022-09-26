from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
            "page" : markdown2.markdown(page)
        })