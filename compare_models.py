#!/usr/bin/env python3
"""Compare old model v1 vs new model v2 predictions"""

import pickle
import pandas as pd
from market_intelligence import MarketIntelligence
from pricing import DynamicPricingEngine

# Load model v2
print("📂 Loading model v2...")
with open('models/vehicle_price_model_v2.pkl', 'rb') as f:
    model_v2_data = pickle.load(f)

print("✅ Model v2 loaded")
print(f"   Version: {model_v2_data['version']}")
print(f"   MAPE: {model_v2_data['metrics']['mape']:.2f}%")
print(f"   R² Score: {model_v2_data['metrics']['r2']:.4f}")

# Initialize market intelligence
mi = MarketIntelligence()

# Test cases
test_cases = [
    {'brand': 'Maruti', 'model': 'Swift', 'year': 2020, 'km': 50000, 'fuel': 'Petrol', 'transmission': 'Manual', 'city': 'Chennai'},
    {'brand': 'Hyundai', 'model': 'Creta', 'year': 2019, 'km': 60000, 'fuel': 'Diesel', 'transmission': 'Manual', 'city': 'Bangalore'},
    {'brand': 'Honda', 'model': 'City', 'year': 2018, 'km': 70000, 'fuel': 'Petrol', 'transmission': 'Automatic', 'city': 'Mumbai'},
    {'brand': 'Tata', 'model': 'Nexon', 'year': 2021, 'km': 30000, 'fuel': 'Petrol', 'transmission': 'Manual', 'city': 'Delhi'},
    {'brand': 'Kia', 'model': 'Seltos', 'year': 2020, 'km': 40000, 'fuel': 'Diesel', 'transmission': 'Automatic', 'city': 'Pune'},
]

print("\n" + "="*100)
print("MODEL v2 PREDICTIONS vs MARKET DATA")
print("="*100)

def predict_v2(test_case):
    """Predict using model v2"""
    encoders = model_v2_data['encoders']
    model = model_v2_data['model']
    
    # Prepare features
    car_age = 2026 - test_case['year']
    km_per_year = test_case['km'] / (car_age + 1)
    
    brand_tier_map = {
        'Mercedes-Benz': 'luxury', 'BMW': 'luxury', 'Audi': 'luxury',
        'Hyundai': 'premium', 'Honda': 'premium', 'Toyota': 'premium',
        'Maruti': 'budget', 'Tata': 'budget', 'Renault': 'budget'
    }
    brand_tier = brand_tier_map.get(test_case['brand'], 'mid')
    
    city_tier_map = {
        'Mumbai': 'tier1', 'Delhi': 'tier1', 'Bangalore': 'tier1',
        'Hyderabad': 'tier1', 'Chennai': 'tier1', 'Pune': 'tier1'
    }
    city_tier = city_tier_map.get(test_case['city'], 'tier2')
    
    features = {
        'brand_encoded': encoders['brand'].transform([test_case['brand']])[0],
        'model_encoded': encoders['model'].transform([test_case['model']])[0],
        'year': test_case['year'],
        'kilometers': test_case['km'],
        'fuel_encoded': encoders['fuel'].transform([test_case['fuel']])[0],
        'transmission_encoded': encoders['transmission'].transform([test_case['transmission']])[0],
        'city_encoded': encoders['city'].transform([test_case['city']])[0],
        'owner_encoded': encoders['owner_type'].transform(['First'])[0],
        'car_age': car_age,
        'brand_tier_encoded': encoders['brand_tier'].transform([brand_tier])[0],
        'city_tier_encoded': encoders['city_tier'].transform([city_tier])[0],
        'km_per_year': km_per_year
    }
    
    X = pd.DataFrame([features])
    return model.predict(X)[0]

for i, tc in enumerate(test_cases, 1):
    print(f"\n{'='*100}")
    print(f"TEST CASE {i}: {tc['year']} {tc['brand']} {tc['model']} | {tc['km']:,} km | {tc['fuel']} | {tc['transmission']} | {tc['city']}")
    print(f"{'='*100}")
    
    # Model v2 prediction
    try:
        pred_v2 = predict_v2(tc)
        print(f"✅ Model v2 Prediction: ₹{pred_v2:,.0f}")
    except Exception as e:
        print(f"❌ Model v2 Error: {e}")
        pred_v2 = None
    
    # Market intelligence
    market_data = mi.get_market_insights(tc['brand'], tc['model'], tc['year'], tc['city'])
    
    if market_data['sample_size'] > 0:
        stats = market_data['statistics']
        print(f"\n📊 Market Intelligence:")
        print(f"   Sample Size: {market_data['sample_size']}")
        print(f"   Confidence: {market_data['confidence']}")
        print(f"   Average: ₹{stats['average_price']:,.0f}")
        print(f"   Median: ₹{stats['median_price']:,.0f}")
        print(f"   Range: ₹{stats['min_price']:,.0f} - ₹{stats['max_price']:,.0f}")
        
        if pred_v2:
            diff_avg = abs(pred_v2 - stats['average_price']) / stats['average_price'] * 100
            diff_median = abs(pred_v2 - stats['median_price']) / stats['median_price'] * 100
            print(f"\n🎯 Model v2 Accuracy:")
            print(f"   vs Market Average: {diff_avg:.1f}% difference")
            print(f"   vs Market Median: {diff_median:.1f}% difference")
            
            if diff_avg < 15:
                print(f"   ✅ EXCELLENT - Within 15% of market")
            elif diff_avg < 25:
                print(f"   ⚠️  GOOD - Within 25% of market")
            else:
                print(f"   ❌ NEEDS IMPROVEMENT - >25% difference")
    else:
        print(f"\n📊 Market Intelligence: No data available")

print("\n" + "="*100)
print("COMPARISON COMPLETE")
print("="*100)
