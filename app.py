import numpy as np
import streamlit as st
import plotly.graph_objects as go
from engine import (
    SUBSTANCIAS_CALOR_ESPECIFICO,
    FLUIDOS_MANOMETRIA,
    GASES_TERMICOS,
    converter_temperatura,
    calcular_calor_sensivel,
    calcular_processo_termodinamico,
    calcular_p_atm,
    calcular_pressao_reservatorio,
    calcular_sistema_acoplado,
)

# ──────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ThermoFluid Lab",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Hero da home ── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 1rem 2rem;
    border-bottom: 1px solid #1e293b;
    margin-bottom: 2rem;
}
.hero-eyebrow {
    font-size: 0.68rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: .14em; color: #475569; margin-bottom: .75rem;
}
.hero-title {
    font-size: 2.6rem; font-weight: 700; color: #f1f5f9;
    line-height: 1.1; margin-bottom: .75rem;
}
.hero-title em { color: #3b82f6; font-style: normal; }
.hero-sub {
    font-size: .95rem; color: #94a3b8; line-height: 1.75;
    max-width: 520px; margin: 0 auto 1.5rem;
}
.prof-bubble {
    display: inline-flex; align-items: center; gap: 10px;
    background: #0f172a; border: 1px solid #1e3a5f;
    border-radius: 14px; padding: .65rem 1.1rem;
}
.prof-bubble-av {
    width: 34px; height: 34px; border-radius: 50%;
    background: #1e3a5f; display: flex; align-items: center;
    justify-content: center; font-size: 17px; flex-shrink: 0;
}
.prof-bubble-text { font-size: .82rem; color: #93c5fd; font-style: italic; text-align: left; }

/* ── Cards de módulo (home) ── */
.mod-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 1.75rem; }
.mod-card {
    background: #0f172a; border: 1px solid #1e293b;
    border-radius: 12px; padding: 1.1rem 1rem;
    position: relative; overflow: hidden;
}
.mod-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
}
.mod-1::before { background: #ef4444; }
.mod-2::before { background: #3b82f6; }
.mod-3::before { background: #22c55e; }
.mod-4::before { background: #a855f7; }
.mod-num { font-size: .65rem; font-weight: 600; text-transform: uppercase; letter-spacing: .1em; color: #475569; margin-bottom: .5rem; }
.mod-icon { font-size: 1.6rem; margin-bottom: .5rem; display: block; }
.mod-title { font-size: .92rem; font-weight: 600; color: #e2e8f0; margin-bottom: .35rem; }
.mod-desc { font-size: .78rem; color: #64748b; line-height: 1.6; margin-bottom: .65rem; }
.mod-chips { display: flex; flex-wrap: wrap; gap: 4px; }
.chip {
    font-size: .65rem; padding: 2px 7px; border-radius: 20px;
    border: 1px solid; font-weight: 500;
}
.chip-1 { border-color: #7f1d1d; color: #fca5a5; }
.chip-2 { border-color: #1e3a5f; color: #93c5fd; }
.chip-3 { border-color: #14532d; color: #86efac; }
.chip-4 { border-color: #3b0764; color: #d8b4fe; }

/* ── Fluxo de progressão ── */
.flow-wrap { display: flex; align-items: center; justify-content: center; gap: 8px; flex-wrap: wrap; margin-bottom: 2rem; }
.flow-node { font-size: .75rem; font-weight: 600; padding: 5px 12px; border-radius: 20px; }
.fn1 { background: #450a0a; color: #fca5a5; }
.fn2 { background: #0c1a3a; color: #93c5fd; }
.fn3 { background: #052e16; color: #86efac; }
.fn4 { background: #1a0533; color: #d8b4fe; }
.flow-arr { color: #334155; font-size: 1rem; }

/* ── Conceito de teoria (mesclado) ── */
.concept-block {
    background: #0f172a; border: 1px solid #1e293b;
    border-radius: 12px; overflow: hidden; margin-bottom: 1rem;
}
.concept-header {
    background: #0c1a3a; border-bottom: 1px solid #1e3a5f;
    padding: .75rem 1rem; display: flex; align-items: center; gap: 10px;
}
.concept-num {
    width: 26px; height: 26px; min-width: 26px; border-radius: 50%;
    background: #1e3a5f; display: flex; align-items: center; justify-content: center;
    font-size: .75rem; font-weight: 700; color: #93c5fd;
}
.concept-heading { flex: 1; }
.concept-sub { font-size: .65rem; color: #475569; text-transform: uppercase; letter-spacing: .08em; }
.concept-title { font-size: .9rem; font-weight: 600; color: #bfdbfe; line-height: 1.2; }
.concept-formula-badge {
    font-family: 'Courier New', monospace; font-size: .78rem;
    color: #60a5fa; background: #172554; border: 1px solid #1e3a5f;
    border-radius: 6px; padding: 3px 8px; white-space: nowrap;
}
.concept-body { padding: .85rem 1rem; }
.concept-text { font-size: .83rem; color: #94a3b8; line-height: 1.7; margin-bottom: .65rem; }

.formula-line {
    border-left: 3px solid #3b82f6; background: #020617;
    padding: .55rem .85rem; border-radius: 0 6px 6px 0;
    font-family: 'Courier New', monospace; font-size: .95rem;
    color: #93c5fd; margin: .5rem 0 .2rem;
}
.formula-vars { font-size: .72rem; color: #475569; margin-bottom: .6rem; }

.example-box {
    background: #0a0f1e; border: 1px solid #1e293b; border-radius: 8px;
    padding: .65rem .85rem;
}
.example-label { font-size: .62rem; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; color: #3b82f6; margin-bottom: .3rem; }
.example-q { font-size: .8rem; color: #64748b; margin-bottom: .3rem; }
.example-ans { font-family: 'Courier New', monospace; font-size: .85rem; color: #22c55e; }

.bullet-row { display: flex; gap: 8px; align-items: flex-start; margin-bottom: .4rem; }
.bullet-dot { width: 5px; height: 5px; min-width: 5px; border-radius: 50%; background: #3b82f6; margin-top: 6px; }
.bullet-text { font-size: .83rem; color: #94a3b8; line-height: 1.65; }

.warn-note {
    background: #1c1407; border-left: 3px solid #f59e0b;
    border-radius: 0 8px 8px 0; padding: .5rem .75rem;
    font-size: .8rem; color: #fbbf24; margin-bottom: .85rem;
}

/* ── Processo cards (aba 2) ── */
.proc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 1rem; }
.proc-card { border-radius: 8px; padding: .65rem .85rem; font-size: .8rem; line-height: 1.55; }
.proc-card strong { display: block; margin-bottom: 3px; font-size: .77rem; }
.proc-iso    { background:#1e3a5f; color:#93c5fd; } .proc-iso strong    { color:#60a5fa; }
.proc-isobar { background:#14532d; color:#86efac; } .proc-isobar strong { color:#4ade80; }
.proc-adiab  { background:#4c1d1d; color:#fca5a5; } .proc-adiab strong  { color:#f87171; }
.proc-polit  { background:#2e1065; color:#d8b4fe; } .proc-polit strong  { color:#c084fc; }

/* ── Professor card ── */
.prof-card {
    display: flex; gap: 12px; align-items: flex-start;
    background: #0c1a3a; border-left: 4px solid #3b82f6;
    border-radius: 0 10px 10px 0; padding: .9rem 1.1rem; margin-bottom: 1.25rem;
}
.prof-avatar { font-size: 2rem; line-height: 1; }
.prof-name   { font-size: .68rem; font-weight: 700; color: #3b82f6; text-transform: uppercase; letter-spacing: .1em; margin-bottom: 2px; }
.prof-text   { font-size: .86rem; color: #93c5fd; line-height: 1.65; }

/* ── Rótulos e seções ── */
.sec-label { font-size: .68rem; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; color: #334155; margin-bottom: .4rem; }
.module-tag { display: inline-block; font-size: .68rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; margin-bottom: .85rem; }
.tag-thermo  { background:#450a0a; color:#fca5a5; }
.tag-fluid   { background:#052e16; color:#86efac; }
.tag-coupled { background:#1a0533; color:#d8b4fe; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────

def prof(texto: str) -> None:
    st.markdown(f"""
    <div class="prof-card">
        <div class="prof-avatar">🧑‍🏫</div>
        <div>
            <div class="prof-name">Prof. Thermo</div>
            <div class="prof-text">{texto}</div>
        </div>
    </div>""", unsafe_allow_html=True)


def concept(num: int, subtitulo: str, titulo: str, formula_badge: str,
            corpo_bullets: list[str], formula_expr: str, formula_vars: str,
            ex_enunciado: str, ex_resposta: str, aviso: str = "") -> None:
    """
    Renderiza um bloco de teoria mesclando Opção A e B.
    Dividido em dois st.markdown para evitar o bug do Streamlit que escapa
    conteúdo de texto dentro de tags HTML aninhadas em f-strings longas.
    """
    bullets_html = "".join(
        f'<div class="bullet-row"><div class="bullet-dot"></div>'
        f'<div class="bullet-text">{b}</div></div>'
        for b in corpo_bullets
    )
    aviso_html = f'<div class="warn-note">&#9888; {aviso}</div>' if aviso else ""

    # Parte 1: cabeçalho + bullets + fórmula (sem conteúdo de texto livre problemático)
    st.markdown(f"""
<div class="concept-block">
  <div class="concept-header">
    <div class="concept-num">{num}</div>
    <div class="concept-heading">
      <div class="concept-sub">{subtitulo}</div>
      <div class="concept-title">{titulo}</div>
    </div>
    <span class="concept-formula-badge">{formula_badge}</span>
  </div>
  <div class="concept-body">
    {bullets_html}
    <div class="formula-line">{formula_expr}</div>
    <div class="formula-vars">{formula_vars}</div>
    {aviso_html}
  </div>
</div>""", unsafe_allow_html=True)

    # Parte 2: exemplo resolvido — st.markdown separado evita escape do conteúdo
    import html as _html
    eq = _html.escape(ex_enunciado)
    er = _html.escape(ex_resposta)
    st.markdown(f"""
<div style="background:#0a0f1e;border:1px solid #1e293b;border-radius:8px;
            padding:.65rem .85rem;margin-top:-.6rem;margin-bottom:1rem;">
  <div style="font-size:.62rem;font-weight:700;text-transform:uppercase;
              letter-spacing:.1em;color:#3b82f6;margin-bottom:.3rem;">Exemplo resolvido</div>
  <div style="font-size:.8rem;color:#64748b;margin-bottom:.3rem;">{eq}</div>
  <div style="font-family:'Courier New',monospace;font-size:.85rem;color:#22c55e;">{er}</div>
</div>""", unsafe_allow_html=True)


def warn(texto: str) -> None:
    st.markdown(f'<div class="warn-note">⚠️ {texto}</div>', unsafe_allow_html=True)


def metric_row(items: list[tuple]) -> None:
    cols = st.columns(len(items))
    for col, (label, valor, unidade) in zip(cols, items):
        col.metric(label, f"{valor} {unidade}")


def hex_rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


CORES_PROCESSO = {
    "Isotérmico":  "#3b82f6",
    "Isobárico":   "#22c55e",
    "Adiabático":  "#ef4444",
    "Politrópico": "#a855f7",
}
PLOTLY_TEMPLATE = "plotly_dark"


# ══════════════════════════════════════════════════════════════
# NAVEGAÇÃO — 5 abas (Home + 4 módulos)
# ══════════════════════════════════════════════════════════════
tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Início",
    "🔥 Ciências Térmicas",
    "⚡ Energia e Trabalho",
    "💧 Estática e Manometria",
    "⚙️ Sistema Acoplado",
])


# ══════════════════════════════════════════════════════════════
# ABA 0 — PÁGINA INICIAL
# ══════════════════════════════════════════════════════════════
with tab0:
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-eyebrow">Engenharia · Fenômenos de Transporte</div>
        <div class="hero-title">Thermo<em>Fluid</em> Lab</div>
        <div class="hero-sub">
            Um simulador interativo para explorar os fundamentos de ciências térmicas
            e mecânica dos fluidos — com teoria, fórmulas e cálculos em cada módulo.
        </div>
        <div class="prof-bubble">
            <div class="prof-bubble-av">🧑‍🏫</div>
            <div class="prof-bubble-text">
                "Cada módulo constrói sobre o anterior. No final, você vai ver energia,
                pressão e temperatura agindo juntas num sistema real."
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">O que você vai aprender</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="mod-grid">
        <div class="mod-card mod-1">
            <div class="mod-num">Módulo 1</div>
            <span class="mod-icon">🔥</span>
            <div class="mod-title">Ciências Térmicas</div>
            <div class="mod-desc">Os três conceitos que todo engenheiro precisa distinguir antes de qualquer cálculo.</div>
            <div class="mod-chips">
                <span class="chip chip-1">Temperatura</span>
                <span class="chip chip-1">Calor sensível</span>
                <span class="chip chip-1">Energia interna</span>
                <span class="chip chip-1">Escalas K · °C · °F</span>
            </div>
        </div>
        <div class="mod-card mod-2">
            <div class="mod-num">Módulo 2</div>
            <span class="mod-icon">⚡</span>
            <div class="mod-title">Energia e Trabalho</div>
            <div class="mod-desc">A 1ª Lei em ação: como calor vira trabalho mecânico em quatro processos distintos.</div>
            <div class="mod-chips">
                <span class="chip chip-2">1ª Lei</span>
                <span class="chip chip-2">Diagrama P×V</span>
                <span class="chip chip-2">Isotérmico</span>
                <span class="chip chip-2">Adiabático</span>
                <span class="chip chip-2">Politrópico</span>
            </div>
        </div>
        <div class="mod-card mod-3">
            <div class="mod-num">Módulo 3</div>
            <span class="mod-icon">💧</span>
            <div class="mod-title">Estática e Manometria</div>
            <div class="mod-desc">Pressão hidrostática, Princípio de Pascal e medição de pressão com colunas de fluido.</div>
            <div class="mod-chips">
                <span class="chip chip-3">P hidrostática</span>
                <span class="chip chip-3">Tubo em U</span>
                <span class="chip chip-3">Tubo inclinado</span>
                <span class="chip chip-3">P atmosférica</span>
            </div>
        </div>
        <div class="mod-card mod-4">
            <div class="mod-num">Módulo 4</div>
            <span class="mod-icon">⚙️</span>
            <div class="mod-title">Sistema Acoplado</div>
            <div class="mod-desc">Síntese: os três módulos anteriores agindo simultaneamente num cilindro com pistão real.</div>
            <div class="mod-chips">
                <span class="chip chip-4">Atuador hidráulico</span>
                <span class="chip chip-4">Processo isobárico</span>
                <span class="chip chip-4">Balanço energético</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Progressão dos conceitos</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="flow-wrap">
        <span class="flow-node fn1">Temperatura &amp; Calor</span>
        <span class="flow-arr">→</span>
        <span class="flow-node fn2">1ª Lei &amp; Trabalho</span>
        <span class="flow-arr">→</span>
        <span class="flow-node fn3">Pressão &amp; Fluidos</span>
        <span class="flow-arr">→</span>
        <span class="flow-node fn4">Sistema Integrado</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Como cada módulo funciona</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**📖 Teoria** — Conceitos numerados com fórmulas e exemplos resolvidos em cada módulo.")
    with c2:
        st.info("**🧮 Calculadora** — Sliders interativos que atualizam resultados e gráficos em tempo real.")
    with c3:
        st.info("**👁️ Visualização** — Diagramas P×V, manômetros e cilindros animados com os seus parâmetros.")


# ══════════════════════════════════════════════════════════════
# ABA 1 — CIÊNCIAS TÉRMICAS
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<span class="module-tag tag-thermo">Ciências Térmicas · Módulo 1 de 4</span>', unsafe_allow_html=True)
    prof("Antes de entrar em pressões e pistões, precisamos dominar três conceitos distintos: "
         "<strong>temperatura</strong> (agitação molecular), <strong>calor</strong> (energia em trânsito) "
         "e <strong>energia interna</strong> (energia armazenada). Eles parecem sinônimos, mas têm "
         "definições precisas — e confundi-los é o erro mais comum em termodinâmica.")

    col_th, col_calc = st.columns([1, 1], gap="large")

    with col_th:
        st.markdown('<div class="sec-label">Teoria</div>', unsafe_allow_html=True)

        concept(
            num=1, subtitulo="escala de temperatura",
            titulo="Temperatura e escalas de medição",
            formula_badge="T(K) = T(°C) + 273,15",
            corpo_bullets=[
                "Temperatura mede a <strong>energia cinética média</strong> das moléculas — quanto mais rápido vibram, maior a temperatura.",
                "Kelvin (K) é a escala absoluta, obrigatória em equações termodinâmicas. O zero absoluto (0 K) é o ponto onde toda agitação cessa.",
                "Celsius e Fahrenheit são escalas relativas — úteis no cotidiano, mas nunca use diretamente em cálculos de gás ideal.",
            ],
            formula_expr="T(K) = T(°C) + 273,15 &nbsp;|&nbsp; T(°F) = T(°C) × 9/5 + 32",
            formula_vars="Sempre converta para Kelvin antes de aplicar em PV = nRT ou ΔU = n·Cᵥ·ΔT",
            ex_enunciado="Converter 150 °C para Kelvin e Fahrenheit:",
            ex_resposta="K = 150 + 273,15 = 423,15 K &nbsp;|&nbsp; °F = 150 × 9/5 + 32 = 302 °F",
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

    with col_calc:
        st.markdown('<div class="sec-label">Calculadora interativa</div>', unsafe_allow_html=True)

        grupos = {}
        for nome, dados in SUBSTANCIAS_CALOR_ESPECIFICO.items():
            grupos.setdefault(dados["grupo"], []).append(nome)
        nomes_ordenados = []
        for g in ["Líquidos", "Gases", "Sólidos"]:
            for n in grupos.get(g, []):
                nomes_ordenados.append(n)

        sub_nome = st.selectbox(
            "Substância",
            nomes_ordenados,
            format_func=lambda n: f"{n}  —  {SUBSTANCIAS_CALOR_ESPECIFICO[n]['c']} J/kg·K",
        )
        c_val = SUBSTANCIAS_CALOR_ESPECIFICO[sub_nome]["c"]
        t_ini = st.slider("Temperatura inicial (°C)", -50, 300, 25)
        massa = st.slider("Massa (kg)", 0.1, 200.0, 2.0, step=0.1)
        delta_t_val = st.slider("Variação ΔT (K)", 1, 500, 50)

        temps = converter_temperatura(t_ini)
        calor = calcular_calor_sensivel(massa, c_val, delta_t_val)

        metric_row([
            ("Em Kelvin", f"{temps['kelvin']:.2f}", "K"),
            ("Em Fahrenheit", f"{temps['fahrenheit']:.1f}", "°F"),
        ])
        metric_row([
            ("Calor específico c", f"{c_val}", "J/kg·K"),
            ("Calor Q", f"{calor['Q_kJ']:.2f}", "kJ"),
        ])
        st.info(f"Para aquecer **{massa:.1f} kg** de **{sub_nome}** em **{delta_t_val} K** → **{calor['Q_kJ']:.2f} kJ**")

        dts = np.linspace(0, delta_t_val * 1.5 + 10, 80)
        qs = massa * c_val * dts / 1000
        fig_q = go.Figure()
        fig_q.add_trace(go.Scatter(
            x=dts, y=qs, mode="lines",
            line=dict(color="#3b82f6", width=3),
            fill="tozeroy", fillcolor="rgba(59,130,246,0.10)", name="Q (kJ)",
        ))
        fig_q.add_trace(go.Scatter(
            x=[delta_t_val], y=[calor["Q_kJ"]], mode="markers",
            marker=dict(color="#f59e0b", size=10), name="Ponto atual",
        ))
        fig_q.update_layout(
            template=PLOTLY_TEMPLATE, height=230,
            margin=dict(l=10, r=10, t=10, b=30),
            xaxis_title="ΔT (K)", yaxis_title="Q (kJ)", showlegend=False,
        )
        st.plotly_chart(fig_q, width="stretch")


# ══════════════════════════════════════════════════════════════
# ABA 2 — ENERGIA E TRABALHO
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<span class="module-tag tag-thermo">Conservação de Energia · Módulo 2 de 4</span>', unsafe_allow_html=True)
    prof("A 1ª Lei é simples: energia não some. Num sistema com pistão, o calor que entra vai para "
         "a energia interna do gás <em>e</em> para o trabalho mecânico. "
         "A área sob a curva P×V <strong>é</strong> o trabalho — não é uma aproximação, é exato.")

    col_th2, col_calc2 = st.columns([1, 1], gap="large")

    with col_th2:
        st.markdown('<div class="sec-label">Teoria</div>', unsafe_allow_html=True)

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
            ex_resposta="ΔU = Q − W = 50 − 20 = 30 kJ &nbsp;|&nbsp; ΔT = 30000/(10×20,8) = 144 K",
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

        st.markdown('<div class="sec-label" style="margin-top:.5rem">Processos termodinâmicos</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="proc-grid">
            <div class="proc-card proc-iso">
                <strong>Isotérmico (T = cte)</strong>
                W = nRT·ln(V₂/V₁)<br>Q = W &nbsp;|&nbsp; ΔU = 0
            </div>
            <div class="proc-card proc-isobar">
                <strong>Isobárico (P = cte)</strong>
                W = P·ΔV = nR·ΔT<br>Q = n·Cₚ·ΔT
            </div>
            <div class="proc-card proc-adiab">
                <strong>Adiabático (Q = 0)</strong>
                PVᵞ = cte<br>W = −ΔU = −n·Cᵥ·ΔT
            </div>
            <div class="proc-card proc-polit">
                <strong>Politrópico (PVⁿ = cte)</strong>
                W = (P₁V₁ − P₂V₂)/(n−1)<br>Q = ΔU + W
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_calc2:
        st.markdown('<div class="sec-label">Calculadora + diagrama P×V interativo</div>', unsafe_allow_html=True)

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
        cor = CORES_PROCESSO[processo]

        fig_pv = go.Figure()
        fig_pv.add_trace(go.Scatter(
            x=np.append(res2["v_array"], res2["v_array"][::-1]),
            y=np.append(res2["p_array"] / 1000, np.zeros(len(res2["p_array"]))),
            fill="toself", fillcolor=hex_rgba(cor, 0.12),
            line=dict(width=0), showlegend=False, hoverinfo="skip",
        ))
        fig_pv.add_trace(go.Scatter(
            x=res2["v_array"], y=res2["p_array"] / 1000,
            mode="lines", line=dict(color=cor, width=3), name=processo,
        ))
        fig_pv.add_trace(go.Scatter(
            x=[res2["V1"], res2["V2"]], y=[res2["P1_kPa"], res2["P2_kPa"]],
            mode="markers+text",
            marker=dict(color=cor, size=10, line=dict(color="white", width=1.5)),
            text=["V₁,P₁", "V₂,P₂"],
            textposition=["top right", "bottom left"],
            textfont=dict(size=11), showlegend=False,
        ))
        fig_pv.add_annotation(
            x=(res2["V1"] + res2["V2"]) / 2,
            y=(res2["P1_kPa"] + res2["P2_kPa"]) / 2,
            text=f"<b>W = {res2['W_kJ']:.1f} kJ</b><br>(área = trabalho)",
            showarrow=False, font=dict(size=11, color=cor),
            bgcolor="#020617", bordercolor=cor, borderwidth=1,
        )
        fig_pv.update_layout(
            template=PLOTLY_TEMPLATE, height=290,
            margin=dict(l=10, r=10, t=10, b=30),
            xaxis_title="Volume V (m³)", yaxis_title="Pressão P (kPa)",
            legend=dict(x=0.01, y=0.99),
        )
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


# ══════════════════════════════════════════════════════════════
# ABA 3 — ESTÁTICA E MANOMETRIA
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<span class="module-tag tag-fluid">Mecânica dos Fluidos · Módulo 3 de 4</span>', unsafe_allow_html=True)
    prof("Agora saímos das moléculas e olhamos para colunas inteiras de fluido. "
         "A pressão hidrostática aumenta <em>linearmente</em> com a profundidade, "
         "independente da forma do recipiente — isso é o Princípio de Pascal. "
         "O manômetro transforma essa pressão numa altura de coluna legível.")

    col_th3, col_calc3 = st.columns([1, 1], gap="large")

    with col_th3:
        st.markdown('<div class="sec-label">Teoria</div>', unsafe_allow_html=True)

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
            ex_resposta="P_hid = 13600×9,81×0,15 = 20012 Pa &nbsp;|&nbsp; P_abs = 121 337 Pa ≈ 121,3 kPa",
            aviso="Pressão absoluta = Pressão manométrica + P_atm. Não confundir as duas!",
        )

    with col_calc3:
        st.markdown('<div class="sec-label">Calculadora + visualização do manômetro</div>', unsafe_allow_html=True)

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

        fig_man = go.Figure()
        nivel_esq = 2.0 - h_man / 4
        nivel_dir = 2.0 + h_man / 4

        fig_man.add_trace(go.Scatter(
            x=[1.0, 1.0], y=[0.4, nivel_esq],
            mode="lines", line=dict(color=cor_fluido, width=26), name=fluido_nome,
        ))
        theta_base = np.linspace(np.pi, 2 * np.pi, 80)
        fig_man.add_trace(go.Scatter(
            x=1.5 + 0.5 * np.cos(theta_base), y=0.45 + 0.12 * np.sin(theta_base),
            mode="lines", line=dict(color=cor_fluido, width=26), showlegend=False,
        ))
        if tipo_man == "Tubo Inclinado":
            ang_r = np.radians(angulo_val)
            dx = h_man * np.cos(ang_r) * 1.5
            dy = h_man * np.sin(ang_r) * 1.5
            fig_man.add_trace(go.Scatter(
                x=[2.0, 2.0 + dx], y=[0.45, 0.45 + dy],
                mode="lines", line=dict(color=cor_fluido, width=26), showlegend=False,
            ))
            fig_man.add_trace(go.Scatter(
                x=[2.0, 2.0 + dx * 1.8], y=[0.4, 0.4 + dy * 1.8],
                mode="lines", line=dict(color="white", width=2), showlegend=False, opacity=0.25,
            ))
            fig_man.add_annotation(
                x=2.0 + dx * 0.6, y=0.35 + dy * 0.3,
                text=f"θ = {angulo_val:.0f}°", showarrow=False,
                font=dict(size=11, color="#f59e0b"),
            )
        else:
            fig_man.add_trace(go.Scatter(
                x=[2.0, 2.0], y=[0.45, nivel_dir],
                mode="lines", line=dict(color=cor_fluido, width=26), showlegend=False,
            ))

        for x_c in [1.0, 2.0]:
            fig_man.add_trace(go.Scatter(
                x=[x_c - 0.15, x_c - 0.15, x_c + 0.15, x_c + 0.15],
                y=[3.6, 0.4, 0.4, 3.6],
                mode="lines", line=dict(color="white", width=1.5),
                showlegend=False, opacity=0.3,
            ))

        fig_man.add_shape(type="line", x0=0.5, y0=nivel_esq, x1=2.5, y1=nivel_esq,
                          line=dict(color="#f59e0b", width=1, dash="dot"))
        if tipo_man == "Tubo em U Vertical":
            fig_man.add_shape(type="line", x0=0.5, y0=nivel_dir, x1=2.5, y1=nivel_dir,
                              line=dict(color="#f59e0b", width=1, dash="dot"))
            fig_man.add_annotation(x=2.6, y=(nivel_esq + nivel_dir) / 2,
                                   text=f"h = {h_man:.2f} m", showarrow=False,
                                   font=dict(size=11, color="#f59e0b"))
        fig_man.add_annotation(x=1.0, y=3.5, text="← P_abs",
                               showarrow=True, arrowhead=2, arrowcolor="#ef4444",
                               font=dict(color="#ef4444", size=11), ax=50, ay=0)
        fig_man.add_annotation(x=2.0, y=3.5, text="P_atm →",
                               showarrow=True, arrowhead=2, arrowcolor="#22c55e",
                               font=dict(color="#22c55e", size=11), ax=-50, ay=0)
        fig_man.update_layout(
            template=PLOTLY_TEMPLATE, height=370,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(range=[0.3, 3.0], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[0, 4.2], showgrid=False, zeroline=False, title="Escala vertical (m)"),
            showlegend=True, legend=dict(x=0.01, y=0.01),
        )
        st.plotly_chart(fig_man, width="stretch")


# ══════════════════════════════════════════════════════════════
# ABA 4 — SISTEMA ACOPLADO
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<span class="module-tag tag-coupled">Sistema Integrado · Módulo 4 de 4</span>', unsafe_allow_html=True)
    prof("Módulo de síntese! Um gás confinado recebe calor (Módulos 1 e 2) e precisa vencer "
         "a pressão de uma coluna de fluido (Módulo 3) para mover o pistão. "
         "Temperatura, pressão e volume interagem simultaneamente num processo <strong>isobárico</strong>.")

    col_th4, col_calc4 = st.columns([1, 1], gap="large")

    with col_th4:
        st.markdown('<div class="sec-label">Teoria</div>', unsafe_allow_html=True)

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
            formula_vars="A (m²) = área do pistão &nbsp;|&nbsp; n = 10 mol de N₂ na simulação",
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

    with col_calc4:
        st.markdown('<div class="sec-label">Simulador integrado</div>', unsafe_allow_html=True)

        fluido_ac = st.selectbox("Fluido sobre o pistão", list(FLUIDOS_MANOMETRIA.keys()), key="fl_ac")
        rho_ac = FLUIDOS_MANOMETRIA[fluido_ac]["rho"]
        cor_ac = FLUIDOS_MANOMETRIA[fluido_ac]["cor"]
        h_ac = st.slider("Altura da coluna de fluido h (m)", 0.1, 3.0, 0.5, 0.1, key="h_ac")
        q_ac = st.slider("Calor injetado Q (kJ)", 1, 50, 15, key="q_ac")
        area_ac = st.slider("Área do pistão A (m²)", 0.01, 0.20, 0.05, 0.01, key="area_ac")

        res4 = calcular_sistema_acoplado(rho_ac, h_ac, q_ac, area_ac)

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

        y_ini = res4["y_inicial"]
        y_fim = res4["y_final"]
        topo = y_fim + h_ac + 0.3
        calor_norm = min(q_ac / 50, 1.0)
        r_gas = int(50 + calor_norm * 200)
        g_gas = int(180 - calor_norm * 150)

        fig_cil = go.Figure()
        fig_cil.add_trace(go.Bar(
            x=["Cilindro"], y=[y_fim],
            marker_color=f"rgba({r_gas},{g_gas},255,0.45)",
            width=0.5, name=f"Gás (N₂) — {res4['T_final_C']:.0f} °C",
        ))
        fig_cil.add_trace(go.Bar(
            x=["Cilindro"], y=[h_ac], base=y_fim,
            marker_color=hex_rgba(cor_ac, 0.6),
            width=0.5, name=f"Fluido: {fluido_ac}",
        ))
        fig_cil.add_shape(type="rect",
            x0=-0.27, x1=0.27, y0=y_fim, y1=y_fim + 0.04,
            fillcolor="#94a3b8", line=dict(color="#e2e8f0", width=1))
        for xp in [-0.27, 0.27]:
            fig_cil.add_shape(type="line", x0=xp, x1=xp, y0=0, y1=topo,
                              line=dict(color="#475569", width=8))
        fig_cil.add_shape(type="line", x0=-0.27, x1=0.27, y0=0, y1=0,
                          line=dict(color="#475569", width=8))
        for i, xi in enumerate([-0.15, 0, 0.15]):
            fig_cil.add_annotation(
                x=xi, y=-0.2, text="▲",
                font=dict(size=14 + i * 2, color=f"rgba(251,191,36,{0.5+i*0.25})"),
                showarrow=False,
            )
        fig_cil.add_annotation(x=0, y=-0.45, text=f"Q = {q_ac} kJ",
                               font=dict(size=11, color="#f59e0b"), showarrow=False)
        fig_cil.add_shape(type="line", x0=0.32, x1=0.32, y0=y_ini, y1=y_fim,
                          line=dict(color="#f59e0b", width=1.5, dash="dot"))
        fig_cil.add_annotation(x=0.44, y=(y_ini + y_fim) / 2,
                               text=f"Δy={res4['deslocamento_cm']:.1f}cm",
                               showarrow=False, font=dict(size=10, color="#f59e0b"))
        fig_cil.update_layout(
            template=PLOTLY_TEMPLATE, barmode="stack", height=400,
            margin=dict(l=10, r=65, t=10, b=30),
            xaxis=dict(showticklabels=False, showgrid=False),
            yaxis=dict(title="Altura (m)", range=[-0.65, topo + 0.2],
                       showgrid=True, gridcolor="#1e293b"),
            legend=dict(x=0.01, y=0.99), showlegend=True,
        )
        st.plotly_chart(fig_cil, width="stretch")

        fig_bal = go.Figure(go.Bar(
            x=["Calor Q", "Trabalho W", "Energia interna ΔU"],
            y=[res4["Q_kJ"], res4["W_kJ"], res4["delta_U_kJ"]],
            marker_color=["#3b82f6", "#22c55e", "#f59e0b"],
            text=[f"{v:.2f} kJ" for v in [res4["Q_kJ"], res4["W_kJ"], res4["delta_U_kJ"]]],
            textposition="auto",
        ))
        fig_bal.update_layout(
            template=PLOTLY_TEMPLATE, height=190,
            margin=dict(l=10, r=10, t=25, b=10),
            title=dict(text="Balanço energético — 1ª Lei", font=dict(size=13)),
            yaxis_title="kJ",
        )
        st.plotly_chart(fig_bal, width="stretch")