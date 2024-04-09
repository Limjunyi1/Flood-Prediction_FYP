import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from pandas import read_csv, get_dummies

df = read_csv('BangladeshFloodWeatherData.csv')
df = df.drop('Sl', axis=1) # column 'Sl' has no meaning, just row number
print(df.isna().sum()) # check for missing values
print(df.head())

# One-hot encode the 'Station_Names' variable (same as pivoting a column)
df = get_dummies(df, columns=['Station_Names'])

# Target variable = 'Flood?', features = all other columns
X = df.drop('Flood?', axis=1)
y = df['Flood?']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build a Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Use SHAP to explain test set predictions
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Plot the SHAP values
shap.summary_plot(shap_values, X_test)
