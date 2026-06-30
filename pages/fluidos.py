import streamlit as st

from components.cards import concept, metric_row
from components.charts import build_manometro_chart
from components.professor import prof
from engine import FLUIDOS_MANOMETRIA
from formulas.fluidos import calcular_p_atm, calcular_pressao_reservatorio

st.markdown('<div class="mb-3.5"><span class="badge badge-success badge-outline">Mecânica dos Fluidos · Módulo 3 de 4</span></div>', unsafe_allow_html=True)
prof("""
<p>Agora saímos das moléculas e olhamos para colunas inteiras de fluido.</p>

<p>A pressão hidrostática aumenta linearmente com a profundidade,
independente da forma do recipiente, isso é o Princípio de Pascal.</p>

<p>O manômetro transforma essa pressão em uma altura de coluna legível.</p>
""")


st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-1.5">Teoria</div>', unsafe_allow_html=True)

concept(
        num=1, subtitulo="pressão hidrostática",
        titulo="Pressão em fluidos estáticos",
        formula_badge="P = P₀ + ρ·g·h",
        corpo_bullets=[
            "Em um fluido em repouso, cada camada suporta o peso de tudo acima dela — a pressão aumenta linearmente com a profundidade h.",
            "A pressão num ponto depende apenas de h e de ρ do fluido, não da forma do recipiente (<strong>Princípio de Pascal</strong>).",
            "Pontos à mesma altura no mesmo fluido contínuo em repouso têm sempre a mesma pressão.",
        ],
        formula_expr="P = P₀ + ρ · g · h",
        formula_vars="P₀ (Pa) = pressão de referência &nbsp;|&nbsp; ρ (kg/m³) = massa específica &nbsp;|&nbsp; g = 9,81 m/s² &nbsp;|&nbsp; h (m) = altura",
        ex_enunciado="P no fundo de um tanque com 3 m de água (ρ=1000 kg/m³), P₀=101325 Pa:",
        ex_resposta="P = 101325 + 1000×9,81×3 = 101325 + 29430 = 130 755 Pa ≈ 130,8 kPa",
    )

concept(
        num=2, subtitulo="pressão atmosférica",
        titulo="Variação com a altitude",
        formula_badge="P_atm = P_mar − ρ_ar·g·z",
        corpo_bullets=[
            "A pressão atmosférica diminui com a altitude porque há menos coluna de ar acima do ponto.",
            "A equação barométrica simplificada usa densidade média do ar ρ ≈ 1,2 kg/m³ e vale até ~4000 m.",
            "Isso afeta manômetros instalados em locais elevados: a P_atm de referência é menor.",
        ],
        formula_expr="P_atm(z) = 101 325 − 1,2 · 9,81 · z",
        formula_vars="z (m) = altitude acima do nível do mar &nbsp;|&nbsp; P_mar = 101 325 Pa",
        ex_enunciado="P_atm em Belo Horizonte (altitude ≈ 850 m):",
        ex_resposta="P = 101325 − 1,2×9,81×850 = 101325 − 10005 = 91 320 Pa ≈ 91,3 kPa",
    )

concept(
        num=3, subtitulo="manometria",
        titulo="Tubo em U e tubo inclinado",
        formula_badge="P_abs = P_atm + ρ·g·h_ef",
        corpo_bullets=[
            "O manômetro conecta um reservatório pressurizado ao ambiente. A diferença de nível h indica a pressão manométrica.",
            "Tubo inclinado: h_efetivo = L·sen(θ). Um pequeno ΔP gera deslocamento L grande, <strong>aumentando a precisão</strong> da leitura por fator 1/sen(θ).",
            "Pressão absoluta = pressão manométrica + P_atm. Nunca confundir as duas.",
        ],
        formula_expr="P_abs = P_atm + ρ · g · h_efetivo &nbsp;|&nbsp; h_ef = L · sen(θ)",
        formula_vars="L (m) = leitura no tubo inclinado &nbsp;|&nbsp; θ = ângulo de inclinação",
        ex_enunciado="Manômetro de mercúrio (ρ=13600), h=0,15 m, P_atm=101325 Pa:",
        ex_resposta="P_hid = 13600×9,81×0,15 = 20012 Pa  P_abs = 121 337 Pa ≈ 121,3 kPa",
        aviso="Pressão absoluta = Pressão manométrica + P_atm. Não confundir as duas!",
    )

st.markdown("---")
st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-1.5">Experimento interativo</div>', unsafe_allow_html=True)

# EXPERIMENTO (INPUTS)

col1 = st.columns(1)


st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-1.5">Calculadora + visualização do manômetro</div>', unsafe_allow_html=True)

fluido_nome = st.selectbox("Fluido manométrico", list(FLUIDOS_MANOMETRIA.keys()))
rho_man = FLUIDOS_MANOMETRIA[fluido_nome]["rho"]
cor_fluido = FLUIDOS_MANOMETRIA[fluido_nome]["cor"]
altitude_val = st.slider("Altitude do sistema (m)", 0, 4000, 325, 25)
tipo_man = st.radio("Tipo de manômetro", ["Tubo em U Vertical", "Tubo Inclinado"], horizontal=True)
angulo_val = 30.0
if tipo_man == "Tubo Inclinado":
    angulo_val = float(st.slider("Ângulo de inclinação θ (°)", 10, 80, 30))
h_man = st.slider("Deflexão / altura da coluna h (m)", 0.05, 2.0, 0.50, 0.05)

res3 = calcular_pressao_reservatorio(
    calcular_p_atm(altitude_val), rho_man, h_man, tipo_man, angulo_val
)

metric_row([
    ("P atmosférica local", f"{res3['P_atm_kPa']:.2f}", "kPa"),
    ("P hidrostática", f"{res3['P_hid_kPa']:.3f}", "kPa"),
    ("P absoluta", f"{res3['P_abs_kPa']:.2f}", "kPa"),
])

h_ef = res3["h_efetivo"]
st.info(f"h efetivo = {h_ef:.4f} m → P_hid = {rho_man} × 9,81 × {h_ef:.4f} = **{res3['P_hid_kPa']:.3f} kPa**")

fig_man = build_manometro_chart(h_man, tipo_man, angulo_val, cor_fluido, fluido_nome)
st.plotly_chart(fig_man, width="stretch")