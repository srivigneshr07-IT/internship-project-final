#!/usr/bin/env python3
"""Export database listings to CSV for ML model training"""

from database.connection import get_session
from database.models import MarketPrice
import pandas as pd
from datetime import datetime

def export_data():
    print("🔄 Connecting to database...")
    session = get_session().__enter__()
    
    print("📊 Fetching all listings...")
    listings = session.query(MarketPrice).all()
    
    print(f"✅ Found {len(listings)} listings")
    
    # Convert to DataFrame
    data = []
    for l in listings:
        data.append({
            'brand': l.brand,
            'model': l.model,
            'year': l.year,
            'kilometers': l.kilometers,
            'fuel': l.fuel,
            'transmission': l.transmission,
            'city': l.city,
            'owner_type': 'First',  # Default (not in current schema)
            'price': l.price,
            'source': l.source if hasattr(l, 'source') else 'unknown'
        })
    
    df = pd.DataFrame(data)
    
    # Add derived features
    df['car_age'] = 2026 - df['year']
    
    # Data quality report
    print("\n📈 DATA QUALITY REPORT:")
    print(f"Total records: {len(df)}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nPrice range: ₹{df['price'].min():,.0f} - ₹{df['price'].max():,.0f}")
    print(f"Average price: ₹{df['price'].mean():,.0f}")
    print(f"\nYear range: {df['year'].min()} - {df['year'].max()}")
    print(f"\nTop brands:\n{df['brand'].value_counts().head(10)}")
    print(f"\nTop cities:\n{df['city'].value_counts().head(10)}")
    print(f"\nFuel types:\n{df['fuel'].value_counts()}")
    print(f"\nTransmission:\n{df['transmission'].value_counts()}")
    
    # Save to CSV
    filename = f'training_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(filename, index=False)
    print(f"\n✅ Exported to {filename}")
    
    return df, filename

if __name__ == "__main__":
    df, filename = export_data()
