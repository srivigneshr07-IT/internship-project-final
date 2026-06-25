#!/usr/bin/env python3
"""Test model v2 prediction directly"""

import pandas as pd
from backend.app.predictor import predict_price, model_data
from pricing import DynamicPricingEngine
from market_intelligence import MarketIntelligence

print(f"✅ Model loaded: {model_data.get('version')}")
print(f"   MAPE: {model_data.get('metrics', {}).get('mape', 0):.2f}%")
print(f"   R² Score: {model_data.get('metrics', {}).get('r2', 0):.4f}")

# Test case: Maruti Swift 2020, Chennai
test_data = {
    'brand': 'Maruti',
    'model': 'Swift',
    'year': 2020,
    'kilometers': 50000,
    'fuel_type': 'Petrol',
    'transmission': 'Manual',
    'owner_type': 'First',
    'city': 'Chennai',
    'car_age': 2026 - 2020,
    'myear': 2020
}

print("\n" + "="*80)
print(f"🧪 Test: {test_data['year']} {test_data['brand']} {test_data['model']}")
print(f"    {test_data['kilometers']:,} km | {test_data['fuel_type']} | {test_data['transmission']}")
print(f"    {test_data['city']} | {test_data['owner_type']} Owner")
print("="*80)

# ML Prediction
input_df = pd.DataFrame([test_data])
ml_price = predict_price(input_df)
print(f"\n💡 ML Prediction (Model v2): ₹{ml_price:,.0f}")

# Market Intelligence
mi = MarketIntelligence()
market_data = mi.get_market_insights(
    test_data['brand'],
    test_data['model'],
    test_data['year'],
    test_data['city']
)

if market_data['sample_size'] > 0:
    stats = market_data['statistics']
    print(f"\n📊 Market Intelligence:")
    print(f"   Sample Size: {market_data['sample_size']}")
    print(f"   Confidence: {market_data['confidence']}")
    print(f"   Average: ₹{stats['average_price']:,.0f}")
    print(f"   Median: ₹{stats['median_price']:,.0f}")
    
    # Calculate accuracy
    diff = abs(ml_price - stats['average_price']) / stats['average_price'] * 100
    print(f"\n🎯 Model Accuracy: {diff:.1f}% difference from market average")
    if diff < 15:
        print("   ✅ EXCELLENT - Within 15%")
    elif diff < 25:
        print("   ⚠️  GOOD - Within 25%")
    else:
        print("   ❌ NEEDS IMPROVEMENT")

# Dynamic Pricing
engine = DynamicPricingEngine()
result = engine.get_dynamic_price(
    ml_price,
    test_data['brand'],
    test_data['model'],
    test_data['year'],
    test_data['city']
)

print(f"\n💰 Dynamic Pricing (40% ML + 60% Market):")
print(f"   Final Price: ₹{result['final_price']:,.0f}")
if 'pricing_breakdown' in result and 'confidence_level' in result['pricing_breakdown']:
    print(f"   Confidence: {result['pricing_breakdown']['confidence_level']}")

print("\n✅ Model v2 integration test complete!")

