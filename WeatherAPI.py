import requests
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
            return None
        
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
    def get_weather_data(self, city_input, days = 1):

        # Get the forecast data from the API
        data = self.get_data_from_api(city_input, days)

        if data is None:
            return None

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
            "Year": int(year),
            "Month": int(month),
            "Max_Temp (°C)": float(max_temp),
            "Min_Temp (°C)": float(min_temp),
            "Avg_Temp (°C)": float(avg_temp),
            "Rainfall (mm)": float(rainfall_mm),
            "Relative_Humidity (%)": float(relative_humidity),
            "Wind_Speed (m/s)": float(wind_speed_mps),
            "Cloud_Coverage (Okta)": float(cloud_coverage),
            "LATITUDE": float(latitude),
            "LONGITUDE": float(longitude),
            "Station_Names_Barisal": city == "Barisal",
            "Station_Names_Bhola": city == "Bhola",
            "Station_Names_Bogra": city == "Bogra",
            "Station_Names_Chandpur": city == "Chandpur",
            "Station_Names_Chittagong (City-Ambagan)": city_input == "Chittagong (City-Ambagan)" and city == "Chittagong",
            "Station_Names_Chittagong (IAP-Patenga)": city_input == "Chittagong (IAP-Patenga)" and city == "Chittagong",
            "Station_Names_Comilla": city == "Comilla",
            "Station_Names_Cox's Bazar": city == "Cox's Bazar",
            "Station_Names_Dhaka": city == "Dhaka",
            "Station_Names_Dinajpur": city == "Dinajpur",
            "Station_Names_Faridpur": city == "Faridpur",
            "Station_Names_Feni": city == "Feni",
            "Station_Names_Hatiya": city == "Hatiya",
            "Station_Names_Ishurdi": city == "Ishurdi",
            "Station_Names_Jessore": city == "Jessore",
            "Station_Names_Khepupara": city == "Khepupara",
            "Station_Names_Khulna": city == "Khulna",
            "Station_Names_Madaripur": city == "Madaripur",
            "Station_Names_Maijdee Court": city == "Maijdee Court",
            "Station_Names_Mongla": city == "Mongla",
            "Station_Names_Mymensingh": city == "Mymensingh",
            "Station_Names_Patuakhali": city == "Patuakhali",
            "Station_Names_Rajshahi": city == "Rajshahi",
            "Station_Names_Rangamati": city == "Rangamati",
            "Station_Names_Rangpur": city == "Rangpur",
            "Station_Names_Sandwip": city == "Sandwip",
            "Station_Names_Satkhira": city == "Satkhira",
            "Station_Names_Sitakunda": city == "Sitakunda",
            "Station_Names_Sylhet": city == "Sylhet",
            "Station_Names_Tangail": city == "Tangail",
            "Station_Names_Teknaf": city == "Teknaf",
            "Station_Names": city,
            "Rainfall (cm)": rainfall_cm,
            "Period": period
        }

        weather_data_df = pd.DataFrame(weather_data, index=[1])

        # Return the extracted data
        return weather_data_df
    

# Main function to test the WeatherAPI class
def __main__():
    # Create an instance of WeatherAPI class
    weather = WeatherAPI("93de58fb29a54413a6064558240804")
    city = "Chittagong (IAP-Patenga)"

    weather = weather.get_weather_data(city, 3)
    print(weather, city)

# Run the main function   
if __name__ == "__main__":
    __main__()