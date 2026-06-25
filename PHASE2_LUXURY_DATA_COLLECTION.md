# Phase 2: Luxury Car Data Collection

**Date**: June 24, 2026  
**Goal**: Expand dataset from 801 → 1,150+ listings by adding luxury cars  
**Strategy**: Collect ALL data first, then train model v3 ONCE (not v3 + v4)

---

## 🎯 Plan Overview

### Current Status:
- **Total Listings**: 801
- **Luxury Cars**: ~10-20 (1-2%)
- **Popular Cars**: ~780-790 (98%)
- **Problem**: Model underestimates luxury cars (no training data)

### Target Status:
- **Total Listings**: 1,150+
- **Luxury Cars**: 250-350 (20-30%)
- **Popular Cars**: 800-900 (70-80%)
- **Result**: Balanced dataset for model v3

---

## 📋 Data Collection Plan

### Phase 2A: CarDekho + Cars24 Luxury Cars (2 hours)
**Target**: +250 luxury listings

**Sources**:
- CarDekho (primary)
- Cars24 (secondary)

**Cities**:
- Mumbai (most luxury cars)
- Delhi
- Bangalore
- Hyderabad
- Pune
- Chennai

**Brands**:
- BMW
- Mercedes-Benz
- Audi
- Jaguar
- Land Rover
- Volvo
- Porsche
- Lexus
- Mini

**Method**: Use existing CarDekho + Cars24 scrapers (already configured)

**Expected**: +250 listings (180-200 luxury)

---

### Phase 2B: Spinny All Cars (4 hours)
**Target**: +150 listings (50 luxury + 100 popular)

**Why Spinny**:
- Good luxury car inventory
- High data quality (verified cars)
- More automatic transmission cars

**Method**: Use existing Spinny adapter (currently disabled, needs enabling)

---

## 🛠️ Implementation

### Step 1: Check Current Data
```bash
cd /home/sagemaker-user/intern-project-final/ai-powered-car-cost-estimation-main
python scrape_luxury_cars.py
```

This will:
1. Show current database status
2. Calculate how many luxury cars needed
3. Display brand distribution

### Step 2: Scrape CarDekho
The script will automatically:
1. Scrape 6 luxury cities from CarDekho
2. Extract all brands (luxury + popular)
3. Add to database (deduplication automatic)
4. Show progress

**Expected**: +200-250 listings (150-200 luxury)

### Step 3: Scrape Spinny (Optional)
If needed, the script will:
1. Enable Spinny scraper
2. Scrape 6 cities
3. Add to database
4. Show final results

**Expected**: +100-150 listings (50-100 luxury)

---

## 📊 Expected Results

| Metric | Before | After CarDekho+Cars24 | After Spinny | Target |
|--------|--------|----------------------|--------------|--------|
| Total Listings | 801 | 1,050-1,100 | 1,150-1,250 | 1,150+ |
| Luxury Cars | 10-20 | 190-220 | 240-320 | 250+ |
| Luxury % | 1-2% | 18-20% | 20-26% | 20-30% |
| Popular Cars | 780-790 | 830-880 | 830-930 | 800-900 |

---

## ✅ Database Deduplication

**Automatic**: The ETL pipeline checks for duplicates before inserting:

```python
# Checks: brand + model + year + km + city + price
if listing_exists:
    update last_seen_at  # Mark as still available
else:
    insert new_listing   # Add to database
```

**Result**: 
- Existing 801 listings: Kept ✅
- New listings: Added ✅
- Duplicates: Skipped ✅

---

## 🎯 After Data Collection

### Train Model v3 (1 hour)

Once data collection is complete:

```bash
# Export expanded dataset
python export_training_data.py
# Output: training_data_YYYYMMDD_HHMMSS.csv (1,150+ rows)

# Train model v3
python train_model_v3.py
# Output: models/vehicle_price_model_v3.pkl

# Test model v3
python compare_models.py
# Compare v2 vs v3 accuracy
```

**Expected Improvements**:
- MAPE: 28.7% → 22-25% (better overall)
- Luxury car accuracy: Poor → Good (now has training data)
- Popular car accuracy: 6% → 5-8% (maintained or improved)

---

## 🚨 Important Notes

### 1. Scraping Time
- **CarDekho**: 1.5-2 hours (6 cities × 3 pages × 2 sec delay)
- **Spinny**: 2-3 hours (requires Selenium, slower)
- **Total**: 4-5 hours

### 2. Rate Limiting
- 2 second delay between requests (configured)
- If IP blocked: Wait 24 hours or use mobile hotspot
- Scrape during off-peak hours (night time)

### 3. Data Quality
- CarDekho: High quality ✅
- Spinny: High quality ✅
- Validation: Automatic (price range, year range, etc.)

### 4. Spinny Requirements
If Spinny scraping fails:
```bash
# Install Selenium
pip install selenium undetected-chromedriver

# Or skip Spinny and use CarDekho only
# Still get 1,000+ listings (16-20% luxury)
```

---

## 📁 Files

### Created:
- `scrape_luxury_cars.py` - Main scraping script
- `PHASE2_LUXURY_DATA_COLLECTION.md` - This file

### Will Create:
- `training_data_YYYYMMDD_HHMMSS.csv` - Expanded dataset (1,150+ rows)
- `models/vehicle_price_model_v3.pkl` - New model with luxury cars
- `PHASE2_COMPLETE.md` - Completion report

---

## 🎯 Success Criteria

- [x] Script created
- [ ] Current data checked
- [ ] CarDekho scraped (+200 listings)
- [ ] Spinny scraped (+150 listings) - Optional
- [ ] Total listings: 1,150+
- [ ] Luxury cars: 250+ (20-30%)
- [ ] Model v3 trained
- [ ] Accuracy improved

---

## 🚀 Next Steps

1. **Run scraping script**:
   ```bash
   python scrape_luxury_cars.py
   ```

2. **Wait for completion** (4-5 hours)

3. **Train model v3**:
   ```bash
   python train_model_v3.py
   ```

4. **Test and deploy**:
   ```bash
   python test_api_v3.py
   ```

---

## 💡 Alternative: If Scraping Fails

**Option A**: Use CarDekho only
- Still get 1,000+ listings
- 16-20% luxury cars
- Good enough for model v3

**Option B**: Manual data entry
- Find 50-100 luxury car listings manually
- Add to CSV
- Import to database

**Option C**: Use synthetic data
- Generate luxury car prices using depreciation formulas
- Based on new car prices
- Less accurate but better than nothing

---

**Status**: Ready to execute ✅  
**Estimated Time**: 5-6 hours (scraping + training)  
**Expected Result**: Model v3 with 20-30% luxury cars, improved accuracy
