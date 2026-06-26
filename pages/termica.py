import streamlit as st

from components.cards import concept, metric_row
from components.charts import build_calor_chart
from components.professor import prof
from engine import SUBSTANCIAS_CALOR_ESPECIFICO
from formulas.calor import calcular_calor_sensivel, converter_temperatura

# PROFESSOR
st.markdown('<div class="mb-3.5"><span class="badge badge-error badge-outline">Ciências Térmicas · Módulo 1 de 4</span></div>', unsafe_allow_html=True)
prof("Antes de qualquer cálculo, precisamos diferenciar três conceitos fundamentais da termodinâmica: "
     "<strong>temperatura</strong> (agitação molecular), <strong>calor</strong> (energia em trânsito) "
     "e <strong>energia interna</strong> (energia armazenada)."
     
     "Esses conceitos serão a base para todos os módulos seguintes.")

st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-1.5">Teoria</div>', unsafe_allow_html=True)

concept(
        num=1, subtitulo="escala de temperatura",
        titulo="Temperatura e escalas de medição",
        formula_badge="T(K) = T(°C) + 273,15",
        corpo_bullets=[
            "Temperatura mede a energia cinética média das moléculas.",
            "Kelvin é a escala absoluta usada em termodinâmica.",
            "Celsius e Fahrenheit são escalas relativas do cotidiano.",
        ],
        formula_expr="T(K) = T(°C) + 273,15 &nbsp;|&nbsp; T(°F) = T(°C) × 9/5 + 32",
        formula_vars="Sempre converta para Kelvin antes de aplicar em PV = nRT ou ΔU = n·Cᵥ·ΔT",
        ex_enunciado="Converter 150 °C para Kelvin e Fahrenheit:",
        ex_resposta="K = 150 + 273,15 = 423,15 K   °F = 150 × 9/5 + 32 = 302 °F",
    )

concept(
        num=2, subtitulo="calor sensível",
        titulo="Calor — energia em trânsito",
        formula_badge="Q = m · c · ΔT",
        corpo_bullets=[
            "Calor (Q) é energia que flui de uma região quente para uma fria devido a uma diferença de temperatura — não é uma propriedade do sistema, é um processo.",
            "O <strong>calor específico c</strong> depende do material: água (4186 J/kg·K) armazena ~8× mais energia que o aço (500 J/kg·K) para a mesma massa.",
            "Calor sensível não muda o estado da matéria — apenas a temperatura. Mudança de fase exige calor latente (L), que não entra neste módulo.",
        ],
        formula_expr="Q = m · c · ΔT",
        formula_vars="Q (J) = calor &nbsp;|&nbsp; m (kg) = massa &nbsp;|&nbsp; c (J/kg·K) = calor específico &nbsp;|&nbsp; ΔT (K) = variação de temperatura",
        ex_enunciado="Calor para aquecer 5 kg de água de 20 °C a 80 °C (ΔT = 60 K):",
        ex_resposta="Q = 5 × 4186 × 60 = 1 255 800 J ≈ 1 256 kJ",
        aviso="Convenção: Q > 0 → sistema absorve calor. Q < 0 → sistema cede calor à vizinhança.",
    )

concept(
        num=3, subtitulo="energia interna",
        titulo="Energia interna — energia armazenada",
        formula_badge="ΔU = n · Cᵥ · ΔT",
        corpo_bullets=[
            "Energia interna (U) é a soma de todas as energias cinéticas e potenciais microscópicas do sistema.",
            "Para um <strong>gás ideal</strong>, U depende <em>somente</em> da temperatura: ΔU = n·Cᵥ·ΔT. Não depende de P nem V.",
            "Quando calor entra num sistema fechado, ele pode aumentar U (elevar T), realizar trabalho mecânico (W), ou ambos — é isso que a 1ª Lei descreve.",
        ],
        formula_expr="ΔU = n · Cᵥ · ΔT",
        formula_vars="n (mol) = quantidade de substância &nbsp;|&nbsp; Cᵥ (J/mol·K) = calor específico a volume constante &nbsp;|&nbsp; ΔT (K)",
        ex_enunciado="ΔU de 10 mol de N₂ (Cᵥ = 20,8 J/mol·K) aquecido em 50 K:",
        ex_resposta="ΔU = 10 × 20,8 × 50 = 10 400 J = 10,4 kJ",
    )


# SEPARADOR
st.markdown("---")
st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-1.5">Experimento interativo</div>', unsafe_allow_html=True)

# EXPERIMENTO (INPUTS)

col1, col2 = st.columns(2)

with col1:
    sub_nome = st.selectbox(
        "Substância",
        list(SUBSTANCIAS_CALOR_ESPECIFICO.keys()),
        format_func=lambda n: f"{n} — {SUBSTANCIAS_CALOR_ESPECIFICO[n]['c']} J/kg·K",
    )

    c_val = SUBSTANCIAS_CALOR_ESPECIFICO[sub_nome]["c"]

    t_ini = st.slider("Temperatura inicial (°C)", -50, 300, 25)
    massa = st.slider("Massa (kg)", 0.1, 200.0, 2.0, step=0.1)
    delta_t_val = st.slider("Variação ΔT (K)", 1, 500, 50)

with col2:
    temps = converter_temperatura(t_ini)
    calor = calcular_calor_sensivel(massa, c_val, delta_t_val)

    metric_row([
        ("Temperatura (K)", f"{temps['kelvin']:.2f}", "K"),
        ("Temperatura (°F)", f"{temps['fahrenheit']:.1f}", "°F"),
    ])

    metric_row([
        ("Calor específico", f"{c_val}", "J/kg·K"),
        ("Energia Q", f"{calor['Q_kJ']:.2f}", "kJ"),
    ])

    st.success(
        f"O sistema absorveu aproximadamente {calor['Q_kJ']:.2f} kJ de energia térmica."
    )


# GRÁFICO
fig_q = build_calor_chart(massa, c_val, delta_t_val, calor["Q_kJ"])
st.plotly_chart(fig_q, width="stretch")


# =========================
# INTERPRETAÇÃO FÍSICA
# =========================
st.markdown("### 🧠 Interpretação física")

st.info("""
O calor calculado representa a energia necessária para aumentar a agitação molecular do material.

Materiais com maior calor específico exigem mais energia para variar a temperatura,
como a água em comparação com metais.
""")