import requests
import json
from datetime import datetime, timedelta
import pandas as pd

# WeatherAPI class to get current and forecast weather data
class WeatherAPI:
    # Constructor to initialize the API key
    def __init__(self, api_key):
        self.api_key = api_key

    
    # Method to get forecast weather data
    def get_data_from_api(self, city, days = 1):
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
    
    def count_date(self, current, days):
        # Get the current date
        date = datetime.strptime(current, "%Y-%m-%d %H:%M")

        # Extract the date
        date = date.date()

        # Calculate the future date
        future_date = date + timedelta(days-1)

        # Return the future date
        return future_date.strftime("%Y-%m-%d")
    
    # Method to process the retrived data
    def get_weather_data(self, city, days = 1):

        # Get the forecast data from the API
        data = self.get_data_from_api(city, days)

        # Check for days
        if days > 1:
            date = self.count_date(data["location"]["localtime"], days)
        else:
            date = data["location"]["localtime"].split(" ")[0]

        # Extract the required data from the response
        city = data["location"]["name"]
        year = date.split("-")[0]
        month = date.split("-")[1]
        max_temp = data["forecast"]["forecastday"][-1]["day"]["maxtemp_c"]
        min_temp = data["forecast"]["forecastday"][-1]["day"]["mintemp_c"]
        avg_temp = data["forecast"]["forecastday"][-1]["day"]["avgtemp_c"]
        rainfall_mm = data["forecast"]["forecastday"][-1]["day"]["totalprecip_mm"]
        rainfall_cm = rainfall_mm / 10
        relative_humidity = data["forecast"]["forecastday"][-1]["day"]["avghumidity"]
        wind_speed_kph = data["forecast"]["forecastday"][-1]["day"]["maxwind_kph"]
        wind_speed_mps = wind_speed_kph / 3.6

        sum = 0
        for i in range(24):
            sum += data["forecast"]["forecastday"][-1]["hour"][i]["cloud"]
        avg_cloud = sum / 24

        cloud_coverage = avg_cloud / 12.5

        latitude = data["location"]["lat"]
        longitude = data["location"]["lon"]
        period = year + "." + month


    

        # Create a dictionary to store the extracted data
        weather_data = {
            "Station_Names": city,
            "Year": year,
            "Month": month,
            "Max_Temp (°C)": max_temp,
            "Min_Temp (°C)": min_temp,
            "Avg_Temp (°C)": avg_temp,
            "Rainfall (mm)": rainfall_mm,
            "Rainfall (cm)": rainfall_cm,
            "Relative_Humidity (%)": relative_humidity,
            "Wind_Speed (m/s)": wind_speed_mps,
            "Cloud_Coverage (Okta)": cloud_coverage,
            "Latitude": latitude,
            "Longitude": longitude,
            "Period": period
        }

        weather_data_df = pd.DataFrame(weather_data, index=[1])

        # Return the extracted data
        return weather_data_df
    

# Main function to test the WeatherAPI class
def __main__():
    # Create an instance of WeatherAPI class
    weather = WeatherAPI("93de58fb29a54413a6064558240804")
    city = "Barisal"

    # weather = weather.get_data_from_api(city,3)

    # print(json.dumps(weather, indent = 6))
    weather = weather.get_weather_data(city, 3)
    print(weather)

    # with open("forecast.json", "w") as outfile:
        # outfile.write(json.dumps(weather, indent = 6))

# Run the main function   
if __name__ == "__main__":
    __main__()