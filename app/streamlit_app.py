import os
import sys
from pathlib import Path
import streamlit as st

# Add repository root to sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Set page configuration
st.set_page_config(
    page_title="CropAI — Smart Agriculture Decision-Support Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom ultra-minimalist CSS (Light & Dark mode compatible)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        font-size: 2.25rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 0.25rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    
    .sub-header {
        font-size: 1.05rem;
        font-weight: 400;
        opacity: 0.7;
        margin-bottom: 1.75rem;
    }
    
    .minimal-card {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.18);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        min-height: 180px;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    
    .minimal-card:hover {
        border-color: rgba(16, 185, 129, 0.5);
        transform: translateY(-2px);
    }
    
    .card-title-text {
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-desc {
        font-size: 0.88rem;
        line-height: 1.5;
        opacity: 0.75;
    }
    
    .section-box {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("CropAI System")
st.sidebar.caption("v2.0 • Decision-Support Engine")
st.sidebar.write("---")
st.sidebar.markdown("""
**Navigation Tip:**
Select a module below or from the dashboard cards to begin diagnosis, recommendation, or yield prediction.
""")

# Main Header
st.markdown("<div class='main-header'>🌱 CropAI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Explainable, Uncertainty-Aware Agricultural Decision Support System</div>", unsafe_allow_html=True)

st.write("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="minimal-card">
        <div class="card-title-text">🔍 Disease Diagnosis</div>
        <div class="card-desc">Identify plant pathogens from leaf photos. Returns prediction confidence, MC Dropout uncertainty, and Grad-CAM lesion heatmaps.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Diagnosis", key="btn_disease", use_container_width=True):
        st.switch_page("pages/disease.py")

with col2:
    st.markdown("""
    <div class="minimal-card">
        <div class="card-title-text">🚜 Crop Recommendation</div>
        <div class="card-desc">Analyze soil chemistry (N, P, K, pH) and weather parameters to recommend optimal crops with local SHAP feature explanations.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Recommendation", key="btn_crop", use_container_width=True):
        st.switch_page("pages/crop.py")

with col3:
    st.markdown("""
    <div class="minimal-card">
        <div class="card-title-text">📈 Yield Prediction</div>
        <div class="card-desc">Forecast agricultural yield per hectare. Calculates 90% Conformal Prediction bounds and SHAP feature influence breakdowns.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Yield Prediction", key="btn_yield", use_container_width=True):
        st.switch_page("pages/yield.py")

st.markdown("""
<div class="section-box">
    <h4 style="margin-top:0; font-weight:600; font-size:1.05rem;">Core Architecture & Reliability</h4>
    <ul style="margin-bottom:0; font-size:0.88rem; opacity:0.85; padding-left:1.2rem;">
        <li><b>API-First Serving:</b> Decoupled FastAPI engine serving calibrated models.</li>
        <li><b>Explainability (XAI):</b> SHAP feature attribution & Grad-CAM neural spatial activation maps.</li>
        <li><b>Uncertainty Bounds:</b> Conformal Prediction distribution intervals & MC Dropout entropy scoring.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
