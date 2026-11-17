# AgriAI – Machine Learning Fertilizer Recommendation Engine

## 1. Overview & Agronomic Basis
The **AgriAI Fertilizer Recommendation Engine** provides precision, farm-tailored fertilizer advisory for major crops cultivated across the agro-climatic zones of **Andhra Pradesh, India**.

It marries **Machine Learning Classification** with **Scientific Nutrient Balancing Equations** derived from:
- **Acharya N.G. Ranga Agricultural University (ANGRAU)** *Package of Practices for Field and Horticultural Crops*.
- **Indian Council of Agricultural Research (ICAR)** guidelines for Soil Test Crop Response (STCR).
- **National Soil Health Card Portal (Government of India)** nutrient deficiency thresholds.

---

## 2. Technical Architecture & Methodology

```
Farm Soil Test Inputs
(N, P, K, pH, Soil Type, Moisture, OC, Acreage)
               │
               ▼
┌─────────────────────────────────┐
│     Machine Learning Branch     │
│   (Random Forest Classifier)    │
│  Predicts Optimal Formulation   │
│   e.g. Urea + DAP + MOP + Zn    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│       Agronomic Engine          │
│   (Nutrient Deficit & Bag Math) │
│ - Target RDF vs Soil Fertility  │
│ - Commercial Product Quantities │
│ - 50 kg Bag Counts for Acreage  │
│ - Growth Split Schedule (1-4)   │
│ - Lime / Gypsum Soil Amendments │
└────────────────┬────────────────┘
                 │
                 ▼
    Full Farmer-Facing Advisory
```

---

## 3. Recommended Doses of Fertilizers (RDF) Standards
Values in kg/ha ($N : P_2O_5 : K_2O$):
- **Paddy (Rice):** 120 : 60 : 40 (3 split applications, Zinc Sulphate indicated)
- **Cotton:** 150 : 60 : 60 (4 split applications)
- **Chillies:** 150 : 60 : 60 (4 split applications, Zinc Sulphate indicated)
- **Groundnut:** 20 : 40 : 50 (Basal single application)
- **Maize:** 120 : 60 : 50 (3 split applications, Zinc Sulphate indicated)
- **Bengal Gram:** 20 : 50 : 0 (Legume basal application)
- **Sugarcane:** 250 : 100 : 120 (4 split applications)

---

## 4. Commercial Product Calculations
Commercial fertilizers supply nutrients at standard concentrations:
1. **DAP (Diammonium Phosphate):** Supplies $18\% \text{ N}$ and $46\% P_2O_5$.
   $$\text{DAP Required (kg/ha)} = \frac{\text{Adjusted } P_2O_5}{0.46}$$
2. **Urea:** Supplies $46\% \text{ N}$.
   $$\text{N from DAP} = \text{DAP (kg/ha)} \times 0.18$$
   $$\text{Urea Required (kg/ha)} = \frac{\max(0, \text{Adjusted N} - \text{N from DAP})}{0.46}$$
3. **MOP (Muriate of Potash):** Supplies $60\% K_2O$.
   $$\text{MOP Required (kg/ha)} = \frac{\text{Adjusted } K_2O}{0.60}$$

---

## 5. Soil Amendments
- **Acidic Soils ($pH < 6.0$):** Requires Agricultural Lime ($\text{CaCO}_3$) at $\approx 500 \text{ kg/ha}$.
- **Alkaline/Saline Soils ($pH > 8.2$):** Requires Agricultural Gypsum ($\text{CaSO}_4$) at $\approx 1000 \text{ kg/ha}$.
