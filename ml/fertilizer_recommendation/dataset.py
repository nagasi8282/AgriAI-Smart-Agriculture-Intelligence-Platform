"""
AgriAI Machine Learning - Fertilizer Recommendation Dataset Generator
Generates realistic, scientifically calibrated soil test and fertilizer formulation data
representative of Andhra Pradesh agro-climatic conditions and ANGRAU agronomic practices.
"""

import os
import random
import numpy as np
import pandas as pd
from typing import Optional

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

CROPS = ["Paddy (Rice)", "Cotton", "Chillies", "Groundnut", "Maize", "Bengal Gram", "Sugarcane"]
SOIL_TYPES = ["Black Cotton", "Coastal Alluvial", "Red Sandy Loam", "Laterite"]

def generate_fertilizer_dataset(num_samples: int = 1200, output_path: Optional[str] = None) -> pd.DataFrame:
    """
    Generate synthetic soil-crop-fertilizer dataset with grounded agronomic rules.
    """
    records = []
    for _ in range(num_samples):
        crop = random.choice(CROPS)
        soil_type = random.choice(SOIL_TYPES)
        
        # Soil test parameters based on regional AP soil dynamics
        if soil_type == "Black Cotton":
            ph = round(np.random.normal(7.8, 0.5), 1)
            nitrogen = round(np.random.normal(240, 50), 1)
            phosphorus = round(np.random.normal(16, 6), 1)
            potassium = round(np.random.normal(290, 60), 1)
            oc = round(np.random.uniform(0.35, 0.75), 2)
            moisture = round(np.random.uniform(35, 65), 1)
        elif soil_type == "Coastal Alluvial":
            ph = round(np.random.normal(7.1, 0.4), 1)
            nitrogen = round(np.random.normal(290, 60), 1)
            phosphorus = round(np.random.normal(22, 7), 1)
            potassium = round(np.random.normal(210, 50), 1)
            oc = round(np.random.uniform(0.45, 0.85), 2)
            moisture = round(np.random.uniform(40, 75), 1)
        elif soil_type == "Red Sandy Loam":
            ph = round(np.random.normal(6.3, 0.6), 1)
            nitrogen = round(np.random.normal(210, 45), 1)
            phosphorus = round(np.random.normal(12, 5), 1)
            potassium = round(np.random.normal(160, 40), 1)
            oc = round(np.random.uniform(0.25, 0.60), 2)
            moisture = round(np.random.uniform(25, 55), 1)
        else:  # Laterite
            ph = round(np.random.normal(5.6, 0.5), 1)
            nitrogen = round(np.random.normal(190, 40), 1)
            phosphorus = round(np.random.normal(9, 4), 1)
            potassium = round(np.random.normal(130, 35), 1)
            oc = round(np.random.uniform(0.30, 0.65), 2)
            moisture = round(np.random.uniform(20, 50), 1)
            
        # Constrain to realistic boundaries
        ph = max(4.5, min(9.5, ph))
        nitrogen = max(60.0, min(550.0, nitrogen))
        phosphorus = max(5.0, min(80.0, phosphorus))
        potassium = max(50.0, min(500.0, potassium))
        oc = max(0.15, min(1.20, oc))
        
        # Agronomic Decision Rule for optimal formulation label
        if ph < 6.0:
            formulation = "Agricultural Lime + DAP + MOP"
        elif ph > 8.2:
            formulation = "Agricultural Gypsum + Urea + DAP + MOP"
        elif crop in ["Groundnut", "Bengal Gram"]:
            formulation = "DAP + MOP (Legume Base)"
        elif crop in ["Paddy (Rice)", "Maize", "Sugarcane"] and (nitrogen < 260 or phosphorus < 14):
            formulation = "Urea + DAP + MOP + Zinc Sulphate"
        elif soil_type in ["Red Sandy Loam", "Laterite"] and phosphorus < 12:
            formulation = "Urea + SSP + MOP"
        elif crop in ["Cotton", "Chillies"]:
            formulation = "NPK Complex 20-20-0-13 + MOP"
        else:
            formulation = "Urea + DAP + MOP"
            
        records.append({
            "crop": crop,
            "soil_type": soil_type,
            "nitrogen_kg_ha": nitrogen,
            "phosphorus_kg_ha": phosphorus,
            "potassium_kg_ha": potassium,
            "soil_ph": ph,
            "organic_carbon_pct": oc,
            "moisture_pct": moisture,
            "recommended_formulation": formulation,
        })
        
    df = pd.DataFrame(records)
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Generated {len(df)} fertilizer recommendation samples -> {output_path}")
    return df

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample", "fertilizer_recommendation_sample.csv")
    generate_fertilizer_dataset(num_samples=1500, output_path=out_file)
