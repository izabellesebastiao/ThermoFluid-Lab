import numpy as np
import plotly.graph_objects as go

from components.layout import CUPCAKE, CORES_PROCESSO, PLOTLY_TEMPLATE, PLOTLY_THEME_LAYOUT, hex_rgba

_GREY = "#9aa0a6"  # cinza metálico — cupcake não define um tom de cinza próprio


def build_calor_chart(massa: float, c_val: float, delta_t_val: float, q_kj: float) -> go.Figure:
    dts = np.linspace(0, delta_t_val * 1.5 + 10, 80)
    qs = massa * c_val * dts / 1000
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dts, y=qs, mode="lines",
        line=dict(color=CUPCAKE["primary"], width=3),
        fill="tozeroy", fillcolor=hex_rgba(CUPCAKE["primary"], 0.15), name="Q (kJ)",
    ))
    fig.add_trace(go.Scatter(
        x=[delta_t_val], y=[q_kj], mode="markers",
        marker=dict(color=CUPCAKE["accent"], size=10), name="Ponto atual",
    ))
    fig.update_layout(
        **PLOTLY_THEME_LAYOUT, template=PLOTLY_TEMPLATE, height=230,
        margin=dict(l=10, r=10, t=10, b=30),
        xaxis_title="ΔT (K)", yaxis_title="Q (kJ)", showlegend=False,
    )
    return fig


def build_pv_chart(res: dict, processo: str) -> go.Figure:
    cor = CORES_PROCESSO[processo]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=np.append(res["v_array"], res["v_array"][::-1]),
        y=np.append(res["p_array"] / 1000, np.zeros(len(res["p_array"]))),
        fill="toself", fillcolor=hex_rgba(cor, 0.15),
        line=dict(width=0), showlegend=False, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=res["v_array"], y=res["p_array"] / 1000,
        mode="lines", line=dict(color=cor, width=3), name=processo,
    ))
    fig.add_trace(go.Scatter(
        x=[res["V1"], res["V2"]], y=[res["P1_kPa"], res["P2_kPa"]],
        mode="markers+text",
        marker=dict(color=cor, size=10, line=dict(color=CUPCAKE["neutral"], width=1.5)),
        text=["V₁,P₁", "V₂,P₂"],
        textposition=["top right", "bottom left"],
        textfont=dict(size=11), showlegend=False,
    ))
    fig.add_annotation(
        x=(res["V1"] + res["V2"]) / 2,
        y=(res["P1_kPa"] + res["P2_kPa"]) / 2,
        text=f"<b>W = {res['W_kJ']:.1f} kJ</b><br>(área = trabalho)",
        showarrow=False, font=dict(size=11, color=cor),
        bgcolor=CUPCAKE["base100"], bordercolor=cor, borderwidth=1,
    )
    fig.update_layout(
        **PLOTLY_THEME_LAYOUT, template=PLOTLY_TEMPLATE, height=290,
        margin=dict(l=10, r=10, t=10, b=30),
        xaxis_title="Volume V (m³)", yaxis_title="Pressão P (kPa)",
        legend=dict(x=0.01, y=0.99),
    )
    return fig


def build_manometro_chart(h_man: float, tipo_man: str, angulo_val: float,
                           cor_fluido: str, fluido_nome: str) -> go.Figure:
    fig = go.Figure()
    nivel_esq = 2.0 - h_man / 4
    nivel_dir = 2.0 + h_man / 4

    fig.add_trace(go.Scatter(
        x=[1.0, 1.0], y=[0.4, nivel_esq],
        mode="lines", line=dict(color=cor_fluido, width=26), name=fluido_nome,
    ))
    theta_base = np.linspace(np.pi, 2 * np.pi, 80)
    fig.add_trace(go.Scatter(
        x=1.5 + 0.5 * np.cos(theta_base), y=0.45 + 0.12 * np.sin(theta_base),
        mode="lines", line=dict(color=cor_fluido, width=26), showlegend=False,
    ))
    if tipo_man == "Tubo Inclinado":
        ang_r = np.radians(angulo_val)
        dx = h_man * np.cos(ang_r) * 1.5
        dy = h_man * np.sin(ang_r) * 1.5
        fig.add_trace(go.Scatter(
            x=[2.0, 2.0 + dx], y=[0.45, 0.45 + dy],
            mode="lines", line=dict(color=cor_fluido, width=26), showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=[2.0, 2.0 + dx * 1.8], y=[0.4, 0.4 + dy * 1.8],
            mode="lines", line=dict(color="#ffffff", width=2), showlegend=False, opacity=0.35,
        ))
        fig.add_annotation(
            x=2.0 + dx * 0.6, y=0.35 + dy * 0.3,
            text=f"θ = {angulo_val:.0f}°", showarrow=False,
            font=dict(size=11, color=CUPCAKE["accent"]),
        )
    else:
        fig.add_trace(go.Scatter(
            x=[2.0, 2.0], y=[0.45, nivel_dir],
            mode="lines", line=dict(color=cor_fluido, width=26), showlegend=False,
        ))

    for x_c in [1.0, 2.0]:
        fig.add_trace(go.Scatter(
            x=[x_c - 0.15, x_c - 0.15, x_c + 0.15, x_c + 0.15],
            y=[3.6, 0.4, 0.4, 3.6],
            mode="lines", line=dict(color=CUPCAKE["neutral"], width=1.5),
            showlegend=False, opacity=0.3,
        ))

    fig.add_shape(type="line", x0=0.5, y0=nivel_esq, x1=2.5, y1=nivel_esq,
                  line=dict(color=CUPCAKE["accent"], width=1, dash="dot"))
    if tipo_man == "Tubo em U Vertical":
        fig.add_shape(type="line", x0=0.5, y0=nivel_dir, x1=2.5, y1=nivel_dir,
                      line=dict(color=CUPCAKE["accent"], width=1, dash="dot"))
        fig.add_annotation(x=2.6, y=(nivel_esq + nivel_dir) / 2,
                           text=f"h = {h_man:.2f} m", showarrow=False,
                           font=dict(size=11, color=CUPCAKE["accent"]))
    fig.add_annotation(x=1.0, y=3.5, text="← P_abs",
                       showarrow=True, arrowhead=2, arrowcolor=CUPCAKE["error"],
                       font=dict(color=CUPCAKE["error"], size=11), ax=50, ay=0)
    fig.add_annotation(x=2.0, y=3.5, text="P_atm →",
                       showarrow=True, arrowhead=2, arrowcolor=CUPCAKE["success"],
                       font=dict(color=CUPCAKE["success"], size=11), ax=-50, ay=0)
    fig.update_layout(
        **PLOTLY_THEME_LAYOUT, template=PLOTLY_TEMPLATE, height=370,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(range=[0.3, 3.0], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, 4.2], showgrid=False, zeroline=False, title="Escala vertical (m)"),
        showlegend=True, legend=dict(x=0.01, y=0.01),
    )
    return fig


def _blend_gas_color(calor_norm: float) -> str:
    """Interpola a cor do gás de frio (info) a quente (error) conforme o calor injetado."""
    frio = (28, 146, 242)    # info
    quente = (255, 87, 36)   # error
    r = int(frio[0] + calor_norm * (quente[0] - frio[0]))
    g = int(frio[1] + calor_norm * (quente[1] - frio[1]))
    b = int(frio[2] + calor_norm * (quente[2] - frio[2]))
    return f"rgba({r},{g},{b},0.45)"


def build_cilindro_chart(res: dict, h_ac: float, q_ac: float,
                          cor_ac: str, fluido_ac: str) -> go.Figure:
    y_ini = res["y_inicial"]
    y_fim = res["y_final"]
    topo = y_fim + h_ac + 0.3
    calor_norm = min(q_ac / 50, 1.0)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Cilindro"], y=[y_fim],
        marker_color=_blend_gas_color(calor_norm),
        width=0.5, name=f"Gás — {res['T_final_C']:.0f} °C",
    ))
    fig.add_trace(go.Bar(
        x=["Cilindro"], y=[h_ac], base=y_fim,
        marker_color=hex_rgba(cor_ac, 0.6),
        width=0.5, name=f"Fluido: {fluido_ac}",
    ))
    fig.add_shape(type="rect",
        x0=-0.27, x1=0.27, y0=y_fim, y1=y_fim + 0.04,
        fillcolor=_GREY, line=dict(color=CUPCAKE["neutral"], width=1))
    for xp in [-0.27, 0.27]:
        fig.add_shape(type="line", x0=xp, x1=xp, y0=0, y1=topo,
                      line=dict(color=hex_rgba(CUPCAKE["neutral"], 0.55), width=8))
    fig.add_shape(type="line", x0=-0.27, x1=0.27, y0=0, y1=0,
                  line=dict(color=hex_rgba(CUPCAKE["neutral"], 0.55), width=8))
    for i, xi in enumerate([-0.15, 0, 0.15]):
        fig.add_annotation(
            x=xi, y=-0.2, text="▲",
            font=dict(size=14 + i * 2, color=hex_rgba(CUPCAKE["accent"], 0.5 + i * 0.25)),
            showarrow=False,
        )
    fig.add_annotation(x=0, y=-0.45, text=f"Q = {q_ac} kJ",
                       font=dict(size=11, color=CUPCAKE["accent"]), showarrow=False)
    fig.add_shape(type="line", x0=0.32, x1=0.32, y0=y_ini, y1=y_fim,
                  line=dict(color=CUPCAKE["accent"], width=1.5, dash="dot"))
    fig.add_annotation(x=0.44, y=(y_ini + y_fim) / 2,
                       text=f"Δy={res['deslocamento_cm']:.1f}cm",
                       showarrow=False, font=dict(size=10, color=CUPCAKE["accent"]))
    fig.update_layout(
        **PLOTLY_THEME_LAYOUT, template=PLOTLY_TEMPLATE, barmode="stack", height=400,
        margin=dict(l=10, r=65, t=10, b=30),
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(title="Altura (m)", range=[-0.65, topo + 0.2],
                   showgrid=True, gridcolor=CUPCAKE["base300"]),
        legend=dict(x=0.01, y=0.99), showlegend=True,
    )
    return fig


def build_balanco_chart(res: dict) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=["Calor Q", "Trabalho W", "Energia interna ΔU"],
        y=[res["Q_kJ"], res["W_kJ"], res["delta_U_kJ"]],
        marker_color=[CUPCAKE["primary"], CUPCAKE["success"], CUPCAKE["accent"]],
        text=[f"{v:.2f} kJ" for v in [res["Q_kJ"], res["W_kJ"], res["delta_U_kJ"]]],
        textposition="auto",
    ))
    fig.update_layout(
        **PLOTLY_THEME_LAYOUT, template=PLOTLY_TEMPLATE, height=190,
        margin=dict(l=10, r=10, t=25, b=10),
        title=dict(text="Balanço energético — 1ª Lei", font=dict(size=13)),
        yaxis_title="kJ",
    )
    return fig
