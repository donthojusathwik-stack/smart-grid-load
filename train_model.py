import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Load dataset
df = pd.read_csv("energy.csv")

# Convert ? to NaN if present
df.replace("?", pd.NA, inplace=True)

# Convert columns to numeric
cols = [
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
    "Sub_metering_1",
    "Sub_metering_2",
    "Sub_metering_3"
]
df[cols] = df[cols].apply(pd.to_numeric)

# Drop Date & Time (basic version)
df.drop(["Date", "Time"], axis=1, inplace=True)

# Handle missing values
df.fillna(df.mean(), inplace=True)

# Features & Target
X = df.drop("Global_active_power", axis=1)
y = df["Global_active_power"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluation
pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, pred))
print("R2 Score:", r2_score(y_test, pred))

# Save model
joblib.dump(model, "energy_model.pkl")
print("Model trained & saved successfully")
