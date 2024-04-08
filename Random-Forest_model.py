import pandas as pd
from pandas import get_dummies, read_csv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Read the data into a dataframe
df = read_csv('BangladeshFloodWeatherData.csv')
df = df.drop('Sl', axis=1)                          # column 'Sl' has no meaning, just row number
df = df.drop('Period', axis=1)                      # column 'Period' is just year and month combined
df = df.drop('Bright_Sunshine (hours/day)', axis = 1)

# One-hot encode the 'Station_Names' variable (same as pivoting a column)
df_encoded = get_dummies(df)

# dependent variable = 'Flood?', independent variables = all other columns
X = df_encoded.drop('Flood?', axis=1)  # Independent variables
y = df_encoded['Flood?']  # Dependent variable

# Split the data into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=32625510)

# Create a RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=32625510)

# Train the model using the training sets
clf.fit(X_train, y_train)

# Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy
print("Accuracy of this model:", accuracy_score(y_test, y_pred))

# Feature importunateness
feature_importances = pd.DataFrame({"Feature": X.columns, "Importance": clf.feature_importances_})
feature_importances = feature_importances.sort_values(by="Importance", ascending=False)
print(feature_importances)