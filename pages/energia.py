import streamlit as st

from components.cards import concept, metric_row
from components.charts import build_pv_chart
from components.professor import prof
from engine import GASES_TERMICOS
from formulas.termodinamica import calcular_processo_termodinamico

st.markdown('<div class="mb-3.5"><span class="badge badge-primary badge-outline">Conservação de Energia · Módulo 2 de 4</span></div>', unsafe_allow_html=True)
prof(
    "Na termodinâmica, energia não desaparece, ela apenas muda de forma.<br><br>"
    "Quando um gás em um cilindro com pistão recebe calor, essa energia pode aumentar sua energia interna ou ser convertida em trabalho mecânico ao movimentar o pistão.<br><br>"
    "A forma como esse trabalho é calculado pode ser visualizada no diagrama P×V, "
    "onde ele corresponde à área sob a curva do processo termodinâmico."
)


st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-1.5">Teoria</div>', unsafe_allow_html=True)

concept(
        num=1, subtitulo="1ª Lei da Termodinâmica",
        titulo="Conservação de energia em sistemas fechados",
        formula_badge="ΔU = Q − W",
        corpo_bullets=[
            "A variação de energia interna (ΔU) é igual ao calor absorvido (Q) menos o trabalho realizado pelo sistema (W).",
            "Para gases ideais, ΔU depende <em>somente</em> da temperatura, independentemente do processo.",
            "A relação de Mayer conecta Cₚ e Cᵥ: Cₚ − Cᵥ = R. Isso vale para qualquer gás ideal.",
        ],
        formula_expr="ΔU = Q − W &nbsp;|&nbsp; ΔU = n·Cᵥ·ΔT &nbsp;|&nbsp; Cₚ = Cᵥ + R",
        formula_vars="R = 8,314 J/mol·K &nbsp;|&nbsp; Cᵥ = R/(γ−1) &nbsp;|&nbsp; γ = Cₚ/Cᵥ (N₂: γ=1,4)",
        ex_enunciado="10 mol de N₂ absorvem Q=50 kJ e realizam W=20 kJ. Qual ΔU?",
        ex_resposta="ΔU = Q − W = 50 − 20 = 30 kJ   ΔT = 30000/(10×20,8) = 144 K",
    )

concept(
        num=2, subtitulo="trabalho de fronteira",
        titulo="Área sob a curva P×V = trabalho",
        formula_badge="W = ∫P dV",
        corpo_bullets=[
            "Quando um gás muda de volume, o trabalho realizado é a integral de P em relação a V.",
            "No diagrama P×V, isso corresponde geometricamente à <strong>área entre a curva e o eixo V</strong>.",
            "Processos diferentes têm curvas P×V diferentes — e portanto trabalhos diferentes para o mesmo ΔV.",
        ],
        formula_expr="W = ∫ P dV",
        formula_vars="Para cada processo, substitua P como função de V antes de integrar",
        ex_enunciado="Processo isobárico: P=200 kPa, V₁=1 m³, V₂=2 m³. Qual W?",
        ex_resposta="W = P·ΔV = 200 000 × (2−1) = 200 000 J = 200 kJ",
    )

st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-1.5">Processos termodinâmicos</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="grid grid-cols-2 gap-2 mb-4">
        <div class="alert alert-info text-sm py-2.5">
            <div><strong class="block text-xs">Isotérmico (T = cte)</strong>
            W = nRT·ln(V₂/V₁)<br>Q = W &nbsp;|&nbsp; ΔU = 0</div>
        </div>
        <div class="alert alert-success text-sm py-2.5">
            <div><strong class="block text-xs">Isobárico (P = cte)</strong>
            W = P·ΔV = nR·ΔT<br>Q = n·Cₚ·ΔT</div>
        </div>
        <div class="alert alert-error text-sm py-2.5">
            <div><strong class="block text-xs">Adiabático (Q = 0)</strong>
            PVᵞ = cte<br>W = −ΔU = −n·Cᵥ·ΔT</div>
        </div>
        <div class="alert text-sm py-2.5 bg-secondary/20 text-secondary-content">
            <div><strong class="block text-xs">Politrópico (PVⁿ = cte)</strong>
            W = (P₁V₁ − P₂V₂)/(n−1)<br>Q = ΔU + W</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-1.5">Calculadora + diagrama P×V interativo</div>', unsafe_allow_html=True)

processo = st.selectbox("Processo termodinâmico", ["Isotérmico", "Isobárico", "Adiabático", "Politrópico"])
gas = st.selectbox("Gás", list(GASES_TERMICOS.keys()))
c1, c2 = st.columns(2)
with c1:
        v1_val = st.slider("Volume inicial V₁ (m³)", 0.5, 4.0, 1.0, 0.1)
with c2:
        razao = st.slider("Razão V₂/V₁", 0.3, 4.0, 2.0, 0.1)
n_exp = 1.3
if processo == "Politrópico":
        n_exp = st.slider("Expoente politrópico n", 1.01, 2.50, 1.30, 0.05)

res2 = calcular_processo_termodinamico(processo, gas, v1_val, razao, n_exp)

fig_pv = build_pv_chart(res2, processo)
st.plotly_chart(fig_pv, width="stretch")

metric_row([
        ("Trabalho W", f"{res2['W_kJ']:.2f}", "kJ"),
        ("Calor Q", f"{res2['Q_kJ']:.2f}", "kJ"),
        ("ΔU", f"{res2['delta_U_kJ']:.2f}", "kJ"),
    ])
metric_row([
        ("T final", f"{res2['T_final_C']:.1f}", "°C"),
        ("P inicial", f"{res2['P1_kPa']:.1f}", "kPa"),
        ("P final", f"{res2['P2_kPa']:.1f}", "kPa"),
    ])

hints = {
        "Isotérmico":  "ΔU = 0 pois T não muda. Todo o calor absorvido vira trabalho de expansão.",
        "Isobárico":   "Pressão constante: o calor se divide entre elevar T (ΔU) e fazer trabalho (W).",
        "Adiabático":  "Q = 0: sem troca de calor. O trabalho vem 100% da queda de energia interna.",
        "Politrópico": f"Caso geral com n={n_exp:.2f}. n=1→isotérmico | n=γ→adiabático | n=0→isobárico.",
    }
st.info(hints[processo])
