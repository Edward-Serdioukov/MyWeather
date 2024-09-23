import requests

import requests

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
        
        # Преобразуем температуру в градусы Цельсия
        temperature_celsius = main['temp'] - 273.15
        
        return {
            'temperature': round(temperature_celsius, 2),  # Округляем до 2 знаков после запятой
            'pressure': main['pressure'],
            'humidity': main['humidity'],
            'wind_speed': wind['speed'],
            'description': weather_description
        }
    else:
        return None


if __name__ == "__main__":
    city = input("Enter city name: ")
    weather = get_weather(city)
    if weather:
        print(f"Temperature: {weather['temperature']}")
        print(f"Pressure: {weather['pressure']}")
        print(f"Humidity: {weather['humidity']}")
        print(f"Wind Speed: {weather['wind_speed']}")
        print(f"Description: {weather['description']}")
    else:
        print("City not found!")
        
