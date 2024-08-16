from django.shortcuts import render
from .models import WeatherData
import requests

def index(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        api_key = '4ba5c659252cce49627398f212f71f56'
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                'city': data['name'],
                'country_code': data['sys']['country'],
                'coordinate': f"{data['coord']['lon']} {data['coord']['lat']}",
                'temp': data['main']['temp'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'main': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }

            # Save the weather data to the database
            WeatherData.objects.create(
                city=weather_data['city'],
                country_code=weather_data['country_code'],
                coordinate=weather_data['coordinate'],
                temperature=weather_data['temp'],
                pressure=weather_data['pressure'],
                humidity=weather_data['humidity'],
                main=weather_data['main'],
                description=weather_data['description'],
                icon=weather_data['icon'],
            )

            return render(request, 'index.html', weather_data)
        else:
            return render(request, 'index.html', {'error': 'City not found'})

    return render(request, 'index.html')
