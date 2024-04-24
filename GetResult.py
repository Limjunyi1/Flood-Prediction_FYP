from pandas import get_dummies
import WeatherAPI
import RandomForestModel
import datetime
import shap

class GetResult:
    # Author: LimJunYi
    # Date: 2024-04-09

    def __init__(self):
        self.weather_api = WeatherAPI.WeatherAPI("93de58fb29a54413a6064558240804")
        self.model = RandomForestModel.RandomForestModel()
        
    def preprocess_data(self, weather_data):

        weather_data.insert(11, 'ALTITUDE (m)', weather_data['Station_Names'].map(self.model.city_altitude))

        weather_data = weather_data.drop(['Station_Names', 'Rainfall (cm)', 'Period'], axis=1)

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
        result = self.model.predict_proba(preprocessed_data)

        shap_result = self.SHAP_explain(preprocessed_data)

        return result, shap_result
    
    def SHAP_explain(self, data):
        # Create a tree explainer for the random forest model
        explainer = shap.TreeExplainer(self.model.model)

        # Explain the prediction using SHAP
        shap_values = explainer.shap_values(data)

        return shap_values
    
def main():
    # Create an instance of GetResult class
    result = GetResult()

    # Get user input
    city = "Maijdee Court"
    date = "2024-05-01"

    try:
        # Get the prediction result and SHAP values
        prediction, shapr = result.get_prediction_result(city, date)
        print("Prediction:", prediction)
        print("SHAP values:", shapr)
    except ValueError as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
    
