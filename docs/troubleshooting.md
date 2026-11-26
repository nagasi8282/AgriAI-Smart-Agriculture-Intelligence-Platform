# AgriAI – Deployment Troubleshooting & Diagnostics

**Scope**: Streamlit Community Cloud, Local Development, and Zero-Cost Standalone Mode  

---

## 1. Common Deployment Issues on Streamlit Community Cloud

### Issue 1: App Fails to Start with `FileNotFoundError: [Errno 2] No such file or directory: 'Home.py'`
- **Cause**: Streamlit Cloud was configured with `Home.py` instead of the actual file location `app/Home.py`.
- **Solution**:
  1. Open your Streamlit Cloud Workspace.
  2. Click **Manage app** (bottom-right) ➔ **Settings** ➔ **General**.
  3. Ensure **Main file path** is set strictly to `app/Home.py`.
  4. Click **Save** and trigger a reboot.

---

### Issue 2: `ModuleNotFoundError: No module named 'backend'` or `'app'`
- **Cause**: Python import path does not include the project root when executing sub-modules directly.
- **Solution**:
  - `app/Home.py` and `app/utils/api_client.py` automatically add the project root to `sys.path`.
  - Ensure your repository structure keeps `app/`, `backend/`, and `ml/` at the repository root.

---

### Issue 3: Container Memory Limit Exceeded (OOM / App Crashing on Free Tier)
- **Cause**: Streamlit Community Cloud provides 1 GB RAM. Loading full PyTorch with CUDA or multi-gigabyte models into memory simultaneously triggers an immediate kernel kill.
- **Solution**:
  - AgriAI is optimized for low memory footprints:
    - Disease detection uses lightweight PIL/NumPy synthetic Grad-CAM overlays (~15 MB RAM).
    - Scikit-Learn models are loaded lazily and cached via `@st.cache_resource`.
    - Live weather data is cached via `@st.cache_data(ttl=600)` to avoid redundant API polling.

---

### Issue 4: `libGL.so.1: cannot open shared object file` (OpenCV / Graphics Error)
- **Cause**: Linux cloud containers lack native X11 / OpenGL shared libraries.
- **Solution**:
  - AgriAI includes `packages.txt` in the repository root containing:
    ```
    libgl1
    libglib2.0-0
    libgomp1
    ```
  - Streamlit Community Cloud detects this file automatically during container provisioning and installs the required packages via `apt-get`.

---

### Issue 5: Live Weather Widget Timeout / Offline Fallback
- **Cause**: Transient network hiccups reaching `api.open-meteo.com`.
- **Solution**:
  - Both `backend/services/weather_live_service.py` and `app/utils/live_weather.py` feature resilient fallbacks with realistic seasonal meteorological baselines. If the external network times out after 4 seconds, the app gracefully switches to the baseline without raising an unhandled exception or breaking the UI.

---

## 2. Local Development Troubleshooting

### Issue 1: `WinError 10013: An attempt was made to access a socket in a way forbidden by its access permissions`
- **Cause**: Port 8000 or 8501 is already occupied by a background process, or Windows sandbox security blocked the port.
- **Solution**:
  ```powershell
  # Find and terminate existing Python processes
  Get-Process -Name python, uvicorn, streamlit -ErrorAction SilentlyContinue | Stop-Process -Force

  # Restart FastAPI and Streamlit
  uvicorn backend.main:app --host 127.0.0.1 --port 8000
  streamlit run app/Home.py --server.port 8501
  ```

---

### Issue 2: Streamlit Shows "Loading crop production trends..." Indefinitely
- **Cause**: The API client cannot reach `http://localhost:8000` and in-process fallback was not triggered.
- **Solution**:
  - Check `app/utils/api_client.py`: Ensure `BACKEND_URL` is set to `http://localhost:8000` (or leave blank for standalone in-process mode).
  - Verify FastAPI is running: visit `http://127.0.0.1:8000/api/v1/health` in your browser.
