import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)


import requests
import datetime

def get_weather(city):
    api_key = "6a9eedc6772205944011d6cbf0b0323f"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}"
    
    response = requests.get(complete_url)
    
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        wind = data['wind']
        weather_description = data['weather'][0]['description']
        icon_code = data['weather'][0]['icon']  # Код иконки погоды
        day = datetime.datetime.fromtimestamp(data['dt']).strftime('%A')
        
        
        # Преобразуем температуру в градусы Цельсия
        temperature_celsius = main['temp'] - 273.15
        
        # Преобразуем давление в мм рт. ст.
        pressure_mm_hg = main['pressure'] * 0.75006375541921
        
        return {
            'day': day,
            'city': city,
            'temperature': round(temperature_celsius, 2),
            'pressure': round(pressure_mm_hg, 2),
            'humidity': main['humidity'],
            'wind_speed': wind['speed'],
            'description': weather_description,
            'icon': f"http://openweathermap.org/img/wn/{icon_code}@2x.png"  # URL иконки
        }
    else:
        return None
    
def get_weather_week(city):
    api_key = "6a9eedc6772205944011d6cbf0b0323f"
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}"
    geo_response = requests.get(geocoding_url)

    if geo_response.status_code == 200:
        geo_data = geo_response.json()
        if len(geo_data) == 0:
            return None
        
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        
        weather_url = f"http://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={api_key}"
        response = requests.get(weather_url)
        
        if response.status_code == 200:
            data = response.json()
            daily_forecast = []
            
            for day in data['daily']:
                # Преобразование метки времени в день недели
                day_name = datetime.datetime.fromtimestamp(day['dt']).strftime('%A')
                
                daily_forecast.append({
                    'day': day_name,  # Передаем уже отформатированное имя дня
                    'temperature': day['temp']['day'] - 273.15,
                    'pressure': day['pressure'] * 0.75006375541921,
                    'humidity': day['humidity'],
                    'wind_speed': day['wind_speed'],
                    'description': day['weather'][0]['description'],
                    'icon': f"http://openweathermap.org/img/wn/{day['weather'][0]['icon']}@2x.png"
                })
            
            return {
                'city': city,
                'forecast': daily_forecast
            }
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    city_weather = get_weather(city)
    if city_weather:
        return render_template('weather.html', city_weather=city_weather)
    else:
        return render_template('index.html', error="City not found.")

@app.route('/four-cities-day', methods=['GET'])
def four_cities_day():
    cities = ['Milan', 'Venezia', 'Prague', 'Marianske Lazne']
    cities_weather = []
    
    for city in cities:
        weather_data = get_weather(city)
        if weather_data:
            cities_weather.append(weather_data)
    
    return render_template('four_cities_day.html', cities_weather=cities_weather)

@app.route('/four-cities-week', methods=['GET'])
def four_cities_week():
    cities = ['Milan', 'Venezia', 'Prague', 'Marianske Lazne']
    cities_weather = []
    
    for city in cities:
        weather_data = get_weather_week(city)
        if weather_data:
            cities_weather.append(weather_data)
    
    return render_template('four_cities_week.html', cities_weather=cities_weather)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 3000)))
    #app.run(debug=True,host='0.0.0.0')

