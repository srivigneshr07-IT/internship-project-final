# Updated System Architecture with AWS Bedrock

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (HTML/CSS/JS)                      │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ Image Upload │  │  Smart Form  │  │   Results    │            │
│  │   Component  │  │  Auto-fill   │  │   Display    │            │
│  └──────┬───────┘  └──────┬───────┘  └──────▲───────┘            │
│         │                 │                  │                     │
└─────────┼─────────────────┼──────────────────┼─────────────────────┘
          │                 │                  │
          │ POST /vision    │ POST /predict    │ Response
          │ (image file)    │ (form data)      │ (price + details)
          │                 │                  │
┌─────────▼─────────────────▼──────────────────┴─────────────────────┐
│                    BACKEND (FastAPI)                                │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    main.py (API Routes)                      │  │
│  │  • POST /vision/analyze  • POST /predict                     │  │
│  │  • GET /brands           • GET /models/{brand}               │  │
│  │  • GET /history          • GET /metadata                     │  │
│  └────┬─────────────────────────────────────────────┬───────────┘  │
│       │                                             │              │
│       │ Image Analysis                              │ Prediction   │
│       │                                             │              │
│  ┌────▼──────────────────┐                    ┌────▼──────────┐   │
│  │  bedrock_vision.py    │                    │ predictor.py  │   │
│  │  • Base64 encode      │                    │ • Load model  │   │
│  │  • Call Bedrock API   │                    │ • Predict     │   │
│  │  • Parse JSON         │                    │ • Damage cost │   │
│  │  • Extract brand      │                    │ • Confidence  │   │
│  └────┬──────────────────┘                    └────┬──────────┘   │
│       │                                            │              │
│       │ Brand name                                 │ Uses         │
│       │                                            │              │
│  ┌────▼────────────────────────────────────────────▼──────────┐   │
│  │                    utils.py (Database)                     │   │
│  │  • SQLite operations  • Vehicle catalog  • History         │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
          │                                             │
          │ Bedrock API Call                            │ Model Load
          │                                             │
┌─────────▼─────────────────────┐         ┌────────────▼─────────────┐
│    AWS BEDROCK (Nova Lite)    │         │  XGBoost Model (Local)   │
│                               │         │                          │
│  • Image → Brand Detection    │         │  • 13 Features Input     │
│  • Returns JSON response      │         │  • Price Prediction      │
│  • Confidence: ~90%           │         │  • Trained on dataset    │
└───────────────────────────────┘         └──────────────────────────┘


═══════════════════════════════════════════════════════════════════════
                            DATA FLOW
═══════════════════════════════════════════════════════════════════════

1. USER UPLOADS IMAGE
   ↓
2. Frontend → POST /vision/analyze (image file)
   ↓
3. Backend → bedrock_vision.py
   ↓
4. AWS Bedrock Nova Lite analyzes image
   ↓
5. Returns: {"detected_brand": "Maruti", "detected_model": "Swift", ...}
   ↓
6. Frontend receives brand → searches database
   ↓
7. Frontend → GET /brands (search="Maruti")
   ↓
8. Backend → utils.py → SQLite query
   ↓
9. Returns: ["maruti suzuki"]
   ↓
10. Frontend → GET /models/maruti suzuki
    ↓
11. Backend → Returns: ["Swift", "Alto", ...]
    ↓
12. Frontend → GET /vehicle/maruti suzuki/Swift
    ↓
13. Backend → Returns: {variants, fuel, transmission, body, premium_brand}
    ↓
14. Frontend AUTO-FILLS form with all details
    ↓
15. User adds: mileage, age, damage description
    ↓
16. User clicks "Predict Price"
    ↓
17. Frontend → POST /predict (complete form data)
    ↓
18. Backend → predictor.py → XGBoost model
    ↓
19. Returns: {predicted_price, damage_cost, confidence, suggested_price}
    ↓
20. Frontend displays results + saves to history


═══════════════════════════════════════════════════════════════════════
                        KEY COMPONENTS
═══════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│ NEW: bedrock_vision.py                                              │
├─────────────────────────────────────────────────────────────────────┤
│ • get_bedrock_client() → boto3 client                               │
│ • encode_image_to_base64() → converts PIL Image                     │
│ • analyze_vehicle_image_with_bedrock() → main function              │
│   - Sends image to Nova Lite                                        │
│   - Parses JSON response                                            │
│   - Extracts brand name (first word only)                           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ UNCHANGED: predictor.py                                             │
├─────────────────────────────────────────────────────────────────────┤
│ • predict_price() → XGBoost model                                   │
│ • estimate_damage_cost() → keyword-based                            │
│ • calculate_confidence_score() → field completeness                 │
│ • calculate_transaction_price() → selling/buying modes              │
│ • calculate_dynamic_profit_margin() → risk-based                    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ UNCHANGED: utils.py                                                 │
├─────────────────────────────────────────────────────────────────────┤
│ • init_db() → SQLite initialization                                 │
│ • search_brands() → brand search with query                         │
│ • get_vehicle_details() → variants, fuel, transmission              │
│ • record_prediction() → save to history                             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ UNCHANGED: frontend/js/app.js                                       │
├─────────────────────────────────────────────────────────────────────┤
│ • analyzeVehicleImages() → calls /vision/analyze                    │
│ • autofillVehicleFromVision() → matches brand + loads models        │
│ • submitForm() → calls /predict with complete data                  │
└─────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════
                    ENVIRONMENT CONFIGURATION
═══════════════════════════════════════════════════════════════════════

.env file:
┌─────────────────────────────────────────────────────────────────────┐
│ AWS_REGION=us-east-1                                                │
│ AWS_ACCESS_KEY_ID=your_aws_access_key_here                              │
│ AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here      │
│ BEDROCK_MODEL_ID=amazon.nova-lite-v1:0                              │
└─────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════
                        SUCCESS METRICS
═══════════════════════════════════════════════════════════════════════

✅ Bedrock connection: WORKING
✅ Brand detection: 90% confidence
✅ Auto-fill flow: INTACT
✅ Price prediction: UNCHANGED
✅ All API endpoints: FUNCTIONAL
✅ Frontend integration: NO CHANGES NEEDED
✅ Complete flow: TESTED & VERIFIED

```
