import html as _html

import streamlit as st


def concept(num: int, subtitulo: str, titulo: str, formula_badge: str,
            corpo_bullets: list[str], formula_expr: str, formula_vars: str,
            ex_enunciado: str, ex_resposta: str, aviso: str = "") -> None:
    """
    Renderiza um bloco de teoria mesclando Opção A e B.
    Dividido em dois st.markdown para evitar o bug do Streamlit que escapa
    conteúdo de texto dentro de tags HTML aninhadas em f-strings longas.
    """
    bullets_html = "".join(
        f'<li class="text-sm opacity-80 leading-relaxed">{b}</li>'
        for b in corpo_bullets
    )
    aviso_html = (
        f'<div class="alert alert-warning text-sm py-2 mb-3">⚠️ {aviso}</div>'
        if aviso else ""
    )

    # Parte 1: cabeçalho + bullets + fórmula (sem conteúdo de texto livre problemático)
    # Renderizado em uma única linha sem indentação: blocos HTML indentados ou
    # com linhas em branco são interpretados pelo parser de markdown do Streamlit
    # como blocos de código, fazendo tags de fechamento aparecerem como texto literal.
    st.markdown(
        f'<div class="card bg-base-200 border border-base-300 mb-4">'
        f'<div class="card-body p-0">'
        f'<div class="bg-base-300 px-4 py-3 flex items-center gap-2.5 rounded-t-2xl">'
        f'<div class="badge badge-info badge-outline w-7 h-7 font-bold">{num}</div>'
        f'<div class="flex-1">'
        f'<div class="text-xs opacity-50 uppercase tracking-wide">{subtitulo}</div>'
        f'<div class="font-semibold text-info leading-tight">{titulo}</div>'
        f'</div>'
        f'<span class="badge badge-info badge-outline font-mono whitespace-nowrap">{formula_badge}</span>'
        f'</div>'
        f'<div class="px-4 py-3.5">'
        f'<ul class="list-none space-y-1.5 mb-2">{bullets_html}</ul>'
        f'<div class="border-l-4 border-primary bg-base-300 px-3.5 py-2.5 rounded-r-md font-mono text-sm my-2">{formula_expr}</div>'
        f'<div class="text-xs opacity-50 mb-2.5">{formula_vars}</div>'
        f'{aviso_html}'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Parte 2: exemplo resolvido — st.markdown separado evita escape do conteúdo
    eq = _html.escape(ex_enunciado)
    er = _html.escape(ex_resposta)
    st.markdown(
        f'<div class="mockup-code text-xs -mt-2.5 mb-4">'
        f'<pre data-prefix=">"><code class="opacity-60">{eq}</code></pre>'
        f'<pre data-prefix="$"><code class="text-success">{er}</code></pre>'
        f'</div>',
        unsafe_allow_html=True,
    )


def warn(texto: str) -> None:
    st.markdown(f'<div class="alert alert-warning text-sm py-2 mb-3">⚠️ {texto}</div>', unsafe_allow_html=True)


def metric_row(items: list[tuple]) -> None:
    cols = st.columns(len(items))
    for col, (label, valor, unidade) in zip(cols, items):
        col.metric(label, f"{valor} {unidade}")
