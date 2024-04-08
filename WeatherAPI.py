import requests

# WeatherAPI class to get current and forecast weather data
class WeatherAPI:
    # Constructor to initialize the API key
    def __init__(self, api_key):
        self.api_key = api_key

    # Method to get current weather data
    def get_current_weather(self, city):
        # API endpoint to get current weather data
        api_endpoint = "https://api.weatherapi.com/v1/current.json"
        response = requests.get(api_endpoint, params={"key": self.api_key, "q": city})

        # Check if the response is successful
        if response.status_code == 200:
            weather_data = response.json()
        else:
            print("Error:", response.status_code)
        
        # Return the weather data
        return weather_data
    
    # Method to get forecast weather data
    def get_forecast_weather(self, city, days=3):
        # API endpoint to get forecast weather data
        api_endpoint = "https://api.weatherapi.com/v1/forecast.json"
        response = requests.get(api_endpoint, params={"key": self.api_key, "q": city, "days": days})

        # Check if the response is successful
        if response.status_code == 200:
            forecast_data = response.json()
        else:
            print("Error:", response.status_code)
        
        # Return the forecast data
        return forecast_data
    

# Main function to test the WeatherAPI class
def __main__():
    # Create an instance of WeatherAPI class
    weather = WeatherAPI("93de58fb29a54413a6064558240804")
    city = "London"
    # Get current weather data
    current_weather = weather.get_current_weather(city)
    print(current_weather)

# Run the main function   
if __name__ == "__main__":
    __main__()