#!/usr/bin/env python3
"""
Scrape Luxury Cars from CarDekho and Spinny
Phase 2: Data Expansion - Collect all luxury listings before training v3
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from etl.run_pipeline import ETLPipeline
from etl.utils.logger import setup_logger
from database.connection import get_session
from database.models import MarketPrice

logger = setup_logger(__name__)

# Luxury brands to target
LUXURY_BRANDS = [
    'BMW', 'Mercedes', 'Audi', 'Jaguar', 'Land Rover', 
    'Volvo', 'Porsche', 'Lexus', 'Mini'
]

# Cities with most luxury cars
LUXURY_CITIES = [
    'Mumbai',      # Most luxury cars in India
    'Delhi',       # Second most
    'Bangalore',   # Tech hub, many luxury cars
    'Hyderabad',   # Growing luxury market
    'Pune',        # Near Mumbai
    'Chennai'      # South India hub
]

def check_current_data():
    """Check current database status"""
    print("\n" + "="*80)
    print("📊 CURRENT DATABASE STATUS")
    print("="*80)
    
    session = get_session().__enter__()
    
    # Total listings
    total = session.query(MarketPrice).count()
    print(f"\nTotal Listings: {total}")
    
    # Brand distribution
    from sqlalchemy import func
    brand_counts = session.query(
        MarketPrice.brand,
        func.count(MarketPrice.id).label('count')
    ).group_by(MarketPrice.brand).order_by(func.count(MarketPrice.id).desc()).all()
    
    print(f"\n📈 Brand Distribution:")
    luxury_count = 0
    popular_count = 0
    
    for brand, count in brand_counts:
        if brand in LUXURY_BRANDS:
            print(f"   {brand}: {count} (LUXURY)")
            luxury_count += count
        else:
            popular_count += count
            if count > 20:  # Only show popular brands
                print(f"   {brand}: {count}")
    
    print(f"\n🎯 Summary:")
    print(f"   Popular Cars: {popular_count} ({popular_count/total*100:.1f}%)")
    print(f"   Luxury Cars: {luxury_count} ({luxury_count/total*100:.1f}%)")
    print(f"   Target: 20-30% luxury cars")
    
    needed = int(total * 0.25) - luxury_count  # Target 25%
    print(f"\n🎯 Need to scrape: ~{max(0, needed)} more luxury listings")
    
    return total, luxury_count

def scrape_luxury_cardekho_cars24():
    """Scrape luxury cars from CarDekho and Cars24"""
    print("\n" + "="*80)
    print("🚗 PHASE 1: Scraping CarDekho + Cars24 Luxury Cars")
    print("="*80)
    
    print(f"\nTarget Cities: {', '.join(LUXURY_CITIES)}")
    print(f"Target Brands: {', '.join(LUXURY_BRANDS)}")
    print(f"\nNote: Scrapers will get all brands, we'll filter luxury in database")
    
    # Run ETL pipeline for luxury cities
    pipeline = ETLPipeline()
    
    # Scrape luxury cities with CarDekho AND Cars24
    pipeline.run(
        cities=LUXURY_CITIES,
        sources=['cardekho', 'cars24']  # Both sources
    )
    
    print(f"\n✅ CarDekho + Cars24 scraping complete!")

def scrape_luxury_spinny():
    """Scrape luxury cars from Spinny"""
    print("\n" + "="*80)
    print("🚗 PHASE 2: Scraping Spinny (All Cars)")
    print("="*80)
    
    print(f"\nTarget Cities: {', '.join(LUXURY_CITIES)}")
    print(f"\nNote: Spinny has good luxury car inventory")
    
    # Check if Spinny is enabled
    from etl.config import SOURCES
    if not SOURCES['spinny']['enabled']:
        print("\n⚠️  WARNING: Spinny scraper is disabled in config")
        print("   Reason: Requires Selenium (dynamic content)")
        print("\n   Options:")
        print("   1. Enable Spinny and run with Selenium")
        print("   2. Skip Spinny for now (use CarDekho only)")
        
        response = input("\n   Enable Spinny scraping? (y/n): ").lower()
        if response != 'y':
            print("   Skipping Spinny scraping")
            return
    
    # Run ETL pipeline for Spinny
    pipeline = ETLPipeline()
    pipeline.run(
        cities=LUXURY_CITIES,
        sources=['spinny']
    )
    
    print(f"\n✅ Spinny scraping complete!")

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("🎯 LUXURY CAR DATA COLLECTION - Phase 2")
    print("="*80)
    print("\nGoal: Expand dataset from 801 → 1,150+ listings")
    print("Strategy: Add 250-350 luxury car listings")
    print("Sources: CarDekho + Spinny")
    print("="*80)
    
    # Step 1: Check current data
    total_before, luxury_before = check_current_data()
    
    input("\n\nPress Enter to start scraping CarDekho + Cars24 luxury cars...")
    
    # Step 2: Scrape CarDekho + Cars24
    scrape_luxury_cardekho_cars24()
    
    # Check progress
    total_after_cardekho, luxury_after_cardekho = check_current_data()
    added_cardekho = total_after_cardekho - total_before
    luxury_added_cardekho = luxury_after_cardekho - luxury_before
    
    print(f"\n📊 CarDekho + Cars24 Results:")
    print(f"   Total added: {added_cardekho}")
    print(f"   Luxury added: {luxury_added_cardekho}")
    
    # Step 3: Ask about Spinny
    print("\n" + "="*80)
    response = input("\nContinue with Spinny scraping? (y/n): ").lower()
    
    if response == 'y':
        scrape_luxury_spinny()
        
        # Final check
        total_final, luxury_final = check_current_data()
        added_spinny = total_final - total_after_cardekho
        luxury_added_spinny = luxury_final - luxury_after_cardekho
        
        print(f"\n📊 Spinny Results:")
        print(f"   Total added: {added_spinny}")
        print(f"   Luxury added: {luxury_added_spinny}")
    
    # Final summary
    total_final, luxury_final = check_current_data()
    
    print("\n" + "="*80)
    print("🎉 DATA COLLECTION COMPLETE!")
    print("="*80)
    print(f"\nBefore: {total_before} listings ({luxury_before} luxury)")
    print(f"After:  {total_final} listings ({luxury_final} luxury)")
    print(f"Added:  {total_final - total_before} listings ({luxury_final - luxury_before} luxury)")
    print(f"\nLuxury %: {luxury_final/total_final*100:.1f}%")
    
    if luxury_final / total_final >= 0.20:
        print("✅ Target achieved! (20%+ luxury cars)")
    else:
        print(f"⚠️  Need {int(total_final * 0.20 - luxury_final)} more luxury listings to reach 20%")
    
    print("\n🎯 Next Step: Train model v3 with expanded dataset")
    print(f"   Command: python train_model_v3.py")
    print("="*80)

if __name__ == "__main__":
    main()
