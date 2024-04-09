from pandas import get_dummies, read_csv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

class RandomForestModel:
    # Author: LimJunYi
    # Date: 2024-04-09
    
    def __init__(self):
        self.model = None
        self.X_test = None
        self.y_test = None
        self.city_altitude = {} # Dictionary to store city names and altitudes
        self.train()

    def train(self):
        # Read the data into a dataframe
        dataset = read_csv('BangladeshFloodWeatherData.csv')

        # Iterate over the dataset to extract city names and altitudes
        for index, row in dataset.iterrows():
            city_name = row['Station_Names']
            altitude = row['ALTITUDE (m)']
            if city_name not in self.city_altitude:
                self.city_altitude[city_name] = altitude

        # Drop columns that are not needed or not provided by the Weather API
        dataset = dataset.drop(['Sl', 'Rainfall (cm)', 'Bright_Sunshine (hours/day)', 'Station_Number', 'X_COR', 'Y_COR', 'Period'], axis=1)

        # One-hot encode the 'Station_Names' variable (same as pivoting a column)
        dataset_encoded = get_dummies(dataset)

        # dependent variable = 'Flood?', independent variables = all other columns
        X = dataset_encoded.drop('Flood?', axis=1)  # Independent variables
        y = dataset_encoded['Flood?']  # Dependent variable

        # Split the data into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=32625510)
        self.X_test = X_test
        self.y_test = y_test

        # Create a RandomForestClassifier
        self.model = RandomForestClassifier(n_estimators=100, random_state=32625510)

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

    # Get the feature importances
    feature_importances = model.get_feature_importance()

    # Sort the feature importances in descending order
    sorted_importances = sorted(zip(X_test.columns, feature_importances), key=lambda x: x[1], reverse=True)

    print("Feature Importances:")
    for feature, importance in sorted_importances:
        print(f"{feature}: {importance}")

if __name__ == "__main__":
    main()