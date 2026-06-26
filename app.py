import streamlit as st

from components.layout import inject_tailwind

st.set_page_config(
    page_title="ThermoFluid Lab",
    page_icon="🌡️",
    layout="wide",
)
inject_tailwind()

pagina = st.navigation([
    st.Page("pages/home.py", title="Início", icon="🏠", default=True),
    st.Page("pages/termica.py", title="Ciências Térmicas", icon="🔥"),
    st.Page("pages/energia.py", title="Energia e Trabalho", icon="⚡"),
    st.Page("pages/fluidos.py", title="Estática e Manometria", icon="💧"),
    st.Page("pages/sistema.py", title="Sistema Acoplado", icon="⚙️"),
], position="top")
pagina.run()
