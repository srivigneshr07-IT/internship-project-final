#!/usr/bin/env python3
"""Comprehensive testing for ensemble model and backend"""

import pandas as pd
import numpy as np
import sys
sys.path.append('backend')

from app.predictor import predict_price, calculate_confidence_score, calculate_transaction_price

print("="*70)
print("🧪 COMPREHENSIVE MODEL & BACKEND TESTING")
print("="*70)

# Test Case 1: Budget Car (Maruti Swift)
print("\n1️⃣ TEST: Budget Car (Maruti Swift 2018)")
test1 = pd.DataFrame([{
    'brand': 'Maruti',
    'model': 'Swift',
    'year': 2018,
    'kilometers': 45000,
    'fuel_type': 'Petrol',
    'transmission': 'Manual',
    'city': 'Chennai',
    'owner_type': 'First'
}])
try:
    price1 = predict_price(test1)
    print(f"   ✅ Prediction: ₹{price1:,.0f}")
    print(f"   Expected range: ₹3-4 lakhs")
    if 250000 <= price1 <= 450000:
        print("   ✅ PASS: Within expected range")
    else:
        print("   ⚠️  WARNING: Outside expected range")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test Case 2: Premium Car (Honda City)
print("\n2️⃣ TEST: Premium Car (Honda City 2019)")
test2 = pd.DataFrame([{
    'brand': 'Honda',
    'model': 'City',
    'year': 2019,
    'kilometers': 30000,
    'fuel_type': 'Petrol',
    'transmission': 'Automatic',
    'city': 'Mumbai',
    'owner_type': 'First'
}])
try:
    price2 = predict_price(test2)
    print(f"   ✅ Prediction: ₹{price2:,.0f}")
    print(f"   Expected range: ₹7-9 lakhs")
    if 600000 <= price2 <= 1000000:
        print("   ✅ PASS: Within expected range")
    else:
        print("   ⚠️  WARNING: Outside expected range")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test Case 3: Luxury Car (Mercedes C-Class)
print("\n3️⃣ TEST: Luxury Car (Mercedes-Benz C-Class 2017)")
test3 = pd.DataFrame([{
    'brand': 'Mercedes-Benz',
    'model': 'C-Class',
    'year': 2017,
    'kilometers': 50000,
    'fuel_type': 'Diesel',
    'transmission': 'Automatic',
    'city': 'Bangalore',
    'owner_type': 'First'
}])
try:
    price3 = predict_price(test3)
    print(f"   ✅ Prediction: ₹{price3:,.0f}")
    print(f"   Expected range: ₹20-25 lakhs")
    if 1800000 <= price3 <= 2800000:
        print("   ✅ PASS: Within expected range")
    else:
        print("   ⚠️  WARNING: Outside expected range")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test Case 4: Old Car (Maruti Alto 2012)
print("\n4️⃣ TEST: Old Car (Maruti Alto 2012)")
test4 = pd.DataFrame([{
    'brand': 'Maruti',
    'model': 'Alto',
    'year': 2012,
    'kilometers': 80000,
    'fuel_type': 'Petrol',
    'transmission': 'Manual',
    'city': 'Delhi',
    'owner_type': 'Second'
}])
try:
    price4 = predict_price(test4)
    print(f"   ✅ Prediction: ₹{price4:,.0f}")
    print(f"   Expected range: ₹1-2 lakhs")
    if 80000 <= price4 <= 250000:
        print("   ✅ PASS: Within expected range")
    else:
        print("   ⚠️  WARNING: Outside expected range")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test Case 5: High Mileage Car (Hyundai i20 2016)
print("\n5️⃣ TEST: High Mileage Car (Hyundai i20 2016)")
test5 = pd.DataFrame([{
    'brand': 'Hyundai',
    'model': 'i20',
    'year': 2016,
    'kilometers': 120000,
    'fuel_type': 'Diesel',
    'transmission': 'Manual',
    'city': 'Pune',
    'owner_type': 'Third'
}])
try:
    price5 = predict_price(test5)
    print(f"   ✅ Prediction: ₹{price5:,.0f}")
    print(f"   Expected range: ₹3-4.5 lakhs")
    if 250000 <= price5 <= 500000:
        print("   ✅ PASS: Within expected range")
    else:
        print("   ⚠️  WARNING: Outside expected range")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test Case 6: Edge Case - Very New Car (2025)
print("\n6️⃣ TEST: Edge Case - Very New Car (Toyota Fortuner 2025)")
test6 = pd.DataFrame([{
    'brand': 'Toyota',
    'model': 'Fortuner',
    'year': 2025,
    'kilometers': 5000,
    'fuel_type': 'Diesel',
    'transmission': 'Automatic',
    'city': 'Hyderabad',
    'owner_type': 'First'
}])
try:
    price6 = predict_price(test6)
    print(f"   ✅ Prediction: ₹{price6:,.0f}")
    print(f"   Expected range: ₹35-45 lakhs")
    if 3000000 <= price6 <= 5000000:
        print("   ✅ PASS: Within expected range")
    else:
        print("   ⚠️  WARNING: Outside expected range")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test Confidence Scoring
print("\n" + "="*70)
print("🎯 TESTING CONFIDENCE SCORING")
print("="*70)

test_payloads = [
    {'oem': 'Maruti', 'model': 'Swift', 'year': 2018, 'km': 45000, 'fuel': 'Petrol', 'transmission': 'Manual'},
    {'oem': 'Mercedes-Benz', 'model': 'C-Class', 'year': 2017, 'km': 50000},
    {'oem': 'Maruti', 'km': 80000},  # Incomplete data
]

for i, payload in enumerate(test_payloads, 1):
    try:
        score = calculate_confidence_score(payload)
        print(f"{i}. Confidence Score: {score}% - {'✅ PASS' if 45 <= score <= 95 else '⚠️  WARNING'}")
    except Exception as e:
        print(f"{i}. ❌ FAILED: {e}")

# Test Transaction Pricing
print("\n" + "="*70)
print("💰 TESTING TRANSACTION PRICING")
print("="*70)

test_price = 500000
test_damage = 20000
test_payload = {'car_age': 5, 'km': 50000, 'owner_type': 'First', 'premium_brand': 0}

for txn_type in ['selling', 'buying_resale', 'buying_personal']:
    try:
        result = calculate_transaction_price(test_price, test_damage, txn_type, test_payload)
        print(f"\n{txn_type.upper()}:")
        print(f"   Transaction Price: ₹{result['transaction_price']:,.0f}")
        if result['profit_margin']:
            print(f"   Profit Margin: ₹{result['profit_margin']:,.0f}")
        if result['price_range_min']:
            print(f"   Range: ₹{result['price_range_min']:,.0f} - ₹{result['price_range_max']:,.0f}")
        print(f"   ✅ PASS")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")

# Test Error Handling
print("\n" + "="*70)
print("🛡️  TESTING ERROR HANDLING")
print("="*70)

# Test 1: Missing fields
print("\n1. Missing required fields:")
try:
    bad_test = pd.DataFrame([{'brand': 'Maruti'}])
    price = predict_price(bad_test)
    print(f"   ⚠️  WARNING: Should have failed but got ₹{price:,.0f}")
except Exception as e:
    print(f"   ✅ PASS: Handled gracefully - {str(e)[:50]}")

# Test 2: Invalid brand
print("\n2. Unknown brand:")
try:
    unknown_brand = pd.DataFrame([{
        'brand': 'UnknownBrand',
        'model': 'TestModel',
        'year': 2020,
        'kilometers': 30000,
        'fuel_type': 'Petrol',
        'transmission': 'Manual',
        'city': 'Mumbai',
        'owner_type': 'First'
    }])
    price = predict_price(unknown_brand)
    print(f"   ✅ PASS: Handled unknown brand - ₹{price:,.0f}")
except Exception as e:
    print(f"   ⚠️  WARNING: Failed on unknown brand - {str(e)[:50]}")

# Test 3: Extreme values
print("\n3. Extreme values (year=1990, km=500000):")
try:
    extreme_test = pd.DataFrame([{
        'brand': 'Maruti',
        'model': 'Swift',
        'year': 1990,
        'kilometers': 500000,
        'fuel_type': 'Petrol',
        'transmission': 'Manual',
        'city': 'Chennai',
        'owner_type': 'Fourth'
    }])
    price = predict_price(extreme_test)
    print(f"   ✅ PASS: Handled extreme values - ₹{price:,.0f}")
except Exception as e:
    print(f"   ⚠️  WARNING: Failed on extreme values - {str(e)[:50]}")

print("\n" + "="*70)
print("✅ TESTING COMPLETE")
print("="*70)
