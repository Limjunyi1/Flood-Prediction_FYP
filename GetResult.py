from pandas import get_dummies
import WeatherAPI
import RandomForestModel
import datetime

class GetResult:
    # Author: LimJunYi
    # Date: 2024-04-09

    def __init__(self):
        self.weather_api = WeatherAPI.WeatherAPI("93de58fb29a54413a6064558240804")
        self.model = RandomForestModel.RandomForestModel()

    # def get_user_input(self):
    #     # Get input from the user
        
    def preprocess_data(self, weather_data):

        weather_data['ALTITUDE (m)'] = weather_data['Station_Names'].map(self.model.city_altitude)

        weather_data = weather_data.drop(['Station_Names', 'Rainfall (cm)', 'Period'], axis=1)
        print(weather_data.columns)
        print(self.model.dataset.columns)

        return weather_data

    def get_prediction_result(self, city, date):
        current_date = datetime.date.today()
        input_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        days_difference = (input_date - current_date).days
        
        # days difference should be 0 to 14
        if days_difference < 0 or days_difference > 14:
            raise ValueError("Invalid date. Please enter a date within the next 14 days or today.")
        
        weather_data = self.weather_api.get_weather_data(city, days_difference)  # Call the weather API function
        preprocessed_data = self.preprocess_data(weather_data)
        result = self.model.predict(preprocessed_data)
        
        # return the result
        return result
    
def main():
    # Create an instance of GetResult class
    result = GetResult()

    # Get user input
    city = "Barisal"
    date = "2024-04-15"

    try:
        # Get the prediction result
        prediction = result.get_prediction_result(city, date)
        print("Prediction:", prediction)
    except ValueError as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
    
