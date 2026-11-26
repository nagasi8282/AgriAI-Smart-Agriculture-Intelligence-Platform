# AgriAI – Streamlit Community Cloud Deployment Guide

**Target Budget**: Strictly ₹0.00 / $0.00  
**Hosting Provider**: Streamlit Community Cloud ([share.streamlit.io](https://share.streamlit.io))  
**Repository**: [https://github.com/nagasi8282/AgriAI-Smart-Agriculture-Intelligence-Platform](https://github.com/nagasi8282/AgriAI-Smart-Agriculture-Intelligence-Platform)  

---

## 1. Prerequisites

1. A free GitHub account with administrative access to the `AgriAI-Smart-Agriculture-Intelligence-Platform` repository.
2. All code committed and pushed to the `main` branch.
3. No credit card or billing details required.

---

## 2. Step-by-Step Deployment Instructions

### Step 1: Sign in to Streamlit Community Cloud
1. Navigate to **[https://share.streamlit.io](https://share.streamlit.io)** in your web browser.
2. Click **Continue with GitHub**.
3. Authorize Streamlit to access your public GitHub repositories.

---

### Step 2: Create a New Application
1. In the top-right corner of the Streamlit Workspace dashboard, click the blue **New app** button.
2. Select **I already have an app**.

---

### Step 3: Configure Repository Settings
Fill in the deployment form with the exact project parameters:

| Field | Configuration Value | Notes |
| :--- | :--- | :--- |
| **Repository** | `nagasi8282/AgriAI-Smart-Agriculture-Intelligence-Platform` | Select from dropdown or paste URL |
| **Branch** | `main` | Production deployment branch |
| **Main file path** | `app/Home.py` | **CRITICAL**: The entry point is `app/Home.py` (not `Home.py`) |
| **App URL (optional)** | `agriai-platform` (or your custom slug) | Generates `https://agriai-platform.streamlit.app` |

---

### Step 4: Advanced Settings & Secrets (Optional)
1. Click **Advanced settings** at the bottom of the form.
2. **Python version**: Select **3.12** or **3.11**.
3. **Secrets**: Leave blank or paste the contents of `.streamlit/secrets.toml.example`.  
   *(All features operate 100% offline out-of-the-box with built-in zero-cost fallbacks; no API keys are required.)*
4. Click **Save**.

---

### Step 5: Deploy
1. Click **Deploy!**.
2. Streamlit Cloud will spin up a secure Debian container:
   - It reads `packages.txt` to install native C++ graphics dependencies (`libgl1`, `libgomp1`).
   - It reads `requirements.txt` to install all Python dependencies.
   - It launches `streamlit run app/Home.py`.
3. In ~60 to 90 seconds, your public application will be live!

---

## 3. Post-Deployment Verification Checklist

Once the app is running at `https://<your-app-slug>.streamlit.app`, test each capability:

- [ ] **Home Overview**: KPI cards, brand sidebar, and working search bar render properly.
- [ ] **Live Weather Widget**: Displays real-time temperature, condition emoji, and 5-day numerical forecast for Guntur and AP districts.
- [ ] **Crop Intelligence**: Production history charts and filters load.
- [ ] **Mandi Price Analytics**: APMC commodity price trends render.
- [ ] **Soil & Fertilizer Intelligence**: Nutrient balancing engine computes commercial fertilizer bags (Urea, DAP, MOP).
- [ ] **Crop Yield Prediction**: Random Forest ML model predicts harvest yield in quintals/ha.
- [ ] **Mandi Price Prediction**: Price regression ML model generates 14-day forecasts.
- [ ] **Plant Disease Detection**: Image upload renders foliar diagnosis and Grad-CAM saliency heatmap.
- [ ] **AgriAI Assistant**: Interactive chat answers agricultural queries with grounded knowledge.
- [ ] **AgriDoc AI (PDF RAG)**: Answers questions citing page numbers from reference research papers.
- [ ] **Reports & Downloads**: CSV export downloads correctly.

---

## 4. Continuous Integration & Auto-Updates

Streamlit Community Cloud is integrated with GitHub webhooks:
- Every `git push origin main` triggers an automatic background rebuild and rolling deployment without downtime.
- Logs and container metrics can be monitored via the bottom-right **Manage app** drawer.
