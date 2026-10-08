import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de la página web
st.set_page_config(page_title="Termodinámica de la Hidrólisis del ATP", layout="wide")

st.title("🔋 Termodinámica de la Hidrólisis del ATP (Cambios Agudos)")
st.write("Explora cómo un cambio agudo en el ATP altera automáticamente el ADP y el Pi por conservación de masa, y cómo esto afecta al cambio de energía libre.")

st.markdown("---")

# --- CONSTANTES FIJAS Y TABULADAS ---
R = 0.008315  # KJ/(mol*K)
DG0_ATP = -30.5  # Valor tabulado estándar fijo en KJ/mol

# --- CONFIGURACIÓN DEL SISTEMA EN LA BARRA LATERAL ---
st.sidebar.header("⚙️ 1. Parámetros del Pool Agudo")
st.sidebar.write("*(Sin síntesis de novo: la masa total permanece constante)*")

# Permitir configurar pools totales más pequeños para forzar termodinámicamente el ΔG positivo
total_adenilatos = st.sidebar.slider(
    "Pool Total de Adenilatos (ATP + ADP) en mM:", 
    min_value=0.1, max_value=20.0, value=2.0, step=0.1
)

pi_basal = st.sidebar.slider(
    "Fosfato Inorgánico (Pi) basal en mM (cuando ADP = 0):", 
    min_value=1.0, max_value=150.0, value=50.0, step=1.0
)

st.sidebar.markdown("---")
st.sidebar.header("🌡️ 2. Control Ambiental")
temp_celsius = st.sidebar.slider(
    "Temperatura Ambiental (°C):",
    min_value=0.0, max_value=50.0, value=37.0, step=1.0
)
temp_kelvin = temp_celsius + 273.15
RT = R * temp_kelvin

st.sidebar.markdown("---")
st.sidebar.header("🕹️ 3. Variable Independiente")

# Control dinámico del ATP limitado por el Pool Total seleccionado
atp_mm = st.sidebar.slider(
    "Concentración de ATP [Sustrato] (mM):", 
    min_value=0.001, 
    max_value=float(total_adenilatos - 0.001), 
    value=float(total_adenilatos * 0.8), 
    step=0.001,
    format="%.3f"
)

# --- CÁLCULOS INTERDEPENDIENTES POR CONSERVACIÓN DE MASA ---
adp_mm = total_adenilatos - atp_mm
pi_mm = pi_basal + adp_mm

# Conversión interna a Molar (M) para la ecuación termodinámica
atp_m = atp_mm / 1000.0
adp_m = adp_mm / 1000.0
pi_m = pi_mm / 1000.0

# Cálculo del Cociente de Reacción (Q) y ΔG Real
Q = (adp_m * pi_m) / atp_m
ln_Q = np.log(Q)
termino_entropico = RT * ln_Q
dg_real = DG0_ATP + termino_entropico

# --- DESPLIEGUE DE RESULTADOS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚡ Estado Energético del ATP")
    
    # Mostrar el valor del ΔG de forma clara e interactiva sin desgloses
    st.metric(
        label="Variación de Energía Libre Real (ΔG Real)", 
        value=f"{dg_real:.2f} KJ/mol",
        delta=f"ΔG°' Estándar Fijo: {DG0_ATP} KJ/mol",
        delta_color="off"
    )
    
    st.markdown("---")
    
    # Alerta visual dinámica según el valor del ΔG calculado
    if dg_real < -45:
        st.success(f"### ΔG = {dg_real:.2f} KJ/mol\n\n**Altamente Exergónica:** Máxima energía disponible. Proporciones fisiológicas normales en una célula sana.")
    elif dg_real < 0:
        st.warning(f"### ΔG = {dg_real:.2f} KJ/mol\n\n**Exergónica Débil:** Fuerza impulsora baja. La célula experimenta un estrés energético agudo, pero la reacción sigue siendo espontánea.")
    else:
        st.error(f"### ΔG = {dg_real:.2f} KJ/mol\n\n**🛑 REACCIÓN INVERTIDA (Endergónica):** ¡Lograste alcanzar el umbral positivo en un cambio agudo! En estas condiciones, el ATP ha perdido toda su capacidad de realizar trabajo espontáneo.")

with col2:
    st.subheader("📊 Distribución de la Masa Celular")

    # Gráfico de barras interactivo de las concentraciones manipuladas
    componentes = ['ATP (Sustrato)', 'ADP (Producto)', 'Fosfato Inorgánico (Pi)']
    valores = [atp_mm, adp_mm, pi_mm]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=componentes, y=valores,
        marker_color=['#2ECC71', '#E67E22', '#3498DB'],
        text=[f"{v:.3f} mM" for v in valores], textposition='auto'
    ))
    fig.update_layout(
        yaxis_title='Concentración en la App (mM)',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300,
        margin=dict(t=10, b=10, l=10, r=10)
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("**Nota Pedagógica de Masa Constante:** Al tratarse de un cambio agudo, observa cómo al reducir el ATP, el ADP y el Pi aumentan de forma inmediata en estricta relación estequiométrica, reflejando fielmente la química celular real.")
