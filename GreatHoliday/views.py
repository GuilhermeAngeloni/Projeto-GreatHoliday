from django.shortcuts import render

def index(request):
  context={}
  return render(request, 'GreatHoliday/starter.html', context)


def search(request):
  print(request)
  context={
    'result': 'testetestestestestestsetesteesttesetstes settesestsetseteswttse'
  }
  if request.method == 'GET':
    print(request.GET)
    
  return render(request, 'GreatHoliday/starter.html', context)