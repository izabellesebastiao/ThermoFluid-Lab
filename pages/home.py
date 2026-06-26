from pathlib import Path
import streamlit as st

_IMG_PROF = Path(__file__).resolve().parent.parent / "assets" / "images" / "prof_introd.png"

st.markdown("""
<div class="text-center px-4 pt-10 pb-8 border-b border-base-300 mb-8">
    <div class="text-xs font-semibold uppercase tracking-widest opacity-50 mb-3">Engenharia · Fenômenos de Transporte</div>
    <h1 class="text-5xl font-bold mb-3">Thermo<span class="text-primary">Fluid</span> Lab</h1>
    <p class="text-base opacity-70 leading-relaxed max-w-[520px] mx-auto mb-6">
        Um simulador interativo para explorar os fundamentos de ciências térmicas
        e mecânica dos fluidos, com teoria, fórmulas e cálculos.
    </p>
</div>
""", unsafe_allow_html=True)

col_prof1, col_text1 = st.columns([1, 4])
with col_prof1:
    st.image(str(_IMG_PROF), width="stretch")
with col_text1:
    st.markdown("""
    <div class="chat chat-start">
        <div class="chat-bubble">
            <p class="font-semibold">Olá! Eu sou o Professor Thermo. Seja bem-vindo ao nosso laboratório de Fenômenos de Transporte!</p>
            <p>Vou acompanhar você nessa jornada de aprendizado, explorando
            como calor, energia e fluidos se comportam através dos princípios
            dos Fenômenos de Transporte.</p>
            <p>Minha missão é ajudar você a enxergar a física por trás das equações.
            Cada fórmula representa um fenômeno que acontece no mundo real.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-2">Explore os três pilares dos Fenômenos de Transporte:</div>', unsafe_allow_html=True)

st.markdown("""
<div class="grid grid-cols-4 gap-3 mb-7">
    <a href="termica" target="_self" class="text-inherit" style="text-decoration:none;">
    <div class="card bg-base-200 border-t-4 border-error shadow-sm hover:shadow-lg hover:-translate-y-1 transition">
        <div class="card-body p-4">
            <div class="text-xs font-semibold uppercase tracking-widest opacity-50">Módulo 1</div>
            <span class="text-2xl">🔥</span>
            <h3 class="card-title text-base">Ciências Térmicas</h3>
            <p class="text-sm opacity-70">Conceitos fundamentais de temperatura, calor e energia interna.</p>
            <div class="card-actions flex-wrap gap-1 mt-1">
                <span class="badge badge-error badge-outline badge-sm">Temperatura</span>
                <span class="badge badge-error badge-outline badge-sm">Calor sensível</span>
                <span class="badge badge-error badge-outline badge-sm">Energia interna</span>
                <span class="badge badge-error badge-outline badge-sm">Escalas K · °C · °F</span>
            </div>
        </div>
    </div>
    </a>
    <a href="energia" target="_self" class="text-inherit" style="text-decoration:none;">
    <div class="card bg-base-200 border-t-4 border-primary shadow-sm hover:shadow-lg hover:-translate-y-1 transition">
        <div class="card-body p-4">
            <div class="text-xs font-semibold uppercase tracking-widest opacity-50">Módulo 2</div>
            <span class="text-2xl">⚡</span>
            <h3 class="card-title text-base">Energia e Trabalho</h3>
            <p class="text-sm opacity-70">A 1ª Lei em ação: como calor vira trabalho mecânico em quatro processos distintos.</p>
            <div class="card-actions flex-wrap gap-1 mt-1">
                <span class="badge badge-primary badge-outline badge-sm">1ª Lei</span>
                <span class="badge badge-primary badge-outline badge-sm">Diagrama P×V</span>
                <span class="badge badge-primary badge-outline badge-sm">Isotérmico</span>
                <span class="badge badge-primary badge-outline badge-sm">Adiabático</span>
                <span class="badge badge-primary badge-outline badge-sm">Politrópico</span>
            </div>
        </div>
    </div>
    </a>
    <a href="fluidos" target="_self" class="text-inherit" style="text-decoration:none;">
    <div class="card bg-base-200 border-t-4 border-success shadow-sm hover:shadow-lg hover:-translate-y-1 transition">
        <div class="card-body p-4">
            <div class="text-xs font-semibold uppercase tracking-widest opacity-50">Módulo 3</div>
            <span class="text-2xl">💧</span>
            <h3 class="card-title text-base">Estática e Manometria</h3>
            <p class="text-sm opacity-70">Pressão hidrostática, Princípio de Pascal e medição de pressão com colunas de fluido.</p>
            <div class="card-actions flex-wrap gap-1 mt-1">
                <span class="badge badge-success badge-outline badge-sm">P hidrostática</span>
                <span class="badge badge-success badge-outline badge-sm">Tubo em U</span>
                <span class="badge badge-success badge-outline badge-sm">Tubo inclinado</span>
                <span class="badge badge-success badge-outline badge-sm">P atmosférica</span>
            </div>
        </div>
    </div>
    </a>
    <a href="sistema" target="_self" class="text-inherit" style="text-decoration:none;">
    <div class="card bg-base-200 border-t-4 border-secondary shadow-sm hover:shadow-lg hover:-translate-y-1 transition">
        <div class="card-body p-4">
            <div class="text-xs font-semibold uppercase tracking-widest opacity-50">Módulo 4</div>
            <span class="text-2xl">⚙️</span>
            <h3 class="card-title text-base">Sistema Acoplado</h3>
            <p class="text-sm opacity-70">Síntese: os três módulos anteriores agindo simultaneamente num cilindro com pistão real.</p>
            <div class="card-actions flex-wrap gap-1 mt-1">
                <span class="badge badge-secondary badge-outline badge-sm">Atuador hidráulico</span>
                <span class="badge badge-secondary badge-outline badge-sm">Processo isobárico</span>
                <span class="badge badge-secondary badge-outline badge-sm">Balanço energético</span>
            </div>
        </div>
    </div>
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-2">Progressão dos conceitos</div>', unsafe_allow_html=True)
st.markdown("""
<div class="flex items-center justify-center gap-2 flex-wrap mb-8">
    <span class="badge badge-error badge-lg">Temperatura &amp; Calor</span>
    <span class="opacity-40">→</span>
    <span class="badge badge-primary badge-lg">1ª Lei &amp; Trabalho</span>
    <span class="opacity-40">→</span>
    <span class="badge badge-success badge-lg">Pressão &amp; Fluidos</span>
    <span class="opacity-40">→</span>
    <span class="badge badge-secondary badge-lg">Sistema Integrado</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="text-xs font-bold uppercase tracking-widest opacity-50 mb-2">Como cada módulo funciona</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.info("**📖 Teoria** — Conceitos numerados com fórmulas e exemplos resolvidos em cada módulo.")
with c2:
    st.info("**🧮 Calculadora** — Sliders interativos que atualizam resultados e gráficos em tempo real.")
with c3:
    st.info("**👁️ Visualização** — Diagramas P×V, manômetros e cilindros animados com os seus parâmetros.")
