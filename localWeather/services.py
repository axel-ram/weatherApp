import requests
from django.conf import settings
from .models import City
from .constants import LocalWeatherConstants as const
def weatherAPIlist(device):
    cities = City.objects.filter(device__device=device.device)
    weather_report = []
    for city in cities:
        response = requests.get(settings.API_URL.format(city.name)).json()
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
    return weather_report

def addNewCity(device, new_city):
    error_msg = ''
    
    cityListFromDevice = City.objects.filter(device__device=device.device) 
    print("rns",cityListFromDevice.count())
    if cityListFromDevice.count() < 3:
        print("in limit")
        existing_city = cityListFromDevice.filter(name__iexact=new_city).count()
        if not existing_city:
            response = requests.get(settings.API_URL.format(new_city)).json()
            if response.get('cod') == 200:
                new_city = City.objects.create(name=response.get("name",""), device = device)
                new_city.save()
            else:
                error_msg = const.incorrectCityName
        else:
            error_msg = const.duplicateCity
    else:
        error_msg = const.cityLimit3
    return error_msg