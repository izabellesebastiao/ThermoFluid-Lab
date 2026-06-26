import streamlit as st


def prof(texto: str) -> None:
    st.markdown(f"""
    <div class="chat chat-start mb-5">
        <div class="chat-image avatar">
            <div class="w-10 text-2xl flex items-center justify-center">🧑‍🏫</div>
        </div>
        <div class="chat-header text-xs font-bold text-primary uppercase tracking-wide mb-0.5">Prof. Thermo</div>
        <div class="chat-bubble chat-bubble-info text-sm leading-relaxed">{texto}</div>
    </div>""", unsafe_allow_html=True)

