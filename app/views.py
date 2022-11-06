from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Ok")

def template(request):
    my_list = ["a", "b", "c"]
    ctx = {"my_list": my_list}
    return render(request, template_name="index.html", context=ctx)

def form(request):
    if request.method == 'POST':
        print('é um post')
        nome = request.POST['nome']
        return HttpResponse("Seu nome é " + nome)
    return render(request, template_name="form.html")