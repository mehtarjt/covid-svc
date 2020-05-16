import practicedatasets.Covid as ds
import plotly.graph_objs as go


def GetGraphData(countryNames, includeConfirmed, includeDeaths, includeRecovered, isLogScale, isPerCapita):
    # Get Covid Numpy Array from the self created shared package
    allCountriesInfo = ds.CovidDataset().GetCovidNpArray()
    # Get population info outside for loop to avoid opening and loading file multiple times
    if isPerCapita:
        populationInfo = ds.PopulationDataSet().GetPopulationRawDataFrame()
    xAxis = 1
    graphData = []
    for i in range(len(countryNames)):
        # Filter numpy array with the data for a specific country
        countryInfo = allCountriesInfo[allCountriesInfo[:, 0] == countryNames[i]]
        if isPerCapita:
            AdjustValuesPerCapita(countryInfo, populationInfo)
        if includeConfirmed:
            yAxis = 2
            label = "Confirmed"
        if includeDeaths:
            yAxis = 3
            label = "Deaths"
        if includeRecovered:
            yAxis = 4
            label = "Recovered"
        graphData.append(go.Line(x=countryInfo[:, xAxis], y=countryInfo[:, yAxis], name=countryNames[i] + " " + label))
    return graphData


def AdjustValuesPerCapita(allCountriesInfo, populationInfo):
    totalPopulation = GetCountryPopulationInMillions(allCountriesInfo[0, 0], populationInfo)
    allCountriesInfo[:, 3] = allCountriesInfo[:, 3] / totalPopulation


def GetCountryPopulationInMillions(countryName, populationInfo):
    if countryName == "US":
        countryName = "United States"
    if countryName == "China":
        countryName = "China \(and dependencies\)"
    filtered = populationInfo[(populationInfo["Location"].str.contains(countryName)) & (populationInfo["Time"] == 2019)]
    selectedRow = filtered[filtered["PopTotal"] == filtered["PopTotal"].max()]
    populationInMillion = selectedRow["PopTotal"].item() / 1000
    print("Population of " + countryName + " in millions is: " + str(populationInMillion))
    return populationInMillion


def GetGraphLayout(isLogScale):
    xAxisLayout = dict(showgrid=True, zeroline=True, showline=True, showticklabels=True, gridwidth=1)
    yAxisLayout = dict(showgrid=False, zeroline=False, showline=False, showticklabels=True)
    if isLogScale:
        yAxisLayout["type"] = "log"
    graphLayout = go.Layout(xaxis=xAxisLayout, yaxis=yAxisLayout, height=900, width=1200, showlegend=True,)
    return graphLayout
