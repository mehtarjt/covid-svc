from django.shortcuts import render, HttpResponse
import plotly.offline as opy
import RnDPackage.Datasets as ds
import pandas as pd
from .GraphHelper import GetGraphData, GetGraphLayout
import html
from django.http import JsonResponse
import urllib

# Create your views here.


def Home(request):
    countries = ["Spain", "France", "Italy", "US", "Denmark", "Sweden", "Canada", "Australia", "Germany", "Poland", "India", "China"]
    # countries = ["Denmark", "US"]
    includeConfirmed = False
    includeDeaths = True
    includeRecovered = False
    isLogScale = True
    isPerCapita = True
    graphData = GetGraphData(countries, includeConfirmed, includeDeaths, includeRecovered, isLogScale, isPerCapita)
    graphInput = {"data": graphData, "layout": GetGraphLayout(isLogScale)}
    fig_div = opy.plot(graphInput, image_width="100%", image_height="100%", include_plotlyjs=False, output_type="div", auto_open=False,)
    context = {"title": "COVID Web Home", "message": "Welcome to COVID Web!", "graph": fig_div}
    return render(request, "home.html", context)


def CovidGraph(request):
    countries = ["Spain", "France", "Italy", "US", "Denmark", "Sweden", "Canada", "Australia", "Germany", "Poland", "India", "China"]
    includeConfirmed = False
    includeDeaths = True
    includeRecovered = False
    isLogScale = True
    isPerCapita = True
    graphData = GetGraphData(countries, includeConfirmed, includeDeaths, includeRecovered, isLogScale, isPerCapita)
    graphInput = {"data": graphData, "layout": GetGraphLayout(isLogScale)}
    fig_div = opy.plot(graphInput, image_width="100%", image_height="100%", include_plotlyjs=False, output_type="div", auto_open=False,)
    jsonData = {"graphHTML": html.escape(fig_div)}
    context = {"title": "API | COVID Web", "message": "Here you can see the graph HTML as JSON data", "jsonData": jsonData}
    return render(request, "graph.html", context)


def CovidGraphAPI(request):
    df = ds.CovidDataset().GetCovidRawDataFrame()[1:20]
    df = df.where(pd.notnull(df), None).to_json(orient="records")
    # return JsonResponse(df, safe=False)
    context = {"title": "API | COVID Web", "message": "Here you can see sample JSON data", "jsonData": df}
    return render(request, "api.html", context)


def Countries(request):
    df = ds.CovidDataset().GetCovidRawDataFrame().groupby(["Location"], as_index=False)["Confirmed"].count()["Location"]
    countries = {"countries": df.to_json(orient="records")}
    return JsonResponse(countries, safe=False)


def CovidEmbeddedGraph(request):
    infoType = request.GET.get("infoType")
    isLogScale = request.GET.get("logScale") == "true"
    byPop = request.GET.get("byPop") == "true"
    countries = request.GET.get("countries").split(",")
    countries = [x.strip(" ") for x in countries]
    includeConfirmed = infoType == "confirmed"
    includeDeaths = infoType == "deaths"
    includeRecovered = infoType == "recovered"
    graphData = GetGraphData(countries, includeConfirmed, includeDeaths, includeRecovered, isLogScale, byPop)
    graphInput = {"data": graphData, "layout": GetGraphLayout(isLogScale)}
    fig_div = opy.plot(graphInput, image_width="100%", image_height="100%", include_plotlyjs=False, output_type="div", auto_open=False,)
    graphHtml = {"graphHtml": fig_div}
    return JsonResponse(graphHtml, safe=False)
