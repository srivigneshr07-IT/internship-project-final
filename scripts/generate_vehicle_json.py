"""
=====================================================

Generate Frontend Dropdown Data

AI Powered Vehicle Valuation System

=====================================================
"""

import pandas as pd
import json

# Load cleaned dataset
df = pd.read_csv("data/vehicle_final_dataset.csv")

vehicle_dict = {}

for brand in sorted(df["oem"].unique()):

    vehicle_dict[brand] = {}

    brand_df = df[df["oem"] == brand]

    for model in sorted(brand_df["model"].unique()):

        variants = sorted(

            brand_df[brand_df["model"] == model]["variant"]

            .dropna()

            .unique()

            .tolist()

        )

        vehicle_dict[brand][model] = variants

with open(

    "frontend/js/vehicleData.json",

    "w"

) as f:

    json.dump(

        vehicle_dict,

        f,

        indent=4

    )

print("vehicleData.json created successfully!")