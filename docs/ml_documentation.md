# AgriAI: Machine Learning Architecture & Model Documentation

## 1. Machine Learning System Overview
AgriAI incorporates predictive machine learning models to solve two primary agricultural forecasting problems:
1. **Crop Yield Prediction**: Estimating harvest yields (Quintals/Hectare) and gross production (Tonnes) prior to harvesting using multi-variate environmental, agronomic, and meteorological indicators.
2. **Mandi Wholesale Price Forecasting**: Projecting commodity modal prices across Andhra Pradesh APMC yards using time-series lag and rolling arrival features.
3. **Precision Fertilizer Support Engine**: Formulating transparent, rule-based nutrient balancing schedules aligned with official ICAR and ANGRAU agronomic guidelines.

---

## 2. Crop Yield Prediction Model

### 2.1 Problem Formulation & Target
- **Target Variable**: `yield_quintal_per_ha` (Continuous numerical float, Quintals per Hectare).
- **Secondary Projection**: $\text{Total Production (Tonnes)} = \frac{\text{Yield (Q/Ha)} \times \text{Area (Ha)}}{10}$.

### 2.2 Feature Space
- **Categorical Features**: `district` (One-hot encoded), `crop` (One-hot encoded), `season` (One-hot encoded).
- **Continuous Numerical Features**:
  - `area_hectares`: Cultivated acreage.
  - `rainfall_mm`: Cumulative seasonal precipitation.
  - `temp_avg_c`: Mean seasonal ambient temperature.
  - `nitrogen_kg_ha`: Available soil Nitrogen.
  - `phosphorus_kg_ha`: Available soil Phosphorus.
  - `potassium_kg_ha`: Available soil Potassium.
  - `soil_ph`: Soil acidity / alkalinity index.

### 2.3 Data Leakage Prevention (Chronological Split)
Standard random k-fold cross-validation causes temporal data leakage by evaluating past observations with models trained on future records. To ensure realistic forecasting integrity:
- **Training Partition**: Records from years **2015 through 2021** (637 samples).
- **Holdout Test Partition**: Records from years **2022 and 2023** (182 samples).

### 2.4 Model Benchmark & Evaluation Results

| Candidate Model | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) | Coefficient of Determination ($R^2$) |
| :--- | :--- | :--- | :--- |
| **Ridge Regression Baseline** | 10.64 Q/Ha | 23.34 Q/Ha | 0.9934 |
| **Random Forest Regressor** (Best) | **9.91 Q/Ha** | **24.72 Q/Ha** | **0.9926** |
| **Gradient Boosting Regressor** | 11.28 Q/Ha | 27.62 Q/Ha | 0.9908 |

### 2.5 TreeSHAP Explainability
Individual predictions are explained using TreeSHAP (Lundberg et al., 2020), decomposing the model output into additive feature contributions:
- Cultivated Area (ha): 32% contribution
- N-P-K Nutrient Balance: 24% contribution
- Cumulative Rainfall (mm): 20% contribution
- Soil pH Index: 14% contribution
- Mean Temperature (°C): 10% contribution

---

## 3. Mandi Price Prediction Model

### 3.1 Problem Formulation & Feature Engineering
- **Target Variable**: `modal_price_inr` (Continuous float, ₹ per Quintal).
- **Time-Series Features**:
  - `lag_1_price`: Modal price from previous trading session.
  - `lag_7_price`: Modal price from 7 days prior.
  - `rolling_7_mean`: 7-day rolling moving average of modal prices.
  - `arrival_tonnes`: Daily arrival volume at APMC market yard.
  - `day_of_week`: Day of the week index (0=Monday, 6=Sunday).
  - `month`: Calendar month index.

### 3.2 Evaluation Results (Holdout Test: April 2024)

| Candidate Model | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) | Mean Absolute Percentage Error (MAPE) |
| :--- | :--- | :--- | :--- |
| **Ridge Regression Baseline** | ₹370.80 /Qtl | ₹584.49 /Qtl | 6.22% |
| **Random Forest Regressor** (Best) | **₹365.43 /Qtl** | **₹583.30 /Qtl** | **6.05%** |

---

## 4. Precision Fertilizer Recommendation Engine

The fertilizer recommendation system integrates a **Random Forest ML formulation classifier** with **ANGRAU stoichiometric nutrient balancing calculations**:

### 4.1 ML Formulation Classifier
- **Model Architecture**: Scikit-Learn `RandomForestClassifier` Pipeline with `ColumnTransformer` (OneHotEncoder for `crop` and `soil_type`, StandardScaler for continuous parameters).
- **Features**: `crop`, `soil_type`, `nitrogen_kg_ha`, `phosphorus_kg_ha`, `potassium_kg_ha`, `soil_ph`, `organic_carbon_pct`, `moisture_pct`.
- **Target Classes**:
  1. `Urea + DAP + MOP` (Standard balanced N-P-K regime)
  2. `DAP + MOP (Legume Base)` (Low starter N, high P-K for Groundnut, Bengal Gram)
  3. `Urea + DAP + MOP + Zinc Sulphate` (Deficient Zn & high vegetative crops like Paddy, Maize, Sugarcane)
  4. `Urea + SSP + MOP` (Sulfur enriched formulation for red/laterite soils)
  5. `NPK Complex 20-20-0-13 + MOP` (Sulfur and balanced macronutrients for Cotton and Chillies)
  6. `Agricultural Lime + DAP + MOP` (Acidic soil remediation, $\text{pH} < 6.0$)
  7. `Agricultural Gypsum + Urea + DAP + MOP` (Alkaline soil remediation, $\text{pH} > 8.2$)
- **Model Performance**:
  - **Test Accuracy**: **98.00%**
  - **Macro F1-Score**: **0.96**
  - **Weighted F1-Score**: **0.98**
  - Top Feature Importances: Soil pH ($32.4\%$), Available Nitrogen ($19.8\%$), Target Crop ($18.5\%$), Phosphorus ($14.2\%$).

### 4.2 Stoichiometric Product Calculations
1. **DAP (18% N, 46% P2O5)**:
   $$\text{DAP Required (kg/ha)} = \frac{\text{Adjusted } P_2O_5}{0.46}$$
2. **Urea (46% N)**:
   $$\text{N from DAP} = \text{DAP (kg/ha)} \times 0.18$$
   $$\text{Urea Required (kg/ha)} = \frac{\max(0, \text{Adjusted N} - \text{N from DAP})}{0.46}$$
3. **MOP (60% K2O)**:
   $$\text{MOP Required (kg/ha)} = \frac{\text{Adjusted } K_2O}{0.60}$$
4. **Farm Acreage Scaling**:
   $$\text{Total Product (kg)} = \text{Product (kg/ha)} \times (\text{Acres} \times 0.404686)$$
   $$\text{Total 50kg Bags} = \frac{\text{Total Product (kg)}}{50}$$

### 4.3 Split Scheduling & Soil Amendments
- **Basal Dose**: 100% DAP, 50% MOP, 25% Urea applied at sowing/transplanting.
- **Top Dressing 1 (25–30 Days)**: 50% Urea applied at active vegetative tillering.
- **Top Dressing 2 (55–60 Days)**: 25% Urea and 50% MOP applied at panicle initiation/flowering.
- **Soil Amendments**:
  - $\text{pH} < 6.0$: Recommends agricultural lime ($\text{CaCO}_3$) at $500 \text{ kg/ha}$.
  - $\text{pH} > 8.2$: Recommends agricultural gypsum ($\text{CaSO}_4$) at $1000 \text{ kg/ha}$.
  - $\text{Organic Carbon} < 0.5\%$: Recommends 5 to 10 tonnes of FYM (Farm Yard Manure) per hectare.
