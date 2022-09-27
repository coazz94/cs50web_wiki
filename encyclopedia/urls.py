from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.get_page, name="get_page"),
    path("search/", views.search, name="search"), 
]
