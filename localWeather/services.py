import requests
from django.conf import settings
from .models import City
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