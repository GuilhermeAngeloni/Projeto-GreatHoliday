from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from GreatHoliday.constants import countries
from datetime import datetime
import http.client
import requests
import json


def index(request):
    context = {'search': ""}
    return render(request, 'GreatHoliday/start.html', context)


def search(request):
    search = request.GET.get("search").replace(" ", "")
    year = str(datetime.now().year)

    # Pesquisa previsão do tempo
    headers = {
        'X-RapidAPI-Key': "6fda019572mshcbe2cbe3d6390fbp146768jsn1ac05fc9b673",
        'X-RapidAPI-Host': "yahoo-weather5.p.rapidapi.com"
    }
    conn = http.client.HTTPSConnection("yahoo-weather5 .p.rapidapi.com")
    conn.request(
        "GET",
        "/weather?location=" + search + "&format=json&u=c",
        headers=headers
    )
    res = conn.getresponse()
    data = res.read()
    resultWeather = json.loads(data)
    country = list(countries.keys())[list(countries.values()).index(resultWeather["location"]["country"])]


    # Pesquisa feriados
    holidayRequest = requests.get("https://date.nager.at/api/v3/publicholidays/" + year + "/" + country)
    resultHolidays = json.loads(holidayRequest.text)


    # Pesquisa detalhes cidade
    cityDetailsRequest = requests.get("https://nominatim.openstreetmap.org/search.php?city="+ search +"&format=jsonv2")
    resultDetailsCity = json.loads(cityDetailsRequest.text)



    # outras cidades
    headers2 = {
        'X-RapidAPI-Key': 'e94e7fef38msh5b0ab2b8907177fp1bd3d1jsn5b0f6c77ca72',
        'X-RapidAPI-Host': 'wft-geo-db.p.rapidapi.com'
    }
    conn2 = http.client.HTTPSConnection("wft-geo-db.p.rapidapi.com")
    conn2.request(
        "GET",
        "/v1/geo/adminDivisions?countryIds=" + country + "&minPopulation=500000",
        headers=headers2
    )

    res2 = conn2.getresponse()
    data2 = res2.read()
    anotherCities = json.loads(data2)
    print(anotherCities)


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

    return render(request, 'GreatHoliday/searchresult.html', context)


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

def login(request):

  #  r = request.get('http://127.0.0.1:8000/api',
   #     data={"Email": email, "Senha": senha}
    #)




    return render(request, 'GreatHoliday/login.html')

def cadastrar(request):
    user = request.POST.get("userLogin")
    email = request.POST.get("userEmail")
    senha = request.POST.get("userPassword")

    r = requests.post('http://127.0.0.1:8000/api/new',
                    json={"Nome": user, "Email": email, "Senha": senha, "Unidade_Temperatura": "C"}
    )
    print(r)
