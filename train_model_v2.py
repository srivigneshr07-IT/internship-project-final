#!/usr/bin/env python3
"""Train XGBoost model v2 with fresh market data"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import pickle
import glob

# Find the latest training data file
files = glob.glob('training_data_*.csv')
latest_file = max(files)
print(f"📂 Loading data from {latest_file}")

df = pd.read_csv(latest_file)
print(f"✅ Loaded {len(df)} records")

# Feature engineering
print("\n🔧 Feature engineering...")
df['brand_tier'] = df['brand'].map({
    'Mercedes-Benz': 'luxury', 'BMW': 'luxury', 'Audi': 'luxury', 'Jaguar': 'luxury',
    'Hyundai': 'premium', 'Honda': 'premium', 'Toyota': 'premium', 'Volkswagen': 'premium',
    'Maruti': 'budget', 'Tata': 'budget', 'Renault': 'budget', 'Datsun': 'budget'
}).fillna('mid')

df['city_tier'] = df['city'].map({
    'Mumbai': 'tier1', 'Delhi': 'tier1', 'Bangalore': 'tier1', 'Hyderabad': 'tier1',
    'Chennai': 'tier1', 'Kolkata': 'tier1', 'Pune': 'tier1', 'Ahmedabad': 'tier1'
}).fillna('tier2')

df['km_per_year'] = df['kilometers'] / (df['car_age'] + 1)

# Encode categorical variables
le_brand = LabelEncoder()
le_model = LabelEncoder()
le_fuel = LabelEncoder()
le_transmission = LabelEncoder()
le_city = LabelEncoder()
le_owner = LabelEncoder()
le_brand_tier = LabelEncoder()
le_city_tier = LabelEncoder()

df['brand_encoded'] = le_brand.fit_transform(df['brand'])
df['model_encoded'] = le_model.fit_transform(df['model'])
df['fuel_encoded'] = le_fuel.fit_transform(df['fuel'])
df['transmission_encoded'] = le_transmission.fit_transform(df['transmission'])
df['city_encoded'] = le_city.fit_transform(df['city'])
df['owner_encoded'] = le_owner.fit_transform(df['owner_type'])
df['brand_tier_encoded'] = le_brand_tier.fit_transform(df['brand_tier'])
df['city_tier_encoded'] = le_city_tier.fit_transform(df['city_tier'])

# Features and target
features = ['brand_encoded', 'model_encoded', 'year', 'kilometers', 'fuel_encoded',
            'transmission_encoded', 'city_encoded', 'owner_encoded', 'car_age',
            'brand_tier_encoded', 'city_tier_encoded', 'km_per_year']

X = df[features]
y = df['price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"✅ Train: {len(X_train)}, Test: {len(X_test)}")

# Train XGBoost model
print("\n🚀 Training XGBoost model...")
model = xgb.XGBRegressor(
    n_estimators=200,
    max_depth=7,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print("✅ Training complete")

# Evaluate
print("\n📊 MODEL EVALUATION:")
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

print("\nTrain Set:")
print(f"  MAE: ₹{mean_absolute_error(y_train, y_pred_train):,.0f}")
print(f"  RMSE: ₹{np.sqrt(mean_squared_error(y_train, y_pred_train)):,.0f}")
print(f"  R² Score: {r2_score(y_train, y_pred_train):.4f}")

print("\nTest Set:")
mae = mean_absolute_error(y_test, y_pred_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
r2 = r2_score(y_test, y_pred_test)
print(f"  MAE: ₹{mae:,.0f}")
print(f"  RMSE: ₹{rmse:,.0f}")
print(f"  R² Score: {r2:.4f}")

# Calculate percentage error
mape = np.mean(np.abs((y_test - y_pred_test) / y_test)) * 100
print(f"  MAPE: {mape:.2f}%")

# Feature importance
print("\n🎯 TOP 10 FEATURE IMPORTANCE:")
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print(importance.head(10).to_string(index=False))

# Sample predictions
print("\n🧪 SAMPLE PREDICTIONS (Test Set):")
sample_indices = np.random.choice(len(X_test), 5, replace=False)
for idx in sample_indices:
    actual = y_test.iloc[idx]
    predicted = y_pred_test[idx]
    error_pct = abs(actual - predicted) / actual * 100
    print(f"  Actual: ₹{actual:,.0f} | Predicted: ₹{predicted:,.0f} | Error: {error_pct:.1f}%")

# Save model and encoders
print("\n💾 Saving model...")
model_data = {
    'model': model,
    'encoders': {
        'brand': le_brand,
        'model': le_model,
        'fuel': le_fuel,
        'transmission': le_transmission,
        'city': le_city,
        'owner_type': le_owner,
        'brand_tier': le_brand_tier,
        'city_tier': le_city_tier
    },
    'features': features,
    'version': 'v2',
    'trained_on': latest_file,
    'metrics': {
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'mape': mape
    }
}

with open('models/vehicle_price_model_v2.pkl', 'wb') as f:
    pickle.dump(model_data, f)

print("✅ Model saved to models/vehicle_price_model_v2.pkl")
print(f"\n🎉 Model v2 training complete! MAPE: {mape:.2f}%")
