import requests
import datetime

api_key = "2KMLGQGHEE2K4GBSFHE5APR9T"

def get_weather_for_period(city, start_date, end_date, api_key):
    # Формируем URL для запроса
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{start_date}/{end_date}?unitGroup=metric&include=days&key={api_key}&contentType=json"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_data = []
        
        for day in data['days']:
            weather_data.append({
                'date': day['datetime'],
                'temperature': day['temp'],
                'pressure': day['pressure'],
                'humidity': day['humidity'],
                'wind_speed': day['windspeed'],
                'description': day['conditions'],
                'icon': f"https://www.visualcrossing.com/static/img/weathericons/{day['icon']}.svg"
            })
        
        return weather_data
    else:
        print("Failed to retrieve data:", response.status_code)
        return None

def display_weather(weather_data):
    if weather_data:
        for day in weather_data:
            print(f"Date: {day['date']}")
            print(f"Temperature: {day['temperature']} °C")
            #print(f"Pressure: {day['pressure']} hPa")
            #print(f"Humidity: {day['humidity']} %")
            #print(f"Wind Speed: {day['wind_speed']} m/s")
            print(f"Description: {day['description']}")
            print("Icon URL:", day['icon'])
            print("-" * 40)
    else:
        print("No weather data available for the specified period.")

# Пример использования
city = "Milan"
start_date = "2024-10-03"
end_date = "2024-10-07"  # Прогноз на 14 дней вперед

weather_data = get_weather_for_period(city, start_date, end_date, api_key)
display_weather(weather_data)
