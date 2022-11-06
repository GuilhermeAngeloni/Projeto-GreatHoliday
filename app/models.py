from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=20)
    ra = models.IntegerField()

class Disciplina(models.Model):
    nome = models.CharField(max_length=50)
    horas = models.IntegerField()
    aluno_disciplina = models.ManyToManyField(Aluno)
