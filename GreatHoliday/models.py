from django.db import models

class Preferencias_Paises(models.Model):
    NomePais = models.CharField(max_length=100)

    def __str__(self):
        return self.NomePais

class Preferencias_Clima(models.Model):
    TipoTempo = models.CharField(max_length=100)
    """Clima_Pais = models.ForeignKey(Preferencias_Paises, on_delete=models.CASCADE)""" """Problema na ForeignKey!! Vou resolver na faculdade."""

    def __str__(self):
        return self.TipoTempo

class Usuario(models.Model):
    Email = models.CharField(max_length=100)
    Nome = models.CharField(max_length=100)
    Senha = models.CharField(max_length=50)
    Unidade_Temperatura = models.CharField
    Usuario_Nome_Pais = models.ManyToManyField(Preferencias_Paises)
    Usuario_Clima_Prefenrencia = models.ManyToManyField(Preferencias_Clima)
    
    def __str__(self):
        return self.Nome