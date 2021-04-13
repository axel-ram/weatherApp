from django.shortcuts import render, redirect
from django.conf import settings
import requests
from .models import City, Device
from .forms import CityForm
import uuid
from .services import weatherAPIlist, addNewCity
from .constants import LocalWeatherConstants as const
def index(request):
    message = ''
    messageClass = ''
    cityForm = CityForm()
    deviceUUID = request.COOKIES.get('device',str(uuid.uuid1()))
    
    device, created = Device.objects.get_or_create(device=deviceUUID)
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            error_msg = addNewCity(device, new_city)
        if error_msg:
            message = error_msg
            messageClass = const.messageClassDanger
        else:
            message  = const.citySuccessfullyAdded
            messageClass = const.messageClassSuccess
    
    weatherReport = weatherAPIlist(device)
    
    context = {
        'deviceUUID' : deviceUUID,
        'cityForm': cityForm,
        'weatherReport': weatherReport,
        'message' : message,
        'messageClass' : messageClass
    }
    return render(request, 'localWeather/index.html', context)

def deleteCity(request, city_name):
    device = request.COOKIES['device']
    device, created = Device.objects.get_or_create(device=device)
    if not created:
        City.objects.filter(device__device=device.device).filter(name__iexact=city_name).delete()
        return redirect('index')

def resetData(request):
    device = request.COOKIES['device']
    device, created = Device.objects.get_or_create(device=device)
    City.objects.filter(device__device=device.device).delete()
    return redirect('index')