from django.urls import path
from .views import Home, CovidGraph, CovidGraphAPI, CovidEmbeddedGraph, Countries


urlpatterns = [
    path("", Home, name="home"),
    path("graphs/", CovidGraph, name="graphs"),
    path("samplejson/", CovidGraphAPI, name="samplejson"),
    path("embgraph/", CovidEmbeddedGraph, name="embgraph"),
    path("countries/", Countries, name="countries"),
]
