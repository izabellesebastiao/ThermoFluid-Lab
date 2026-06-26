import streamlit as st

from components.cards import concept, metric_row
from components.charts import build_balanco_chart, build_cilindro_chart
from components.professor import prof
from engine import FLUIDOS_MANOMETRIA, GASES_TERMICOS
from formulas.termodinamica import calcular_sistema_acoplado

st.markdown('<div class="mb-3.5"><span class="badge badge-secondary badge-outline">Sistema Integrado · Módulo 4 de 4</span></div>', unsafe_allow_html=True)
prof("Módulo de síntese! Um gás confinado recebe calor (Módulos 1 e 2) e precisa vencer "
     "a pressão de uma coluna de fluido (Módulo 3) para mover o pistão. "
     "Temperatura, pressão e volume interagem simultaneamente num processo <strong>isobárico</strong>.")


st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-1.5">Teoria</div>', unsafe_allow_html=True)

concept(
        num=1, subtitulo="equilíbrio de forças",
        titulo="Pressão total sobre o pistão",
        formula_badge="P_tot = P_atm + ρ·g·h",
        corpo_bullets=[
            "O pistão está em equilíbrio entre a pressão do gás por baixo e a pressão total (atmosférica + hidrostática) por cima.",
            "A pressão do fluido é constante durante o processo — por isso o gás se expande de forma <strong>isobárica</strong>.",
            "Aumentar h ou ρ do fluido aumenta P_total, exigindo mais calor para o mesmo deslocamento.",
        ],
        formula_expr="P_total = P_atm + ρ · g · h",
        formula_vars="Pressão constante que o gás precisa vencer para mover o pistão",
        ex_enunciado="P_total com 1 m de água (ρ=1000) sobre o pistão, P_atm=101325 Pa:",
        ex_resposta="P_tot = 101325 + 1000×9,81×1 = 111 135 Pa ≈ 111,1 kPa",
    )

concept(
        num=2, subtitulo="expansão do gás",
        titulo="Deslocamento do pistão pelo calor",
        formula_badge="Δy = ΔV / A",
        corpo_bullets=[
            "Com P constante (isobárico), o calor injetado Q eleva T e portanto V pelo gás ideal.",
            "O aumento de volume ΔV = nR·ΔT/P_total move o pistão uma distância Δy = ΔV/A.",
            "Pistão com área menor → maior deslocamento para o mesmo ΔV (amplificação geométrica).",
        ],
        formula_expr="Q = n·Cₚ·ΔT &nbsp;|&nbsp; ΔV = nR·ΔT / P_total &nbsp;|&nbsp; Δy = ΔV / A",
        formula_vars="A (m²) = área do pistão &nbsp;|&nbsp; n = 10 mol do gás escolhido na simulação",
        ex_enunciado="Q=10 kJ, P_tot=111 kPa, A=0,05 m², n=10 mol N₂ (Cₚ=29,1 J/mol·K):",
        ex_resposta="ΔT = 10000/(10×29,1) = 34,4 K &nbsp;|&nbsp; ΔV = 10×8,314×34,4/111000 = 0,026 m³ &nbsp;|&nbsp; Δy = 0,52 m",
    )

concept(
        num=3, subtitulo="1ª Lei aplicada",
        titulo="Balanço energético do sistema",
        formula_badge="Q = ΔU + W",
        corpo_bullets=[
            "Num processo isobárico, Q se divide entre ΔU (elevar T do gás) e W (trabalho mecânico contra o fluido).",
            "A verificação Q = ΔU + W confirma a conservação de energia — o resultado na calculadora mostra isso em tempo real.",
            "O gráfico de balanço mostra as três grandezas lado a lado para você visualizar a divisão da energia.",
        ],
        formula_expr="Q = ΔU + W &nbsp;|&nbsp; W = P_total · ΔV &nbsp;|&nbsp; ΔU = n·Cᵥ·ΔT",
        formula_vars="Para N₂: Cᵥ = 20,8 J/mol·K &nbsp;|&nbsp; Cₚ = 29,1 J/mol·K &nbsp;|&nbsp; γ = 1,4",
        ex_enunciado="Verificar: Q=10 kJ, ΔU=n·Cᵥ·ΔT=10×20,8×34,4=7,15 kJ. Qual W?",
        ex_resposta="W = Q − ΔU = 10 − 7,15 = 2,85 kJ ✓ (= P_tot × ΔV = 111000×0,026 ≈ 2,85 kJ)",
    )


st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-1.5">Simulador integrado</div>', unsafe_allow_html=True)

gas_ac = st.selectbox("Gás confinado no cilindro", list(GASES_TERMICOS.keys()), key="gas_ac")
fluido_ac = st.selectbox("Fluido sobre o pistão", list(FLUIDOS_MANOMETRIA.keys()), key="fl_ac")
rho_ac = FLUIDOS_MANOMETRIA[fluido_ac]["rho"]
cor_ac = FLUIDOS_MANOMETRIA[fluido_ac]["cor"]
h_ac = st.slider("Altura da coluna de fluido h (m)", 0.1, 3.0, 0.5, 0.1, key="h_ac")
q_ac = st.slider("Calor injetado Q (kJ)", 1, 50, 15, key="q_ac")
area_ac = st.slider("Área do pistão A (m²)", 0.01, 0.20, 0.05, 0.01, key="area_ac")

res4 = calcular_sistema_acoplado(rho_ac, h_ac, q_ac, area_ac, gas_ac)

metric_row([
        ("P total", f"{res4['P_total_kPa']:.2f}", "kPa"),
        ("Força do fluido", f"{res4['F_fluido_kN']:.3f}", "kN"),
    ])
metric_row([
        ("Trabalho W", f"{res4['W_kJ']:.3f}", "kJ"),
        ("ΔU", f"{res4['delta_U_kJ']:.3f}", "kJ"),
        ("T final", f"{res4['T_final_C']:.1f}", "°C"),
    ])
st.success(
        f"Pistão subiu **{res4['deslocamento_cm']:.2f} cm** · "
        f"ΔV = {res4['delta_V_L']:.2f} L · "
        f"ΔT = {res4['delta_T']:.2f} K · "
        f"Q = ΔU + W = {res4['delta_U_kJ'] + res4['W_kJ']:.2f} kJ ✓"
    )

fig_cil = build_cilindro_chart(res4, h_ac, q_ac, cor_ac, fluido_ac)
st.plotly_chart(fig_cil, width="stretch")

fig_bal = build_balanco_chart(res4)
st.plotly_chart(fig_bal, width="stretch")
