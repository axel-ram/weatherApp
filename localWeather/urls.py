from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<str:city_name>', views.deleteCity, name='delete'),
    path('reset', views.resetData, name='resetData'),
]
