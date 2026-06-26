import streamlit as st


def prof(texto: str) -> None:
    st.markdown(
        f'<div class="chat chat-start mb-5">'
        f'<div class="chat-image avatar">'
        f'<div class="w-10 text-2xl flex items-center justify-center">🧑‍🏫</div>'
        f'</div>'
        f'<div class="chat-header text-xs font-bold text-primary uppercase tracking-wide mb-0.5">Prof. Thermo</div>'
        f'<div class="chat-bubble chat-bubble-info text-sm leading-relaxed">{texto}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

