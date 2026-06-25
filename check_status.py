#!/usr/bin/env python3
"""Check scraping status"""

from database.connection import get_session
from database.models import MarketPrice
from sqlalchemy import func
from datetime import datetime, timedelta

session = get_session().__enter__()

print("\n" + "="*80)
print("📊 DATABASE STATUS")
print("="*80)

# Total
total = session.query(MarketPrice).count()
print(f"\nTotal Listings: {total}")

# By source
print("\n📁 By Source:")
sources = session.query(
    MarketPrice.source,
    func.count(MarketPrice.id).label('count')
).group_by(MarketPrice.source).all()

for source, count in sources:
    pct = count/total*100
    print(f"   {source}: {count} ({pct:.1f}%)")

# By brand
print("\n🚗 Top 15 Brands:")
brands = session.query(
    MarketPrice.brand,
    func.count(MarketPrice.id).label('count')
).group_by(MarketPrice.brand).order_by(func.count(MarketPrice.id).desc()).limit(15).all()

for brand, count in brands:
    print(f"   {brand}: {count}")

# Luxury vs Popular
luxury_brands = ['BMW', 'Mercedes', 'Audi', 'Jaguar', 'Land Rover', 'Volvo', 'Porsche', 'Lexus', 'Mini']
luxury_count = session.query(MarketPrice).filter(
    MarketPrice.brand.in_(luxury_brands)
).count()
popular_count = total - luxury_count

print(f"\n🎯 Summary:")
print(f"   Popular Cars: {popular_count} ({popular_count/total*100:.1f}%)")
print(f"   Luxury Cars: {luxury_count} ({luxury_count/total*100:.1f}%)")

# Recent additions
one_hour_ago = datetime.utcnow() - timedelta(hours=1)
recent = session.query(MarketPrice).filter(
    MarketPrice.last_seen_at >= one_hour_ago
).count()

print(f"\n⏱️  Added in last hour: {recent}")

print("\n" + "="*80)
