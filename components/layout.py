import streamlit as st
import streamlit.components.v1 as components

# DaisyUI "cupcake" theme palette — https://daisyui.com/docs/themes/
CUPCAKE = {
    "primary":   "#65c3c8",
    "secondary": "#ef9fbc",
    "accent":    "#eeaf3a",
    "neutral":   "#291334",
    "base100":   "#faf7f5",
    "base200":   "#efeae6",
    "base300":   "#e7e2df",
    "info":      "#1c92f2",
    "success":   "#009485",
    "warning":   "#ff9900",
    "error":     "#ff5724",
}

CORES_PROCESSO = {
    "Isotérmico":  CUPCAKE["primary"],
    "Isobárico":   CUPCAKE["success"],
    "Adiabático":  CUPCAKE["error"],
    "Politrópico": CUPCAKE["secondary"],
}
PLOTLY_TEMPLATE = "plotly_white"

# Sobrepõe o template plotly_white padrão com o fundo/texto do tema cupcake.
PLOTLY_THEME_LAYOUT = dict(
    paper_bgcolor=CUPCAKE["base100"],
    plot_bgcolor=CUPCAKE["base100"],
    font=dict(color=CUPCAKE["neutral"]),
)


def inject_tailwind() -> None:
    """
    st.markdown() strips <script> tags (Streamlit never executes scripts inserted
    via unsafe_allow_html), so neither the Tailwind nor DaisyUI CDN assets can be
    loaded that way. Instead this renders a 0-height components.v1.html iframe
    whose JS reaches into window.parent.document (same-origin) to append the real
    <script>/<link> tags there, which does execute/load and applies the styling
    to the whole app, not just the iframe.

    DaisyUI ships as a plain stylesheet with no JS config step, so unlike a
    custom tailwind.config (which silently failed to apply through this same
    injection path — Tailwind's CDN only reads config during its own internal
    init and ignores later/external changes), its <link rel="stylesheet"> works
    immediately: browsers don't have the equivalent restriction for <link> tags
    that they have for inert innerHTML-inserted <script> tags.
    """
    components.html("""
        <script>
        (function() {
            var doc = window.parent.document;
            if (doc.getElementById('tw-cdn-script')) return;

            doc.documentElement.setAttribute('data-theme', 'cupcake');

            var tw = doc.createElement('script');
            tw.id = 'tw-cdn-script';
            tw.src = 'https://cdn.tailwindcss.com';
            doc.head.appendChild(tw);

            var daisy = doc.createElement('link');
            daisy.id = 'daisyui-cdn-link';
            daisy.rel = 'stylesheet';
            daisy.type = 'text/css';
            daisy.href = 'https://cdn.jsdelivr.net/npm/daisyui@4/dist/full.min.css';
            doc.head.appendChild(daisy);
        })();
        </script>
    """, height=0)


def hex_rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"
