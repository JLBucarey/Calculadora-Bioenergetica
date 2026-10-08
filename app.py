import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de la página web
st.set_page_config(page_title="Termodinámica de la Hidrólisis del ATP", layout="wide")

st.title("🔋 Termodinámica de la Hidrólisis del ATP en la Célula")
st.write("Modifica las variables ambientales y celulares para descubrir los principios de la bioenergética celular bajo un sistema de masa constante.")

st.markdown("---")

# --- CONSTANTES FIJAS Y TABULADAS ---
R = 0.008315  # KJ/(mol*K)
DG0_ATP = -30.5  # Valor tabulado estándar fijo en KJ/mol

# --- CONFIGURACIÓN DEL SISTEMA CERRADO (MASA CONSTANTE) ---
st.sidebar.header("⚙️ Configuración del Sistema")

# Definimos el pozo total de adenilatos (ATP + ADP) en mM
total_adenilatos = st.sidebar.number_input(
    "Pool Total de Adenilatos (ATP + ADP) en mM:", 
    value=10.0, 
    min_value=2.0, 
    max_value=50.0, 
    step=1.0
)

# Definimos una relación base para el Fosfato inorgánico ligado a la hidrólisis
pi_basal = st.sidebar.number_input(
    "Fosfato Inorgánico (Pi) basal en mM (cuando ADP = 0):", 
    value=1.0, 
    min_value=0.1, 
    step=0.5
)

st.sidebar.markdown("---")
st.sidebar.subheader("🌡️ Control de Temperatura")

# --- LÓGICA DEL BOTÓN DE RESTABLECIMIENTO ---
# Usamos el estado de sesión de Streamlit para poder resetear los valores con un clic
if 'atp_val' not in st.session_state:
    st.session_state.atp_val = float(total_adenilatos * 0.8)
if 'temp_val' not in st.session_state:
    st.session_state.temp_val = 37.0

# Botón para resetear a condiciones del cuerpo humano
if st.sidebar.button("🔄 Restablecer a Condiciones Fisiológicas (37°C / 80% ATP)"):
    st.session_state.atp_val = float(total_adenilatos * 0.8)
    st.session_state.temp_val = 37.0
    st.rerun()

# Deslizador en Celsius en el rango de 0 a 50 °C
temp_celsius = st.sidebar.slider(
    "Temperatura Ambiental (°C):",
    min_value=0.0,
    max_value=50.0,
    key='temp_val',
    step=1.0
)

# Conversión automática a Kelvin
temp_kelvin = temp_celsius + 273.15

st.sidebar.markdown("---")
st.sidebar.subheader("🕹️ Control de Concentraciones")

# El alumno mueve la variable de ATP y la masa se conserva
atp_mm = st.sidebar.slider(
    "Concentración de ATP [Sustrato] (mM):", 
    min_value=0.01, 
    max_value=float(total_adenilatos - 0.01), 
    key='atp_val',
    step=0.1
)

# --- CÁLCULOS AUTOMÁTICOS POR BALANCE DE MASA ---
adp_mm = total_adenilatos - atp_mm
pi_mm = pi_basal + adp_mm

# Conversión a Molar (M) para la ecuación termodinámica interna
atp_m = atp_mm / 1000.0
adp_m = adp_mm / 1000.0
pi_m = pi_mm / 1000.0

# Cálculo del término dinámico RT usando la temperatura en Kelvin calculada
RT = R * temp_kelvin

# Cálculo del Cociente de Reacción (Q) y ΔG Real
Q = (adp_m * pi_m) / atp_m
dg_real = DG0_ATP + (RT * np.log(Q))

# --- DESPLIEGUE DE RESULTADOS INTERACTIVOS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚡ Estado Energético Actual")
    
    # Métricas de variables activas
    st.markdown("#### Variables del Entorno:")
    st.write(f"🌡️ **Temperatura:** `{temp_celsius:.1f} °C` ({temp_kelvin:.2f} K)")
    st.write(f"🧪 **ATP [Sustrato]:** `{atp_mm:.2f} mM` | **ADP [Producto]:** `{adp_mm:.2f} mM` | **Pᵢ [Producto]:** `{pi_mm:.2f} mM`")
    
    st.markdown("---")
    st.markdown("#### Potencial Termodinámico Fijo vs Real:")
    st.metric(label="ΔG°' Estándar Tabulado (Fijo)", value=f"{DG0_ATP} KJ/mol")
    
    # Alerta visual dinámica según el valor del ΔG calculado
    if dg_real < -45:
        st.success(f"### ΔG Real = {dg_real:.2f} KJ/mol\n\n**Altamente Exergónica:** Condiciones ideales para la vida celular. El motor energético tiene máxima fuerza para acoplarse a reacciones endergónicas.")
    elif dg_real < 0:
        st.warning(f"### ΔG Real = {dg_real:.2f} KJ/mol\n\n**Exergónica Débil:** La célula está experimentando estrés energético o fatiga. La reacción sigue siendo espontánea pero libera menos energía.")
    else:
        st.error(f"### ΔG Real = {dg_real:.2f} KJ/mol\n\n**Colapso Energético (Endergónica):** ¡La reacción se ha invertido! En estas condiciones el ATP requeriría energía externa para hidrolizarse. Compatible con la muerte celular.")

with col2:
    st.subheader("📊 Distribución de la Masa Celular")
    
    # Gráfico de barras interactivo
    componentes = ['ATP (Sustrato)', 'ADP (Producto)', 'Fosfato Inorgánico (Pi)']
    valores = [atp_mm, adp_mm, pi_mm]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=componentes,
        y=valores,
        marker_color=['#2ECC71', '#E67E22', '#3498DB'],
        text=[f"{v:.2f} mM" for v in valores],
        textposition='auto'
    ))
    
    fig.update_layout(
        yaxis_title='Concentración (mM)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MÓDULO DE AUTOAPRENDIZAJE GUIADO
# ==========================================
st.markdown("---")
st.subheader("🧠 Desafíos de Descubrimiento (Taller Autoaplicado)")
st.write("Manipula los controles laterales de la aplicación para responder a los siguientes casos de estudio biológicos:")

# Desafío 1
with st.expander("📖 Desafío 1: La paradoja del valor biológico real vs. estándar"):
    st.markdown("""
    **Pregunta:** Coloca la temperatura en **25°C** (298.15 K) y ajusta el deslizador de ATP de tal manera que las concentraciones de ATP, ADP y Pi sean exactamente **1000 mM (1 M)** cada una. ¿Qué valor toma el \(\Delta G\) real? ¿Qué conclusión pedagógica obtienes?
    
    **💡 Ver Verificación Científica:**
    Cuando todas las concentraciones son exactamente 1 M, el cociente de reacción \(Q = 1\), por lo tanto \(\ln(1) = 0\). En ese momento exacto, el \(\Delta G\) real se iguala al \(\Delta G^{\circ'}\) estándar (\(-30.5\) KJ/mol). Esto le demuestra al estudiante que las 'condiciones estándar' de los libros de texto son artificiales, ya que ninguna célula viva tiene concentraciones de solutos tan elevadas como 1 M.
    """)

# Desafío 2
with st.expander("📖 Desafío 2: Fiebre alta o estrés térmico ambiental"):
    st.markdown("""
    **Pregunta:** Deja las concentraciones fijas en un estado de fatiga celular (ejemplo: ATP a **3.0 mM**) y mueve el control de temperatura desde **0°C hasta 50°C**. ¿Hacia dónde se desplaza el \(\Delta G\) real a medida que aumenta la temperatura? ¿El calor ayuda o perjudica la disponibilidad energética de la reacción en este escenario?
    
    **💡 Ver Verificación Científica:**
    Al aumentar la temperatura, notarás que el \(\Delta G\) se vuelve ligeramente **más negativo** (si \(Q < K_{eq}\)). Esto ocurre porque la temperatura actúa como un amplificador del término entrópico en la ecuación (\(RT \ln Q\)). En la física celular real, cambios extremos de temperatura alteran la energía disponible, aunque el peligro biológico previo suele ser la desnaturalización de las enzimas encargadas de catalizar el proceso.
    """)

# Desafío 3
with st.expander("📖 Desafío 3: El umbral del colapso celular de la Isquemia"):
    st.markdown("""
    **Pregunta:** Cuando un tejido se queda sin oxígeno (isquemia), el ATP se desploma drásticamente. Mueve el deslizador para reducir el ATP al mínimo posible (**0.1 mM**). ¿Qué ocurre con el signo del \(\Delta G\) real? ¿Puede la célula sobrevivir realizando trabajo metabólico en ese punto?
    
    **💡 Ver Verificación Científica:**
    Al caer drásticamente el ATP, el ADP y el Pi se acumulan por balance de masa, haciendo que el cociente \(Q\) aumente exponencialmente. Esto empuja el \(\Delta G\) real hacia valores **positivos o cercanos a cero**. Cuando el \(\Delta G \ge 0\), la hidrólisis del ATP deja de ser espontánea y el motor molecular celular se detiene por completo, causando la muerte celular por incapacidad de realizar trabajo.
    """)
