from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from GreatHoliday.constants import countries
import http.client
import requests
import json
from datetime import datetime
import datetime
import time

def index(request):
    if request.method == 'POST':
        if 'newLogin' in request.POST:
            return cadastrar(request)
        elif 'unidade_temp' in request.POST:
            return atualizar(request)
        elif 'usrEmail' in request.POST:
            return logar(request)

    print(list(countries.keys()))


    lista = []

    for key, value in countries.items():
        lista.append({"value": key, "label": value})

    context = {
        'search': "",
        'countryCodes': lista
    }
    return render(request, 'GreatHoliday/start.html', context)


def search(request):
    search = request.GET.get("search").replace(" ", "")
    year = str(datetime.datetime.now().year)
    unidadeTemp = "c"
    if "unit" in request.GET:
        unidadeTemp = request.GET.get("unit").lower()

    # Pesquisa previsão do tempo
    headers = {
        'X-RapidAPI-Key': "6fda019572mshcbe2cbe3d6390fbp146768jsn1ac05fc9b673",
        'X-RapidAPI-Host': "yahoo-weather5.p.rapidapi.com"
    }
    conn = http.client.HTTPSConnection("yahoo-weather5.p.rapidapi.com")
    conn.request(
        "GET",
        "/weather?location=" + search + "&format=json&u=" + unidadeTemp,
        headers=headers
    )
    res = conn.getresponse()
    data = res.read()
    resultWeather = json.loads(data)
    country = list(countries.keys())[list(countries.values()).index(resultWeather["location"]["country"])]


    # Pesquisa feriados
    holidayRequest = requests.get("https://date.nager.at/api/v3/publicholidays/" + year + "/" + country)
    resultHolidays = json.loads(holidayRequest.text)


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
        'unit': unidadeTemp.upper()
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

def cadastrar(request):
    user = request.POST.get("newLogin")
    email = request.POST.get("newEmail")
    senha = request.POST.get("newPassword")

    r = requests.post('http://127.0.0.1:8000/api/new',
                    json={"Nome": user, "Email": email, "Senha": senha, "Unidade_Temperatura": "C"}
    )
    alert = ""
    if r.status_code != 200:
        alert = "E-mail/Usuario já utilizados"
    else:
        alert = "Cadastro feito com sucesso, por favor faça o login"

    context = {'search': "", "alert": alert}
    return render(request, 'GreatHoliday/start.html', context)

def logar(request):
    requestJson = {"Email": request.POST.get("usrEmail")}

    if "usrPassword" in request.POST:
        requestJson["Senha"] = request.POST.get("usrPassword")

    r = requests.post('http://127.0.0.1:8000/api/',
                    json=requestJson,
                    headers={"jwt": request.POST.get("UsrToken") if "UsrToken" in request.POST else ""}
    )

    context = {'search': ""}
    
    lista2 = []
    for key, value in countries.items():
        lista2.append({"value": key, "label": value})

    context['countryCodes'] = lista2

    if r.status_code != 200:
        context["alert"] = "E-mail/Usuario invalidos"
    else:
        obj = json.loads(json.loads(r.text)) #duas vezes por conta dos \ da formatação
        context["token"] = obj["token"]
        context["contaObj"] = obj["cadastro"]
        context["conta"] = json.dumps(obj["cadastro"])
 

        if "Preferencias_Paises" in obj["cadastro"]:
            cidades = []
            today = datetime.datetime.now()
            year = today.strftime("%Y")

            for pais in obj["cadastro"]["Preferencias_Paises"]:
                #Carrega informações das 3 cidades mais populosas dos paises favoritados
                r = requests.get("https://wft-geo-db.p.rapidapi.com/v1/geo/adminDivisions",
                                 headers={
                                    'X-RapidAPI-Key': 'e94e7fef38msh5b0ab2b8907177fp1bd3d1jsn5b0f6c77ca72',
                                    'X-RapidAPI-Host': 'wft-geo-db.p.rapidapi.com'
                                 },
                                params={
                                    "sort": '-population',
                                    "minPopulation": 500000,
                                    "countryIds": pais,
                                    "limit": 3
                                }
                )
                if r.status_code == 200:
                    cidadesJson = json.loads(r.text)
                    time.sleep(0.3)

                    holidayRequest = requests.get("https://date.nager.at/api/v3/publicholidays/" + year + "/" + pais)
                    resultHolidays = json.loads(holidayRequest.text)
                    proxFeriado = None
                    for feriado in resultHolidays:
                        dataFeriado = datetime.datetime.strptime(feriado["date"], '%Y-%m-%d')
                        qtdDias = (dataFeriado - today).days
                        if qtdDias >= 0 and qtdDias <= 10:
                            proxFeriado = feriado["name"] + " " + feriado["date"]
                            break

                    if "data" in cidadesJson:
                        for city in cidadesJson["data"]:
                            cidadeUrl = requests.utils.quote(city["name"])
                            cidades.append({
                                "nome": city["name"], 
                                "lat": city["latitude"], 
                                "long": city["longitude"], 
                                "holiday": proxFeriado,
                                "url": cidadeUrl
                            })

            context["cidadesPreferencias"] = cidades

    return render(request, 'GreatHoliday/start.html', context)

def atualizar(request):
    listaDePaises = request.POST.getlist('paises')
    listaDeTempos = request.POST.getlist('tempos')
    unidade_temperatura = request.POST.get("unidade_temp")
    email = request.POST.get("usrEmail")
    token = request.POST.get("UsrToken")

    r = requests.patch('http://127.0.0.1:8000/api/',
                      json={
                            "Email": email,
                            "Unidade_Temperatura": unidade_temperatura,
                            "Preferencias_Paises": listaDePaises,
                            "Preferenciais_Tempo": listaDeTempos
                      },
                      headers={
                          "jwt": token
                      }
    )
    return logar(request)