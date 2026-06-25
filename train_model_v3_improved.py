#!/usr/bin/env python3
"""Train XGBoost model v3.1 with regularization, luxury oversampling, and ensemble"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.utils import resample
import xgboost as xgb
import pickle
import glob

# Find the latest training data file
files = glob.glob('training_data_*.csv')
latest_file = max(files)
print(f"📂 Loading data from {latest_file}")

df = pd.read_csv(latest_file)
print(f"✅ Loaded {len(df)} records")

# ===== FIX #2: LUXURY CAR OVERSAMPLING =====
print("\n🔧 Applying luxury car oversampling...")
luxury_brands = ['Mercedes-Benz', 'BMW', 'Audi', 'Jaguar', 'Land Rover', 'Porsche', 'Volvo']
luxury_df = df[df['brand'].isin(luxury_brands)]
non_luxury_df = df[~df['brand'].isin(luxury_brands)]

print(f"  Original luxury cars: {len(luxury_df)} ({len(luxury_df)/len(df)*100:.1f}%)")

# Oversample luxury to reach ~20% of dataset
target_luxury_count = int(len(df) * 0.20)
if len(luxury_df) < target_luxury_count:
    luxury_upsampled = resample(luxury_df, 
                                n_samples=target_luxury_count, 
                                random_state=42,
                                replace=True)
    df = pd.concat([non_luxury_df, luxury_upsampled]).reset_index(drop=True)
    print(f"  After oversampling: {len(luxury_upsampled)} luxury cars ({len(luxury_upsampled)/len(df)*100:.1f}%)")
    print(f"  Total dataset: {len(df)} records")

# Feature engineering
print("\n🔧 Feature engineering...")
df['brand_tier'] = df['brand'].map({
    'Mercedes-Benz': 'luxury', 'BMW': 'luxury', 'Audi': 'luxury', 'Jaguar': 'luxury',
    'Land Rover': 'luxury', 'Porsche': 'luxury', 'Volvo': 'luxury',
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

# ===== FIX #1: ADD REGULARIZATION TO REDUCE OVERFITTING =====
print("\n🚀 Training XGBoost model v3.1 with regularization...")
model_v3_improved = xgb.XGBRegressor(
    n_estimators=200,
    max_depth=5,              # Reduced from 7
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=3,       # Added - prevents overfitting
    reg_alpha=0.1,            # L1 regularization
    reg_lambda=1.0,           # L2 regularization
    gamma=0.1,                # Minimum loss reduction
    random_state=42,
    n_jobs=-1
)

model_v3_improved.fit(X_train, y_train)
print("✅ Training complete")

# Evaluate v3.1
print("\n📊 MODEL v3.1 EVALUATION:")
y_pred_train = model_v3_improved.predict(X_train)
y_pred_test = model_v3_improved.predict(X_test)

print("\nTrain Set:")
print(f"  MAE: ₹{mean_absolute_error(y_train, y_pred_train):,.0f}")
print(f"  RMSE: ₹{np.sqrt(mean_squared_error(y_train, y_pred_train)):,.0f}")
print(f"  R² Score: {r2_score(y_train, y_pred_train):.4f}")

print("\nTest Set:")
mae_v3 = mean_absolute_error(y_test, y_pred_test)
rmse_v3 = np.sqrt(mean_squared_error(y_test, y_pred_test))
r2_v3 = r2_score(y_test, y_pred_test)
mape_v3 = np.mean(np.abs((y_test - y_pred_test) / y_test)) * 100

print(f"  MAE: ₹{mae_v3:,.0f}")
print(f"  RMSE: ₹{rmse_v3:,.0f}")
print(f"  R² Score: {r2_v3:.4f}")
print(f"  MAPE: {mape_v3:.2f}%")

# ===== FIX #3: CREATE ENSEMBLE WITH v2 =====
print("\n🔗 Loading model v2 for ensemble...")
try:
    with open('models/vehicle_price_model_v2.pkl', 'rb') as f:
        model_v2_data = pickle.load(f)
    model_v2 = model_v2_data['model']
    
    # Get v2 predictions
    y_pred_v2 = model_v2.predict(X_test)
    
    # Ensemble: 60% v2 (better R²) + 40% v3.1 (better MAPE)
    y_pred_ensemble = 0.6 * y_pred_v2 + 0.4 * y_pred_test
    
    mae_ensemble = mean_absolute_error(y_test, y_pred_ensemble)
    rmse_ensemble = np.sqrt(mean_squared_error(y_test, y_pred_ensemble))
    r2_ensemble = r2_score(y_test, y_pred_ensemble)
    mape_ensemble = np.mean(np.abs((y_test - y_pred_ensemble) / y_test)) * 100
    
    print("\n📊 ENSEMBLE MODEL (60% v2 + 40% v3.1):")
    print(f"  MAE: ₹{mae_ensemble:,.0f}")
    print(f"  RMSE: ₹{rmse_ensemble:,.0f}")
    print(f"  R² Score: {r2_ensemble:.4f}")
    print(f"  MAPE: {mape_ensemble:.2f}%")
    
    ensemble_available = True
except Exception as e:
    print(f"⚠️  Could not load v2 model: {e}")
    ensemble_available = False

# Feature importance
print("\n🎯 TOP 10 FEATURE IMPORTANCE (v3.1):")
importance = pd.DataFrame({
    'feature': features,
    'importance': model_v3_improved.feature_importances_
}).sort_values('importance', ascending=False)
print(importance.head(10).to_string(index=False))

# Sample predictions comparison
print("\n🧪 SAMPLE PREDICTIONS COMPARISON (Test Set):")
sample_indices = np.random.choice(len(X_test), 5, replace=False)
for idx in sample_indices:
    actual = y_test.iloc[idx]
    pred_v3 = y_pred_test[idx]
    error_v3 = abs(actual - pred_v3) / actual * 100
    
    if ensemble_available:
        pred_ens = y_pred_ensemble[idx]
        error_ens = abs(actual - pred_ens) / actual * 100
        print(f"  Actual: ₹{actual:,.0f} | v3.1: ₹{pred_v3:,.0f} ({error_v3:.1f}%) | Ensemble: ₹{pred_ens:,.0f} ({error_ens:.1f}%)")
    else:
        print(f"  Actual: ₹{actual:,.0f} | v3.1: ₹{pred_v3:,.0f} ({error_v3:.1f}%)")

# Save model v3.1
print("\n💾 Saving model v3.1...")
model_data = {
    'model': model_v3_improved,
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
    'version': 'v3.1',
    'trained_on': latest_file,
    'metrics': {
        'mae': mae_v3,
        'rmse': rmse_v3,
        'r2': r2_v3,
        'mape': mape_v3
    },
    'improvements': [
        'Regularization (L1=0.1, L2=1.0)',
        'Luxury car oversampling to 20%',
        'Reduced max_depth to 5',
        'Added min_child_weight=3'
    ]
}

with open('models/vehicle_price_model_v3_improved.pkl', 'wb') as f:
    pickle.dump(model_data, f)
print("✅ Model v3.1 saved")

# Save ensemble model if available
if ensemble_available:
    print("\n💾 Saving ensemble model...")
    ensemble_data = {
        'model_v2': model_v2,
        'model_v3': model_v3_improved,
        'weights': {'v2': 0.6, 'v3': 0.4},
        'encoders': model_data['encoders'],
        'features': features,
        'version': 'ensemble_v2_v3',
        'metrics': {
            'mae': mae_ensemble,
            'rmse': rmse_ensemble,
            'r2': r2_ensemble,
            'mape': mape_ensemble
        }
    }
    
    with open('models/vehicle_price_model_ensemble.pkl', 'wb') as f:
        pickle.dump(ensemble_data, f)
    print("✅ Ensemble model saved")

# Summary comparison
print("\n" + "="*60)
print("📊 FINAL COMPARISON SUMMARY")
print("="*60)
print(f"{'Metric':<15} {'v3.1 (New)':<20} {'Ensemble':<20}")
print("-"*60)
print(f"{'MAPE':<15} {mape_v3:>18.2f}%  {mape_ensemble if ensemble_available else 'N/A':>18}")
print(f"{'R² Score':<15} {r2_v3:>18.4f}  {r2_ensemble if ensemble_available else 'N/A':>18}")
print(f"{'MAE':<15} ₹{mae_v3:>17,.0f}  ₹{mae_ensemble if ensemble_available else 0:>17,.0f}")
print("="*60)

if ensemble_available:
    if r2_ensemble > r2_v3 and mape_ensemble < mape_v3:
        print("✅ RECOMMENDATION: Use ENSEMBLE model (best of both worlds)")
    elif r2_v3 > 0.65:
        print("✅ RECOMMENDATION: Use v3.1 model (good balance)")
    else:
        print("⚠️  RECOMMENDATION: Use v2 model (more reliable)")
else:
    if r2_v3 > 0.65:
        print("✅ RECOMMENDATION: Use v3.1 model")
    else:
        print("⚠️  RECOMMENDATION: Use v2 model (more reliable)")

print("\n🎉 Training complete!")
