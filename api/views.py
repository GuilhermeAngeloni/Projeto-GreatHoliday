from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json

from .models import *
import uuid

def SalvarClimas(arr, conta):   
    for i in arr:
        try:
            clima = Preferenciais_Tempo(tipo_tempo=i, cadastro=conta)
            clima.save()
        except:
            print("")

def SalvarPaises(arr, conta):
    for i in arr:
        try:
            pais = Preferencias_Paises(cod_pais=i, cadastro=conta)
            pais.save()
        except:
            print("")

def NovoCadastro(request):
    try:
        cad = Cadastro(
            Nome=request.data["Nome"],
            Email=request.data["Email"],
            Senha=request.data["Senha"],
            Unidade_Temperatura=request.data["Unidade_Temperatura"])

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        cad.save()
        if "Preferencias_Paises" in request.data:
            SalvarPaises(request.data["Preferencias_Paises"], cad)

        if "Preferenciais_Tempo" in request.data:
            SalvarClimas(request.data["Preferenciais_Tempo"], cad)
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_409_CONFLICT)

def FazerLogin(request):
    email = None
    senha = None
    try:
        email = request.data["Email"]
        senha = request.data["Senha"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    cadastro = None
    try:
        cadastro = Cadastro.objects.get(Email=email, Senha=senha)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    cadastro.token = str(uuid.uuid4())
    cadastro.save()

    resposta = {}
    resposta["token"] = cadastro.token
    resposta["cadastro"] = cadastro.ToJson()

    return Response(json.dumps(resposta))

def AtualizarCadastro(request):
    email = None
    token = None
    try:
        email = request.data["Email"]
        token = request.headers["jwt"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    cadastro = None
    try:
        cadastro = Cadastro.objects.get(Email=email, token=token)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if "Preferencias_Paises" in request.data:
        cadastro.preferencias_paises_set.all().delete()
        SalvarPaises(request.data["Preferencias_Paises"], cadastro)

    if "Preferenciais_Tempo" in request.data:
        cadastro.preferenciais_tempo_set.all().delete()
        SalvarClimas(request.data["Preferenciais_Tempo"], cadastro)

    if "Unidade_Temperatura" in request.data:
        cadastro.Unidade_Temperatura = request.data["Unidade_Temperatura"]

    cadastro.save()

    return Response(status=status.HTTP_200_OK)

@api_view(['POST','PATCH'])
def GetAndUpdate(request):
    if request.method == 'POST':
        return FazerLogin(request)
    elif request.method == 'PATCH':
        return AtualizarCadastro(request)

@api_view(['POST',])
def CreateAccount(request):
    if request.method == 'POST':
        return NovoCadastro(request)


