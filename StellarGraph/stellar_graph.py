import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import streamlit as st
from matplotlib.ticker import FormatStrFormatter

# --- STREAMLIT APP SETUP ---
# 1. This MUST be the first Streamlit command executed.
st.set_page_config(layout="wide")

st.title("Stellar Luminosity vs. Temperature")

# --- INITIALIZATION & CONSTANTS ---
T_min = 3000
T_max = 12000
T_init = 5778

# Initialize the temperature in session state if it doesn't exist
# This is the single source of truth for the initial value.
if 'T_current' not in st.session_state:
    st.session_state.T_current = T_init

sigma = 5.67e-8  # Stefan–Boltzmann constant (W/m²·K⁴)
R = 6.96e8       # Approximate solar radius (m)

# --- Stefan–Boltzmann Luminosity Function ---
def luminosity(T):
    return 4 * np.pi * R**2 * sigma * T**4

# --- CALCULATIONS (Uses the T value from the current session state) ---
# T is read directly from the session state
T = st.session_state.T_current
L_current = luminosity(T)

# --- COLOR CHANGE: Using RdYlBu map for Red (Cool) to Blue (Hot) ---
color_current = cm.RdYlBu((T - T_min) / (T_max - T_min))


# 1. Create and Display the Matplotlib Figure (GRAPH)
fig, ax = plt.subplots(figsize=(10, 6))

# --- Plot Styling (Preserved) ---
dark_bg_color = '#0a0a0a' 
ax.set_facecolor(dark_bg_color)
fig.patch.set_facecolor(dark_bg_color) 
ax.set_xlim(T_min, T_max)
ax.set_ylim(0, luminosity(T_max) * 1.1)
ax.tick_params(colors='white', labelsize=10)

for spine in ax.spines.values():
    spine.set_color('gray')
# Apply the fix for the y-axis label
ax.yaxis.set_major_formatter(FormatStrFormatter('%1.1e')) 

# --- Plot Data and Annotations ---
T_vals = np.linspace(T_min, T_max, 400)
L_vals = luminosity(T_vals)

# --- COLOR CHANGE: Apply RdYlBu map to the scatter plot ---
colors = cm.RdYlBu((T_vals - T_min) / (T_max - T_min))
ax.scatter(T_vals, L_vals, c=colors, s=15, edgecolor='none', alpha=0.5)

# Highlight the selected star
ax.plot(T, L_current, 'o', markersize=16, markeredgecolor='white', color=color_current)

ax.set_title("Stellar Luminosity vs. Temperature", color='white', fontsize=16, pad=15)
ax.set_xlabel("Temperature (K)", color='white', fontsize=12)
ax.set_ylabel("Luminosity (Watts)", color='white', fontsize=12)

# Stefan–Boltzmann Law Annotation (Top Right Corner)
law_text = (
    r"$L = 4\pi R^2 \sigma T^4$" "\n"
    r"$\sigma = 5.67\times10^{-8}\ \mathrm{W\,m^{-2}\,K^{-4}}$"
)
ax.text(0.98, 0.95, law_text, color='white', fontsize=11, ha='right', va='top', transform=ax.transAxes, bbox=dict(facecolor='black', edgecolor='gray', alpha=0.5, boxstyle='round,pad=0.5'))
ax.text(0.5, 0.5, "Luminosity $\\propto T^4$", color='orange', fontsize=13, ha='center', transform=ax.transAxes)

# Display the Matplotlib figure in Streamlit
st.pyplot(fig)


# 2. Render the SLIDER (Visually Under the Graph)
# The 'value' parameter is removed. The widget now reads its initial state and updates 
# its value via the 'key'='T_current' linkage.
st.slider(
    "Select Star Temperature (K)",
    min_value=T_min,
    max_value=T_max,
    key='T_current', # This key ensures the value updates the state variable
    step=10,
    format='%0.0f K'
)


# 3. Render the TEXT DETAILS (Visually Under the Slider)
st.markdown("---") 

# --- UPDATED LUMINOSITY DISPLAY ---
# Format L_current as scientific notation (e.g., '1.23e+27' or '1.23e-08')
formatted_L = "{:.2e}".format(L_current)

# Logic to split the string and handle both positive and negative exponents
if 'e+' in formatted_L:
    base, exponent = formatted_L.split('e+')
elif 'e-' in formatted_L:
    base, exponent = formatted_L.split('e-')
    exponent = '-' + exponent # Prefix with negative sign
else:
    # Handles non-scientific notation case (unlikely here)
    base = formatted_L
    exponent = '0'

# Use LaTeX syntax ($...$) to display the scientific notation cleanly as X.XX times 10 to the YY
st.markdown(
    f"**Calculated Luminosity ($L$):** <span style='color:orange; font-size:1.3em;'>${base} \\times 10^{{{exponent}}}$ Watts</span>",
    unsafe_allow_html=True
)
# --- END OF UPDATED LUMINOSITY DISPLAY ---

st.markdown(
    f"Relative to the Sun ($3.83 \\times 10^{{26}}$ W), this star is **{L_current/3.83e26:1.1f} times** brighter.",
    unsafe_allow_html=True
)
