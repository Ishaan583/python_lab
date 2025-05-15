import requests
import json
import matplotlib.pyplot as plt

API_KEY = "2932136b489b44f0bcc142701242311"  # Replace with your WeatherAPI key

def get_weather(city, api_key):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': city,
        'aqi': 'no'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': data['location']['name'],
            'temperature': data['current']['temp_c'],
            'description': data['current']['condition']['text'],
            'humidity': data['current']['humidity']
        }
        return weather
    else:
        print(f"Error {response.status_code}: {response.json().get('error', {}).get('message', 'Unknown error')}")
        return None

def get_forecast(city, api_key):
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        'key': api_key,
        'q': city,
        'days': 5,
        'aqi': 'no',
        'alerts': 'no'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        forecast = []
        for day in data['forecast']['forecastday']:
            for hour in day['hour']:
                forecast.append({
                    'datetime': hour['time'],
                    'temperature': hour['temp_c'],
                    'description': hour['condition']['text']
                })
        return forecast
    else:
        print(f"Error {response.status_code}: {response.json().get('error', {}).get('message', 'Unknown error')}")
        return None

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

def plot_forecast(forecast):
    dates = [item['datetime'] for item in forecast]
    temperatures = [item['temperature'] for item in forecast]
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temperatures, marker='o')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Date and Time")
    plt.ylabel("Temperature (°C)")
    plt.title("5-Day Temperature Forecast")
    plt.tight_layout()
    plt.show()

def main():
    while True:
        print("\nWeather App")
        print("1. Current Weather")
        print("2. 5-Day Weather Forecast")
        print("3. Save Weather Data to File")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            city = input("Enter city name: ")
            weather_data = get_weather(city, API_KEY)
            if weather_data:
                print(f"\nCity: {weather_data['city']}")
                print(f"Temperature: {weather_data['temperature']}°C")
                print(f"Description: {weather_data['description']}")
                print(f"Humidity: {weather_data['humidity']}%")
            else:
                print("Error fetching current weather data.")
        
        elif choice == '2':
            city = input("Enter city name: ")
            forecast_data = get_forecast(city, API_KEY)
            if forecast_data:
                print("\n5-Day Weather Forecast:")
                for item in forecast_data[:10]:  # Display first 10 records (hourly)
                    print(f"{item['datetime']} - Temp: {item['temperature']}°C, Desc: {item['description']}")
                plot_forecast(forecast_data[:10])
            else:
                print("Error fetching forecast data.")
        
        elif choice == '3':
            city = input("Enter city name: ")
            weather_data = get_weather(city, API_KEY)
            forecast_data = get_forecast(city, API_KEY)
            if weather_data and forecast_data:
                combined_data = {
                    "current_weather": weather_data,
                    "forecast": forecast_data
                }
                save_to_file(combined_data, f"{city}_weather.json")
            else:
                print("Error fetching data for saving.")
        
        elif choice == '4':
            print("Exiting the Weather App. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
