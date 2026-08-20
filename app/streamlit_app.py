import os
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="CropAI — Smart Agriculture Decision-Support Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-title {
        background: linear-gradient(135deg, #2E7D32, #4CAF50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #555555;
        font-size: 1.25rem;
        margin-bottom: 2rem;
    }
    
    .card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e8f5e9;
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    .card-title {
        color: #2E7D32;
        font-weight: 600;
        font-size: 1.4rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/sprout.png", width=60)
st.sidebar.title("CropAI Navigation")
st.sidebar.info("Select a workflow from the sidebar or from the landing cards to start diagnosis, crop recommendation, or yield estimation.")

# Main layout
st.markdown("<h1 class='main-title'>🌱 CropAI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Explainable, Uncertainty-Aware Agricultural Decision Support System</p>", unsafe_allow_html=True)

st.write("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">🔍 Disease Diagnosis</div>
        <p>Upload crop leaf images to instantly identify plant pathogens. The system provides prediction confidence, MC Dropout uncertainty, and Grad-CAM visual heatmaps showing the affected leaf lesions.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Disease Diagnosis", key="btn_disease", type="primary"):
        st.switch_page("pages/disease.py")

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">🚜 Crop Recommendation</div>
        <p>Enter soil parameters (N, P, K, pH) and environmental inputs (rainfall, temp, humidity) to receive calibrated crop recommendations. Visualizes feature importance using local SHAP contribution charts.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Crop Recommendation", key="btn_crop", type="primary"):
        st.switch_page("pages/crop.py")

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">📈 Yield Prediction</div>
        <p>Predict expected crop yields using agricultural inputs (crop, season, rainfall, temperature, area). Features conformal prediction intervals for statistical reliability bounds and SHAP explanations.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Yield Prediction", key="btn_yield", type="primary"):
        st.switch_page("pages/yield.py")

st.write("---")

# Platform info
st.markdown("### Engineering & Calibration Quality Standards")
st.markdown("""
- **Decoupled API-First Architecture:** The Streamlit client interacts strictly with the modular FastAPI backend using standardized REST payloads.
- **Explainability (SHAP & Grad-CAM):** Transcends standard black-box models by plotting feature contributions and activation maps.
- **Uncertainty Quantification:** Outlines statistical prediction intervals (Conformal Prediction) and entropy measurements rather than raw confidence.
""")
