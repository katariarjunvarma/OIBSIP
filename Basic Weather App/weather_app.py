import requests

def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an error for bad status codes
        data = response.json()
        
        if data["cod"] != 200:
            return None, f"Error: {data['message']}"
        
        weather = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
        return weather, None
    except requests.exceptions.RequestException as e:
        return None, f"Error fetching data: {str(e)}"

def display_weather(city, weather):
    print(f"\nWeather in {city.title()}:")
    print(f"Temperature: {weather['temperature']}°C")
    print(f"Humidity: {weather['humidity']}%")
    print(f"Conditions: {weather['description'].title()}")

def main():
    api_key = "8beb6da7834fde220c10830445cb9c67"  # Your OpenWeatherMap API key
    print("Welcome to the Weather App!")
    
    while True:
        city = input("\nEnter a city name (or 'quit' to exit): ").strip()
        
        if city.lower() == "quit":
            print("Goodbye!")
            break
        
        if not city:
            print("Error: Please enter a city name.")
            continue
        
        weather, error = get_weather(city, api_key)
        
        if weather:
            display_weather(city, weather)
        else:
            print(error)

if __name__ == "__main__":
    main()