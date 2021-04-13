from django.shortcuts import render, redirect
from django.conf import settings
import requests
from .models import City, Device
from .forms import CityForm
import uuid
from .services import weatherAPIlist

def index(request):
    message = ''
    error_msg = ''
    message_class = ''
    city_form = CityForm()
    deviceUUID = request.COOKIES.get('device',str(uuid.uuid1()))   
    
    device, created = Device.objects.get_or_create(device=deviceUUID)
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city = City.objects.filter(device__device=device.device).filter(name__iexact=new_city).count()
            print("rns",City.objects.filter(device__device=device.device).count())
            if City.objects.filter(device__device=device.device).count() < 3:
                if not existing_city:
                    response = requests.get(settings.API_URL.format(new_city)).json()
                    if response.get('cod') == 200:
                        new_city = City.objects.create(name=response.get("name",""), device = device)
                        new_city.save()
                    else:
                        error_msg = "City name is not correct."
                else:
                    error_msg = "City is already added."
            else:
                error_msg = "You cannot add more than 3 cities."
            
    
        if error_msg:
            message = error_msg
            message_class = 'is-danger'
        else:
            message  = "City added successfully"
            message_class = 'is-success'
    
    weather_report = weatherAPIlist(device)
    
    context = {
        'deviceUUID' : deviceUUID,
        'city_form': city_form,
        'weather_report': weather_report,
        'message' : message,
        'message_class' : message_class
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