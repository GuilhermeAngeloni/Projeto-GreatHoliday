from django.urls import path
from GreatHoliday import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('search', views.search, name='search'),
    path('weather/<str:location>', views.requestWeather),
    path('cadastrar', views.cadastrar, name='cadastrar'),
]
