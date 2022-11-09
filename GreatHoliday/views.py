from django.shortcuts import render
from django.http import HttpResponse
import http.client
import requests
import json


def index(request):
    context = {'search': "", 'year': "2022", 'country': "BR"}
    return render(request, 'GreatHoliday/starter.html', context)


def search(request):

    # Pesquisa previsão do tempo
    conn = http.client.HTTPSConnection("yahoo-weather5.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "6fda019572mshcbe2cbe3d6390fbp146768jsn1ac05fc9b673",
        'X-RapidAPI-Host': "yahoo-weather5.p.rapidapi.com"
    }

    search = request.GET.get("search").replace(" ", "")
    year = request.GET.get("year")
    country = request.GET.get("country")

    conn.request("GET", "/weather?location=" + search + "&format=json&u=c",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()
    resultWeather = json.loads(data)

    if resultWeather is None:
        context = {
            'search': search,
            'year': year,
            'country': country,
            'error': "Error ao realizar a pesquisa - Weather"
        }
        return render(request, 'GreatHoliday/starter.html', context)

    # Pesquisa feriados
    r = requests.get("https://date.nager.at/api/v2/publicholidays/" + year + "/" + country)
    resultHolidays = json.loads(r.text)

    if resultHolidays is None:
        context = {
            'search': search,
            'year': year,
            'country': country,
            'error': "Error ao realizar a pesquisa - Holidays"
        }
        return render(request, 'GreatHoliday/starter.html', context)

    # Pesquisa detalhes cidade
    r2 = requests.get("https://nominatim.openstreetmap.org/search.php?city="+ search +"&format=jsonv2")
    resultDetailsCity = json.loads(r2.text)

    if resultDetailsCity is None:
        context = {
            'search': search,
            'year': year,
            'country': country,
            'error': "Error ao realizar a pesquisa - Details City"
        }
        return render(request, 'GreatHoliday/starter.html', context)

    print(resultDetailsCity)

    # Pesquisa feriados
    r = requests.get("https://date.nager.at/api/v2/publicholidays/" + year + "/" + country)
    resultHolidays = json.loads(r.text)

    if resultHolidays is None:
        context = {
            'search': search,
            'year': year,
            'country': country,
            'error': "Error ao realizar a pesquisa - Holidays"
        }
        return render(request, 'GreatHoliday/starter.html', context)

    location = resultWeather["location"]
    forecasts = resultWeather["forecasts"][:7]
    today = forecasts.pop(0)
    context = {
        'search': search,
        'year': year,
        'country': country,
        'forecasts': forecasts,
        'today': today,
        'location': location,
        'holidays': resultHolidays,
        'detailsCity': resultDetailsCity
    }

    return render(request, 'GreatHoliday/starter.html', context)


def requestWeather(request, location):

    # print(location)
    conn = http.client.HTTPSConnection("yahoo-weather5.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "6fda019572mshcbe2cbe3d6390fbp146768jsn1ac05fc9b673",
        'X-RapidAPI-Host': "yahoo-weather5.p.rapidapi.com"
    }

    conn.request("GET", "/weather?location=" + location + "&format=json&u=c",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()

    return HttpResponse(data)
