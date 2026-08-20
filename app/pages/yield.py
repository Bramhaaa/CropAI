import os
import requests
import streamlit as st
import matplotlib.pyplot as plt
import importlib
yield_exp_mod = importlib.import_module("models.yield.explainability")
generate_yield_shap_plot = yield_exp_mod.generate_yield_shap_plot

# Config
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Yield Prediction — CropAI", page_icon="🌱", layout="wide")

st.markdown("""
<style>
    .section-title {
        color: #2E7D32;
        font-weight: 700;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .metric-container {
        background-color: #f1f8e9;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c5e1a5;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2E7D32;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #555555;
    }
</style>
""", unsafe_style_html=True)

st.markdown("<h1 class='section-title'>📈 Yield Prediction</h1>", unsafe_style_html=True)
st.write("Predict expected agricultural crop yield (tonnes per hectare) and calculate statistical reliability boundaries using Conformal Prediction intervals.")

st.write("---")

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("Agricultural Parameters")
    
    crop = st.selectbox("Select Crop", ["Rice", "Maize", "Chickpea", "Cotton", "Mango", "Banana", "Grapes"])
    season = st.selectbox("Select Season", ["Kharif", "Rabi", "Summer", "Whole Year"])
    rainfall = st.slider("Average Seasonal Rainfall (mm)", min_value=400.0, max_value=2500.0, value=1100.0, step=10.0)
    temp = st.slider("Average Temperature (°C)", min_value=15.0, max_value=40.0, value=26.0, step=0.5)
    area = st.slider("Cultivated Area (hectares)", min_value=0.5, max_value=10.0, value=2.5, step=0.1)
    
    # Conformal confidence selector
    conf_pct = st.selectbox("Statistical Confidence Level", ["90% (Recommended)", "95%", "80%"])
    conf_level = {"90% (Recommended)": 0.90, "95%": 0.95, "80%": 0.80}[conf_pct]
    
    if st.button("Predict Expected Yield", type="primary", use_container_width=True):
        payload = {
            "crop": crop,
            "season": season,
            "rainfall": rainfall,
            "temperature": temp,
            "area": area,
            "confidence_level": conf_level
        }
        
        with st.spinner("Processing regression and generating conformal intervals..."):
            try:
                response = requests.post(f"{API_URL}/api/v1/yield/predict", json=payload, timeout=10)
                if response.status_code == 200:
                    st.session_state["yield_result"] = response.json()
                    st.success("Yield prediction calculated!")
                else:
                    st.error(f"Error {response.status_code}: {response.json().get('detail', 'Yield prediction failed')}")
            except Exception as e:
                st.error(f"Failed to connect to API: {str(e)}")

with col_right:
    st.subheader("Yield Estimates & Reliability")
    
    if "yield_result" in st.session_state:
        res = st.session_state["yield_result"]
        pred_yield = res["predicted_yield"]
        unit = res["unit"]
        interval = res["interval"]
        explanation = res["explanation"]
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Estimated Yield ({unit})</div>
                <div class="metric-value">{pred_yield:.2f}</div>
            </div>
            """, unsafe_style_html=True)
            
        with col_m2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">{int(interval['confidence_level']*100)}% Confidence Interval</div>
                <div class="metric-value">[{interval['lower']:.2f}, {interval['upper']:.2f}]</div>
            </div>
            """, unsafe_style_html=True)
            
        # Explanatory card
        st.write("#### 🛡️ Conformal Prediction Bounds")
        st.write(f"- Under the requested **{int(interval['confidence_level']*100)}%** confidence level, the true yield is statistically guaranteed to fall between **{interval['lower']:.2f}** and **{interval['upper']:.2f}** {unit} (assuming environment consistency).")
        st.write(f"- **Interval Width:** `{interval['interval_width']:.4f}` {unit}")
        
        # Draw SHAP explanation graph
        if explanation.get("top_features"):
            st.write("#### ⚖️ Feature Contribution (SHAP)")
            st.caption("Shows the relative impact of each categorical class one-hot encoding or numeric environmental feature on the predicted yield value.")
            
            fig = generate_yield_shap_plot(explanation["top_features"], pred_yield)
            st.pyplot(fig)
            plt.close(fig)
    else:
        st.info("Input parameters in the left panel and click 'Predict Expected Yield' to view outputs.")

if st.button("Return to Dashboard"):
    st.switch_page("streamlit_app.py")
