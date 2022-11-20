from django.db import models
import json
import datetime

class Cadastro(models.Model):
    ID = models.AutoField(primary_key=True)
    Nome = models.CharField(max_length=100)
    Email = models.CharField(max_length=100, unique=True)
    Senha = models.CharField(max_length=100)
    Unidade_Temperatura = models.CharField(max_length=1)
    token = models.CharField(max_length=100)
    Token_Validade = models.DateTimeField(default=datetime.datetime(1900, 1, 1))

    def ToJson(self):
        j = {}
        paises = []
        climas = []
        j["ID"] = self.ID
        j["Nome"] = self.Nome
        j["Email"] = self.Email
        j["Unidade_Temperatura"] = self.Unidade_Temperatura

        for i in self.preferencias_paises_set.all():
            paises.append(i.cod_pais)

        for i in self.preferenciais_tempo_set.all():
            climas.append(i.tipo_tempo)

        j["Preferencias_Paises"] = paises
        j["Preferenciais_Tempo"] = climas

        return j

class Preferencias_Paises(models.Model):
    ID_Cadastro = models.AutoField(primary_key=True)
    cod_pais = models.CharField(max_length=10)
    cadastro = models.ForeignKey(Cadastro, on_delete=models.CASCADE)

class Preferenciais_Tempo(models.Model):
    ID_Cadastro = models.AutoField(primary_key=True)
    tipo_tempo = models.CharField(max_length=50)
    cadastro = models.ForeignKey(Cadastro, on_delete=models.CASCADE)