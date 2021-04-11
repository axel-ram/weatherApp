from django.shortcuts import render, redirect
from django.conf import settings
import requests
from .models import City
from .forms import CityForm

def index(request, **kwargs):
    message = ''
    error_msg = ''
    message_class = ''
    # print("response", request.)
    if request.method == 'POST':
        print(request.POST)
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city = City.objects.filter(name__iexact=new_city).count()
            
            if not existing_city:
                response = requests.get(settings.API_URL.format(new_city)).json()
                if response.get('cod') == 200:
                    form.save()
                else:
                    error_msg = "City name is not correct."
            else:
                error_msg = "City is already added."

        print("RNS",error_msg)
        if error_msg:
            message = error_msg
            message_class = 'is-danger'
        else:
            message  = "City added successfully"
            message_class = 'is-success'

    city_form = CityForm()
    cities = City.objects.all()
    weather_report = []
    for city in cities:
        response = requests.get(settings.API_URL.format(city)).json()
        #print(response)
        try:
            city_weather = {
                "city" : response.get("name",""),
                "temperature" : response.get("main","").get("temp",0),
                "description" : response.get("weather","")[0].get("description","").title(),
                "icon" : response.get("weather","")[0].get("icon","")
            }
            weather_report.append(city_weather)
        except Exception as e:
            print(e)

    context = {
        'weather_report' : weather_report,
        'city_form': city_form,
        'message' : message,
        'message_class' : message_class
    }
    return render(request, 'localWeather/index.html', context)

def deleteCity(request, city_name):
    print(city_name)
    City.objects.filter(name__iexact=city_name).delete()
    return redirect('index')
