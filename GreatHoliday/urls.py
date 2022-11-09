from django.urls import path
from GreatHoliday import views

urlpatterns = [
    path('', views.index),
    path('search', views.search, name='search'),
    path('weather/<str:location>', views.requestWeather)
]
