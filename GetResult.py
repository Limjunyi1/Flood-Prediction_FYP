from pandas import get_dummies
import WeatherAPI
import RandomForestModel
import datetime
import shap
import matplotlib.pyplot as plt

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

        # Output the SHAP values for each feature
        shap_table = []
        for i, feature in enumerate(data.columns):
            shap_table.append([f"{feature}", f"{shap_values[0, i, 0]} (no flood)", f"{shap_values[0, i, 1]} (flood)"])

        return shap_table

    def plot_shap_result(self, shap_table, prediction):
        features = [f[0] for f in shap_table]
        
        # Plot the bar graph based on prediction
        if prediction == "no flood":
            no_flood_values = [float(f[1].split()[0]) for f in shap_table]
            plt.figure(figsize=(10, 6))
            plt.bar(features, no_flood_values, label='Features Relevances to No Flood')
            plt.xlabel('Features')
            plt.ylabel('SHAP Values')
            plt.title('SHAP Values for No Flood Prediction')
        elif prediction == "flood":
            flood_values = [float(f[2].split()[0]) for f in shap_table]
            plt.figure(figsize=(10, 6))
            plt.bar(features, flood_values, label='Features Relevances to Flood')
            plt.xlabel('Features')
            plt.ylabel('SHAP Values')
            plt.title('SHAP Values for Flood Prediction')
        else:
            raise ValueError("Invalid prediction value. Please provide 'no flood' or 'flood'.")

        plt.legend()
        plt.xticks(rotation=90)
        plt.show()

    
def main():
    # Create an instance of GetResult class
    result = GetResult()

    # Get user input
    city = "Dhaka"
    date = "2024-05-01"

    try:
        # Get the prediction result and SHAP values
        prediction, shap_table = result.get_prediction_result(city, date)
        print("Prediction:", prediction)
        print("SHAP values:", shap_table)

        result.plot_shap_result(shap_table, prediction[0])

    except ValueError as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
    
