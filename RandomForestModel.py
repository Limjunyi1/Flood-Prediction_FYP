# Import the required libraries for our flood prediction model
from pandas import get_dummies, read_csv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import shap

# Define the RandomForestModel class
class RandomForestModel:
    """
    Author: LimJunYi
    Date: 2024-04-09
    A class to represent a Random Forest model for flood prediction.
    """
    
    def __init__(self):
        """
        Created by: LimJunYi
        Initialization for the random forest model.
        """
        self.model = None
        self.X_test = None
        self.y_test = None
        self.city_altitude = {} # Dictionary to store city names and altitudes
        self.train()

    def data_preprocessing(self, dataset):
        """
        Created by: LimJunYi
        Preprocess the Bangladesh Flood Weather Data for training the Random Forest model.
        """
        # Read the data into a dataframe
        dataset = read_csv(dataset)

        # Iterate over the dataset to extract city names and altitudes, later use it to map the altitudes to the city names for Weather API returns
        self.city_altitude = dataset.groupby('Station_Names')['ALTITUDE (m)'].first().to_dict()

        # Drop columns that are not needed or not provided by the Weather API
        dataset = dataset.drop(['Sl', 'Rainfall (cm)', 'Bright_Sunshine (hours/day)', 'Station_Number', 'X_COR', 'Y_COR', 'Period'], axis=1)

        # One-hot encode the 'Station_Names' variable (same as pivoting a column)
        dataset_encoded = get_dummies(dataset)

        # Since Weather API does not contains some cities, we need to drop the columns that are not in the API response
        dataset_encoded = dataset_encoded.drop(['Station_Names_Srimangal', 'Station_Names_Kutubdia'], axis=1)
        
        return dataset_encoded
        
    def train(self):
        """
        Created by: LimJunYi
        Train the Random Forest model using the Bangladesh Flood Weather Data.
        """
        # Preprocess the data
        dataset_encoded = self.data_preprocessing('BangladeshFloodWeatherData.csv')

        # dependent variable = 'Flood?', independent variables = all other columns
        X = dataset_encoded.drop('Flood?', axis=1)  # Independent variables
        y = dataset_encoded['Flood?']  # Dependent variable

        # Split the data into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=32625510)
        self.X_test = X_test
        self.y_test = y_test

        # Create a RandomForestClassifier
        self.model = RandomForestClassifier(n_estimators=200, random_state=32625510)

        # Train the model using the training sets
        self.model.fit(X_train, y_train)
    
    def predict(self, new_data):
        # Make predictions
        predictions = self.model.predict(new_data)
        return predictions
    
    def evaluate(self, X_test, y_test):
        # Predict the test set
        y_pred = self.model.predict(X_test)

        # Calculate the accuracy of the model
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy
    
    def get_feature_importance(self):
        # Get the feature importances
        feature_importances = self.model.feature_importances_
        return feature_importances
    
    def predict_proba(self, weather_data):
        if self.model is None:
            raise Exception("Model is not trained yet. Train the model before prediction.")
        
        probabilities = self.model.predict_proba(weather_data)
        predictions = self.model.predict(weather_data)
        result = []

        for pred, prob in zip(predictions, probabilities):
            if pred == 1:  # flood
                result.append(('flood', prob[1]))
            else:  # no flood
                result.append(('no flood', prob[0]))
        return result
    
    def XAI_explain(self, X_test):
        # Initialize the SHAP explainer
        explainer = shap.Explainer(self.model)

        # Calculate SHAP values for the test set
        shap_values = explainer(X_test)

        return shap_values

# Testing the RandomForestPrediction class
def main():
    # Create an instance of the RandomForestPrediction class
    model = RandomForestModel()

    # Get the test data from the instance
    X_test = model.X_test
    y_test = model.y_test

    # Evaluate the model and get the accuracy score
    accuracy = model.evaluate(X_test, y_test)
    print(f"Accuracy: {accuracy}")

    # # XAI Explanation
    # shap_values = model.XAI_explain(X_test)
    # shap.summary_plot(shap_values, X_test)

    # Get the feature importances
    feature_importances = model.get_feature_importance()

    # Sort the feature importances in descending order
    sorted_importances = sorted(zip(X_test.columns, feature_importances), key=lambda x: x[1], reverse=True)
    print("Feature Importances:")
    for feature, importance in sorted_importances:
        print(f"{feature}: {importance}")
    

if __name__ == "__main__":
    main()