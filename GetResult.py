from io import BytesIO
from pandas import get_dummies
import WeatherAPI
import RandomForestModel
import datetime
import shap
import os
import matplotlib.pyplot as plt

class GetResult:
    """
    Author: LimJunYi
    Date Created: 2024-04-09
    A class to represent a GetResult object for getting flood prediction results.
    """

    def __init__(self):
        """
        Created by: LimJunYi
        Initialization for the GetResult object.
        """
        # Check if the API key is None
        if os.environ.get("WEATHER_API_KEY") is None:
            raise ValueError("Please set up the 'WEATHER_API_KEY' environment variable with your API key.")
        
        # Please set the environment variable 'WEATHER_API_KEY' with the API key in ur system!!!
        self.weather_api = WeatherAPI.WeatherAPI(os.environ.get("WEATHER_API_KEY"))
        self.model = RandomForestModel.RandomForestModel()
        
    def preprocess_data(self, weather_data):
        """
        Created by: LimJunYi
        Preprocess the weather data for prediction.
        """
        # Adding the 'ALTITUDE (m)' column to the weather data since API does not retrieve the altitude
        weather_data.insert(11, 'ALTITUDE (m)', weather_data['Station_Names'].map(self.model.city_altitude))
        # Drop columns that are not needed for prediction
        weather_data = weather_data.drop(['Station_Names', 'Rainfall (cm)', 'Period'], axis=1)

        return weather_data

    def get_prediction_result(self, city, date):
        """
        Created by: LimJunYi
        Get the prediction result for the given city and date.
        The result will return whether there will be a flood or not and the probability of the prediction.
            Along with the SHAP values for each feature.
        """
        # Check if the date is within the next 14 days or today
        current_date = datetime.date.today()
        input_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        days_difference = (input_date - current_date).days
        
        # Validate the days difference
        if days_difference < 0 or days_difference > 14:
            raise ValueError("Invalid date. Please enter a date within the next 14 days or today.")
        
        weather_data = self.weather_api.get_weather_data(city, days_difference)  # Call the weather API function
        preprocessed_data = self.preprocess_data(weather_data)                   # Preprocess the weather data
        result = self.model.predict_proba(preprocessed_data)                     # Get the prediction result

        # Explain the prediction using SHAP
        shap_result = self.SHAP_explain(preprocessed_data)

        return result, shap_result
    
    def SHAP_explain(self, data):
        """
        Created by: LimJunYi
        Explain the prediction using SHAP tree explainer.
        """
        # Create a tree explainer for the random forest model
        explainer = shap.TreeExplainer(self.model.model)

        # Explain the prediction using SHAP
        shap_values = explainer.shap_values(data)

        # Output the SHAP values for each feature
        shap_table = []
        for i, feature in enumerate(data.columns):
            # Remove the 'Station_Name' prefix from the feature names
            if feature.startswith('Station_Names'):
                feature = feature.split('_')[-1]
            # Second column is for 'no flood' and third column is for 'flood'
            shap_table.append([f"{feature}", f"{shap_values[0, i, 0]}", f"{shap_values[0, i, 1]}"])

        return shap_table

    def plot_shap_result(self, shap_table, prediction):
        """
        Created by: LimJunYi
        Plot the SHAP values for the prediction result.
        Modified by: Cheng Tze Pin
        Output the graph as an image file.
        """
        # Get the predictors
        # Remove the 'Station_Name' prefix from the feature names
        features = [f[0].split('_')[-1] if f[0].startswith('Station_Names') else f[0] for f in shap_table]
        
        # Plot the bar graph based on prediction
        if prediction == "no flood":
            # Get SHAP values for "no flood" prediction
            no_flood_values = [float(f[1].split()[0]) for f in shap_table]

            # Get the maximum and minimum SHAP values and their corresponding features
            max_shap_value, max_feature = max(zip(no_flood_values, features))
            min_shap_value, min_feature = min(zip(no_flood_values, features))

            plt.figure(figsize=(12, 8))
            plt.bar(features, no_flood_values, label='Features Relevances to No Flood')
            plt.xlabel('Features')
            plt.ylabel('SHAP Values')
            plt.title('SHAP Values for No Flood Prediction')
            plt.axhline(y=max_shap_value, color='r', linestyle='--', label=f'Most Positive Influence: {max_shap_value:.3f} ({max_feature})')
            plt.axhline(y=min_shap_value, color='g', linestyle='--', label=f'Most Negative Influence: {min_shap_value:.3f} ({min_feature})')
        elif prediction == "flood":
            # Get SHAP values for "flood" prediction
            flood_values = [float(f[2].split()[0]) for f in shap_table]

            # Get the maximum and minimum SHAP values and their corresponding features
            max_shap_value, max_feature = max(zip(flood_values, features))
            min_shap_value, min_feature = min(zip(flood_values, features))

            plt.figure(figsize=(12, 8))
            plt.bar(features, flood_values, label='Features Relevances to Flood')
            plt.xlabel('Features')
            plt.ylabel('SHAP Values')
            plt.title('SHAP Values for Flood Prediction')
            plt.axhline(y=max_shap_value, color='r', linestyle='--', label=f'Most Positive Influence: {max_shap_value:.3f} ({max_feature})')
            plt.axhline(y=min_shap_value, color='g', linestyle='--', label=f'Most Negative Influence: {min_shap_value:.3f} ({min_feature})')
        else:
            raise ValueError("Invalid prediction value. Please provide 'no flood' or 'flood'.")

        plt.legend()
        plt.xticks(rotation=90)
        plt.tight_layout()
        
        # Save the plot as an image file
        img_bytes = BytesIO()
        plt.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        
        return img_bytes

    
def main():
    """
    Created by: LimJunYi
    Main function to test the GetResult class.
    """
    # Create an instance of GetResult class
    result = GetResult()

    # Get user input
    city = "Dhaka"
    date = "2024-05-10"

    try:
        # Get the prediction result and SHAP values
        prediction, shap_table = result.get_prediction_result(city, date)
        print("Prediction:", prediction)
        print("SHAP values:", shap_table)

        # Plot the SHAP values
        result.plot_shap_result(shap_table, prediction[0])

    except ValueError as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
    
