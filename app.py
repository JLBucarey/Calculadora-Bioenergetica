import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de la página web
st.set_page_config(page_title="Termodinámica Biológica: Equilibrio vs Estado Estacionario", layout="wide")

st.title("🧪 Termodinámica Biológica e Hidrólisis del ATP")
st.write("Explora la diferencia crítica entre el equilibrio químico pasivo y el estado estacionario activo de una célula viviente.")

st.markdown("---")

# --- PARAMETROS GLOBALES EN LA BARRA LATERAL (Tomados de tu Excel) ---
st.sidebar.header("⚙️ Constantes del Sistema")
R = 0.008315  # KJ/(mol*K)
T = st.sidebar.number_input("Temperatura (K)", value=298.0, step=1.0) # 25°C según tu Excel
RT = R * T

st.sidebar.markdown("---")
st.sidebar.header("🔋 Propiedades del ATP")
dg0_atp = -30.0  # ΔGo’ = -30 KJ/mol del ATP según tu archivo

# --- CREACIÓN DE PESTAÑAS (TABS) ---
tab1, tab2 = st.tabs(["📉 Pestaña 1: Concentraciones en el Equilibrio", "⚡ Pestaña 2: Estado Estacionario Celular"])

# ==========================================
# PESTAÑA 1: EL ENFOQUE DEL EQUILIBRIO PASIVO
# ==========================================
with tab1:
    st.subheader("Simulación de Concentraciones Finales en el Equilibrio (ΔG = 0)")
    st.write("Descubre cómo impacta la variación de la Energía Libre Estándar (ΔG°') en las concentraciones finales de una reacción.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Control deslizante dinámico basado en tu casilla amarilla del Excel
        dg0_variable = st.slider(
            "Modificar ΔG°' de la reacción (KJ/mol):", 
            min_value=-60.0, max_value=60.0, value=50.0, step=5.0  # Por defecto +50 como tu ejemplo
        )
        
        sust_inicial = st.number_input("Concentración Inicial de Sustrato A (M):", value=1.0, min_value=0.01)
        
        # --- CÁLCULO MATEMÁTICO DEL EXCEL (Resolución Cuadrática) ---
        keq = np.exp(-dg0_variable / RT)
        
        # Ecuación cuadrática: x^2 + keq*x - keq*sust_inicial = 0
        a, b, c = 1.0, keq, -keq * sust_inicial
        discriminante = (b**2) - (4 * a * c)
        x_eq = (-b + np.sqrt(discriminante)) / (2 * a)
        
        sust_eq = sust_inicial - x_eq
        
        # Despliegue de métricas calculadas en el Excel
        st.markdown("#### Datos de Salida Matemáticos:")
        st.metric(label="Constante de Equilibrio (Keq)", value=f"{keq:.5e}")
        st.metric(label="Avance de la reacción (x)", value=f"{x_eq:.5e} M")
        
    with col2:
        # Gráfico dinámico de barras de la Pestaña 1
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=['Sustrato A', 'Producto B', 'Producto C'], y=[sust_inicial, 0, 0], name='Inicio', marker_color='#FFA07A'))
        fig1.add_trace(go.Bar(x=['Sustrato A', 'Producto B', 'Producto C'], y=[sust_eq, x_eq, x_eq], name='En el Equilibrio', marker_color='#20B2AA'))
        
        fig1.update_layout(
            barmode='group', yaxis_title='Concentración (M)', 
            title=f"Concentraciones para un ΔG°' de {dg0_variable} KJ/mol",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=380
        )
        st.plotly_chart(fig1, use_container_width=True)

# ==========================================
# PESTAÑA 2: ESTADO ESTACIONARIO ACTIVO (CELULAR)
# ==========================================
with tab2:
    st.subheader("Análisis de la Célula Viva: Caso Hidrólisis del ATP (ATP ↔ ADP + Pi)")
    st.write("En la vida real, las concentraciones se mantienen estables pero **lejos del equilibrio** gracias al metabolismo activo.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("##### Concentraciones en Estado Estacionario (M o mM)")
        # Inputs interactivos basados en el "Estado estacionario: 1, 1, 1" de tu Excel
        c_atp = st.number_input("Concentración de ATP [Sustrato A]", value=1.0, min_value=0.0001, format="%.4f")
        c_adp = st.number_input("Concentración de ADP [Producto B]", value=1.0, min_value=0.0001, format="%.4f")
        c_pi  = st.number_input("Concentración de Pi  [Producto C]", value=1.0, min_value=0.0001, format="%.4f")
        
        # --- CÁLCULO DE ΔG REAL ---
        # Cociente de reacción Q = ([ADP] * [Pi]) / [ATP]
        Q = (c_adp * c_pi) / c_atp
        
        # ΔG = ΔG°' + RT * ln(Q)
        dg_real = dg0_atp + (RT * np.log(Q))
        
    with col2:
        st.markdown("##### ⚡ Energía Libre de Gibbs Real calculado:")
        
        # Cuadro de color dinámico según el resultado energético del Estado Estacionario
        if dg_real < -10:
            st.success(f"### ΔG Real = {dg_real:.2f} KJ/mol\n\n**¡Trabajo Celular Disponible!** La reacción es altamente exergónica. La célula mantiene este motor encendido lejos del equilibrio dinámico.")
        elif dg_real > 10:
            st.error(f"### ΔG Real = {dg_real:.2f} KJ/mol\n\n**Condición no viable:** La reacción requiere un bombeo inverso masivo de energía externa.")
        else:
            st.warning(f"### ΔG Real = {dg_real:.2f} KJ/mol\n\n**Zona de Peligro (Cerca del Equilibrio):** Si el ΔG se acerca a cero, la célula pierde su capacidad de realizar trabajo y colapsa (muerte celular).")
            
        # Gráfico comparativo de la Pestaña 2: Q vs Keq de la hidrólisis del ATP
        keq_atp = np.exp(-dg0_atp / RT)
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=['Cociente Real Celular (Q)', 'Constante de Equilibrio (Keq)'],
            y=[Q, keq_atp],
            marker_color=['#9370DB', '#FFD700']
        ))
        fig2.update_layout(
            title="Comparativa Escala Logarítmica: Estado Actual (Q) vs Meta Teórica (Keq)",
            yaxis_type="log", yaxis_title="Valor (Escala Logarítmica)",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280
        )
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption("**Nota metodológica:** El agua ($H_2O$) actúa como disolvente puro, por lo que su actividad termodinámica es igual a 1 y se omite en el cociente de reacción $Q$ y en la constante $K_{eq}$.")
