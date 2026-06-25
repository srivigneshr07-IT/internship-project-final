#!/usr/bin/env python3
"""
Scrape Luxury Cars - NON-INTERACTIVE VERSION
Runs automatically without user input (for nohup)
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
    'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Pune', 'Chennai'
]

def check_current_data():
    """Check current database status"""
    print("\n" + "="*80)
    print("📊 CURRENT DATABASE STATUS")
    print("="*80)
    
    session = get_session().__enter__()
    total = session.query(MarketPrice).count()
    
    from sqlalchemy import func
    luxury_count = session.query(MarketPrice).filter(
        MarketPrice.brand.in_(LUXURY_BRANDS)
    ).count()
    
    print(f"\nTotal Listings: {total}")
    print(f"Luxury Cars: {luxury_count} ({luxury_count/total*100:.1f}%)")
    
    return total, luxury_count

def main():
    """Main execution - NO USER INPUT"""
    print("\n" + "="*80)
    print("🎯 LUXURY CAR DATA COLLECTION - AUTOMATIC MODE")
    print("="*80)
    print("\nRunning without user input (nohup mode)")
    print("Will scrape: CarDekho + Cars24 + Spinny")
    print("="*80)
    
    # Check before
    total_before, luxury_before = check_current_data()
    
    # Phase 1: CarDekho + Cars24
    print("\n" + "="*80)
    print("🚗 PHASE 1: Scraping CarDekho + Cars24")
    print("="*80)
    
    pipeline = ETLPipeline()
    pipeline.run(cities=LUXURY_CITIES, sources=['cardekho', 'cars24'])
    
    print(f"\n✅ CarDekho + Cars24 complete!")
    
    # Check progress
    total_after_phase1, luxury_after_phase1 = check_current_data()
    
    # Phase 2: Spinny (AUTOMATIC - no asking)
    print("\n" + "="*80)
    print("🚗 PHASE 2: Scraping Spinny")
    print("="*80)
    
    pipeline.run(cities=LUXURY_CITIES, sources=['spinny'])
    
    print(f"\n✅ Spinny complete!")
    
    # Final check
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
    
    print("\n🎯 Next Step: Train model v3")
    print("="*80)

if __name__ == "__main__":
    main()
