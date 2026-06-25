#!/usr/bin/env python3
"""Quick test: Spinny with Selenium"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from etl.extract.spinny_adapter import SpinnyAdapter

print("🧪 Testing Spinny with Selenium...")
print("="*80)

adapter = SpinnyAdapter()

# Test Mumbai (1 page only)
print("\n📍 Testing: Mumbai (1 page)")
listings = adapter.scrape(city='Mumbai', max_pages=1)

print(f"\n✅ Scraped {len(listings)} listings")

if len(listings) > 0:
    print("\n📊 Sample listing:")
    sample = listings[0]
    print(f"   Brand: {sample.brand}")
    print(f"   Model: {sample.model}")
    print(f"   Year: {sample.year}")
    print(f"   Price: ₹{sample.price:,}")
    print(f"   Fuel: {sample.fuel}")
    print(f"   Transmission: {sample.transmission}")
    print("\n✅ Spinny scraper working with Selenium!")
else:
    print("\n❌ No listings found - scraper needs debugging")

print("="*80)
