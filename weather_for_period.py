import requests
import datetime

api_key = "6a9eedc6772205944011d6cbf0b0323f"


def get_coordinates(city, api_key):
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}"
    response = requests.get(geocoding_url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return data[0]['lat'], data[0]['lon']
    return None, None

def get_weather_for_period(lat, lon, start_date, days_ahead, api_key):
    weather_data = []
    start_dt = datetime.datetime.strptime(start_date, "%d.%m.%Y")

    for i in range(0, days_ahead, 7):
        forecast_dt = start_dt + datetime.timedelta(days=i)
        weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={api_key}"
        response = requests.get(weather_url)
        
        if response.status_code == 200:
            data = response.json()
            for day in data['daily']:
                day_date = datetime.datetime.fromtimestamp(day['dt'])
                if day_date >= forecast_dt and day_date < forecast_dt + datetime.timedelta(days=7):
                    weather_data.append({
                        'date': day_date.strftime('%Y-%m-%d'),
                        'temperature': day['temp']['day'] - 273.15,
                        'pressure': day['pressure'] * 0.75006375541921,
                        'humidity': day['humidity'],
                        'wind_speed': day['wind_speed'],
                        'description': day['weather'][0]['description'],
                        'icon': f"http://openweathermap.org/img/wn/{day['weather'][0]['icon']}@2x.png"
                    })
        else:
            print(f"Failed to retrieve data: {response.status_code}")
    
    return weather_data

def display_weather(weather_data):
    if weather_data:
        for day in weather_data:
            print(f"Date: {day['date']}")
            print(f"Temperature: {day['temperature']:.2f} °C")
            print(f"Pressure: {day['pressure']:.2f} mm Hg")
            print(f"Humidity: {day['humidity']} %")
            print(f"Wind Speed: {day['wind_speed']} m/s")
            print(f"Description: {day['description']}")
            print("Icon URL:", day['icon'])
            print("-" * 40)
    else:
        print("No weather data available for the specified period.")

# Example usage
city = "Minsk"
start_date = "03.10.2024"
days_ahead = 14  # Получаем данные на 14 дней (2 недели)

lat, lon = get_coordinates(city, api_key)
if lat and lon:
    weather_data = get_weather_for_period(lat, lon, start_date, days_ahead, api_key)
    display_weather(weather_data)
else:
    print("Unable to get coordinates for the city.")
