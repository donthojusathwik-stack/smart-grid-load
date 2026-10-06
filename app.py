import streamlit as st
import numpy as np
import joblib
from auth import update_prediction_count, get_user_info
from login import show_login
from register import show_register

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user' not in st.session_state:
    st.session_state.user = None

# Page routing
if not st.session_state.logged_in:
    if st.session_state.page == 'register':
        show_register()
    else:
        show_login()
    st.stop()

# Load trained model
try:
    model = joblib.load(r"C:\Users\SATHWIK\OneDrive\Desktop\smart grid load\smart grid load\smart grid load\energy_model.pkl")
except:
    st.error("⚠️ Error loading model. Please ensure 'energy_model.pkl' exists.")
    st.stop()

# Page config
st.set_page_config(
    page_title="smart grid systems",
    page_icon="⚡",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    :root{
        --bg1: #667eea;
        --bg2: #764ba2;
    }
    .main {
        background: linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 100%);
    }
    /* Adaptive text colors */
    .light-text { color: #111 !important; }
    .dark-text { color: #fff !important; text-shadow: 0 1px 2px rgba(0,0,0,0.6); }

    .stButton>button {
        background: linear-gradient(135deg, var(--bg1), var(--bg2));
        color: inherit;
        border: none;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 8px;
        cursor: pointer;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, var(--bg2), var(--bg1));
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .prediction-box {
        background: linear-gradient(135deg, rgba(0,0,0,0.25), rgba(0,0,0,0.15));
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: inherit;
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        backdrop-filter: blur(6px);
    }
    .contrast-box {
        display:inline-block;
        padding:6px 12px;
        border-radius:8px;
        background: rgba(0,0,0,0.25);
        color: inherit;
    }
    </style>
    <script>
    (function(){
      function hexToLuminance(hex){
        hex = hex.replace('#','');
        var r = parseInt(hex.substring(0,2),16)/255;
        var g = parseInt(hex.substring(2,4),16)/255;
        var b = parseInt(hex.substring(4,6),16)/255;
        var srgb = [r,g,b].map(function(c){ return c<=0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055,2.4); });
        var lum = 0.2126*srgb[0] + 0.7152*srgb[1] + 0.0722*srgb[2];
        return lum;
      }
      var root = getComputedStyle(document.documentElement);
      var bg1 = (root.getPropertyValue('--bg1') || '#667eea').trim();
      var bg2 = (root.getPropertyValue('--bg2') || '#764ba2').trim();
      var lum = (hexToLuminance(bg1) + hexToLuminance(bg2))/2;
      var textClass = lum > 0.5 ? 'light-text' : 'dark-text';
      document.documentElement.classList.add(textClass);
    })();
    </script>
""", unsafe_allow_html=True)

# Navbar with user info and logout
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"### 👤 Welcome, **{st.session_state.user['username']}**!")
with col2:
    if st.button("🚪 Logout", key="logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = 'login'
        st.rerun()

# Get updated user info
user_info = get_user_info(st.session_state.user['username'])
if user_info:
    st.session_state.user['predictions_count'] = user_info['predictions_count']

# Display prediction count
st.info(f"📊 Total Predictions Made: **{st.session_state.user['predictions_count']}**")

st.divider()

# Title
st.markdown("<h1 class='contrast-box' style='text-align: center;'>⚡ Energy Consumption Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='contrast-box' style='text-align: center;'>Predict household energy usage using ML</p>", unsafe_allow_html=True)
st.divider()

# Create a container for inputs
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        reactive = st.number_input("⚡ Reactive Power (kVAR)", min_value=0.0, step=0.01, format="%.2f")
        voltage = st.number_input("🔌 Voltage (V)", min_value=0.0, step=0.1, format="%.1f")
        intensity = st.number_input("📊 Global Intensity (A)", min_value=0.0, step=0.1, format="%.1f")
    
    with col2:
        sub1 = st.number_input("📈 Sub Metering 1 (Wh)", min_value=0.0, step=1.0, format="%.0f")
        sub2 = st.number_input("📉 Sub Metering 2 (Wh)", min_value=0.0, step=1.0, format="%.0f")
        sub3 = st.number_input("📊 Sub Metering 3 (Wh)", min_value=0.0, step=1.0, format="%.0f")

st.divider()

# Prediction button
if st.button("🔮 Predict Energy Consumption", type="primary"):
    if all(v >= 0 for v in [reactive, voltage, intensity, sub1, sub2, sub3]):
        with st.spinner("Analyzing energy parameters..."):
            features = np.array([[reactive, voltage, intensity, sub1, sub2, sub3]])
            prediction = model.predict(features)[0]
            
            # Update prediction count
            new_count = update_prediction_count(st.session_state.user['username'])
            if new_count:
                st.session_state.user['predictions_count'] = new_count
            
            # Display result
            st.markdown(f"""
                <div class='prediction-box'>
                    ⚡ Predicted Energy Consumption<br>
                    <span style='font-size: 48px;'>{prediction:.3f} kW</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.success("✓ Prediction completed successfully!")
            st.balloons()
    else:
        st.error("⚠️ Please ensure all values are non-negative!")

# Info section
st.divider()
with st.expander("ℹ️ About This Predictor"):
    st.write("""
    This ML-based energy consumption predictor uses advanced machine learning algorithms 
    to forecast household energy usage based on multiple parameters:
    
    - **Reactive Power**: Energy consumed by inductive loads
    - **Voltage**: Electrical potential difference
    - **Global Intensity**: Total current flow
    - **Sub Metering 1, 2, 3**: Energy consumption from different circuits
    
    The model has been trained on real household energy data to provide accurate predictions.
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div class='contrast-box' style='text-align:center; font-size:12px;'>"
    "🔋 ML-Based smart grid systems| © 2025 Energy Predictor"
    "</div>",
    unsafe_allow_html=True
)