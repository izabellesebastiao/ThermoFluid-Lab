import numpy as np

# ==============================================================
# BANCO DE DADOS DE SUBSTÂNCIAS
# ==============================================================

SUBSTANCIAS_CALOR_ESPECIFICO = {
    "Água líquida":        {"c": 4186,  "unidade": "J/kg·K", "grupo": "Líquidos"},
    "Água (gelo)":         {"c": 2090,  "unidade": "J/kg·K", "grupo": "Sólidos"},
    "Vapor d'água":        {"c": 2010,  "unidade": "J/kg·K", "grupo": "Gases"},
    "Etanol":              {"c": 2440,  "unidade": "J/kg·K", "grupo": "Líquidos"},
    "Óleo mineral":        {"c": 1670,  "unidade": "J/kg·K", "grupo": "Líquidos"},
    "Mercúrio líquido":    {"c": 140,   "unidade": "J/kg·K", "grupo": "Líquidos"},
    "Alumínio":            {"c": 900,   "unidade": "J/kg·K", "grupo": "Sólidos"},
    "Cobre":               {"c": 385,   "unidade": "J/kg·K", "grupo": "Sólidos"},
    "Aço carbono":         {"c": 500,   "unidade": "J/kg·K", "grupo": "Sólidos"},
    "Ferro fundido":       {"c": 460,   "unidade": "J/kg·K", "grupo": "Sólidos"},
    "Ouro":                {"c": 128,   "unidade": "J/kg·K", "grupo": "Sólidos"},
    "Vidro":               {"c": 840,   "unidade": "J/kg·K", "grupo": "Sólidos"},
    "Concreto":            {"c": 700,   "unidade": "J/kg·K", "grupo": "Sólidos"},
    "Madeira (pinho)":     {"c": 1700,  "unidade": "J/kg·K", "grupo": "Sólidos"},
    "Ar (Cp)":             {"c": 1005,  "unidade": "J/kg·K", "grupo": "Gases"},
    "Nitrogênio N₂ (Cp)":  {"c": 1040,  "unidade": "J/kg·K", "grupo": "Gases"},
    "Argônio Ar (Cp)":     {"c": 520,   "unidade": "J/kg·K", "grupo": "Gases"},
    "CO₂ (Cp)":            {"c": 846,   "unidade": "J/kg·K", "grupo": "Gases"},
    "Hidrogênio H₂ (Cp)":  {"c": 14300, "unidade": "J/kg·K", "grupo": "Gases"},
}

FLUIDOS_MANOMETRIA = {
    "Água":          {"rho": 1000,  "cor": "#378ADD"},
    "Água do mar":   {"rho": 1030,  "cor": "#2E6FA8"},
    "Etanol":        {"rho": 789,   "cor": "#A78BFA"},
    "Óleo mineral":  {"rho": 850,   "cor": "#D97706"},
    "Óleo de motor": {"rho": 870,   "cor": "#92400E"},
    "Mercúrio":      {"rho": 13600, "cor": "#9CA3AF"},
    "Glicerina":     {"rho": 1261,  "cor": "#34D399"},
    "Gasolina":      {"rho": 720,   "cor": "#FCD34D"},
    "Fluido da Prova": {"rho": 3500, "cor": "#F472B6"},
}

GASES_TERMICOS = {
    "Nitrogênio (N₂)": {"gamma": 1.4,  "M": 28.0},
    "Argônio (Ar)":    {"gamma": 1.67, "M": 39.9},
    "Ar Atmosférico":  {"gamma": 1.4,  "M": 29.0},
    "CO₂":             {"gamma": 1.3,  "M": 44.0},
    "Hidrogênio (H₂)": {"gamma": 1.41, "M": 2.0},
}


# ==============================================================
# ABA 1 — CIÊNCIAS TÉRMICAS
# ==============================================================

def converter_temperatura(t_celsius: float) -> dict:
    """Converte temperatura de Celsius para Kelvin e Fahrenheit."""
    return {
        "kelvin": t_celsius + 273.15,
        "fahrenheit": t_celsius * 9 / 5 + 32,
        "celsius": t_celsius,
    }


def calcular_calor_sensivel(massa: float, c: float, delta_t: float) -> dict:
    """
    Calcula o calor sensível Q = m · c · ΔT.

    Parâmetros
    ----------
    massa   : massa da substância (kg)
    c       : calor específico (J/kg·K)
    delta_t : variação de temperatura (K)

    Retorna
    -------
    dict com Q em Joules e kJ, além dos dados de entrada.
    """
    Q_J = massa * c * delta_t
    return {
        "Q_J": Q_J,
        "Q_kJ": Q_J / 1000,
        "massa": massa,
        "c": c,
        "delta_t": delta_t,
    }


# ==============================================================
# ABA 2 — CONSERVAÇÃO DE ENERGIA E TRABALHO
# ==============================================================

def calcular_processo_termodinamico(
    tipo_processo: str,
    gas: str,
    v_inicial: float,
    razao_volume: float,
    n_politropico: float = 1.3,
) -> dict:
    """
    Calcula curva P×V e variáveis da 1ª Lei para processos com gás ideal.

    Parâmetros
    ----------
    tipo_processo : "Isotérmico", "Isobárico", "Adiabático" ou "Politrópico"
    gas           : chave em GASES_TERMICOS
    v_inicial     : volume inicial V₁ (m³)
    razao_volume  : V₂/V₁
    n_politropico : expoente para processo politrópico

    Retorna
    -------
    dict com arrays V e P para o gráfico, e W, Q, ΔU, T_final, P₁, P₂.
    """
    R = 8.314
    n_moles = 10.0
    T_inicial = 300.0  # K (27 °C)

    props = GASES_TERMICOS.get(gas, GASES_TERMICOS["Nitrogênio (N₂)"])
    gamma = props["gamma"]
    Cv = R / (gamma - 1)
    Cp = Cv + R

    v_final = v_inicial * razao_volume
    p_inicial = (n_moles * R * T_inicial) / v_inicial
    v_array = np.linspace(v_inicial, v_final, 120)

    if tipo_processo == "Isotérmico":
        p_array = (p_inicial * v_inicial) / v_array
        p_final = p_array[-1]
        T_final = T_inicial
        W = n_moles * R * T_inicial * np.log(v_final / v_inicial)
        delta_U = 0.0
        Q = W

    elif tipo_processo == "Isobárico":
        p_array = np.full_like(v_array, p_inicial)
        p_final = p_inicial
        T_final = T_inicial * (v_final / v_inicial)
        W = p_inicial * (v_final - v_inicial)
        delta_U = n_moles * Cv * (T_final - T_inicial)
        Q = delta_U + W

    elif tipo_processo == "Adiabático":
        p_array = p_inicial * (v_inicial / v_array) ** gamma
        p_final = p_array[-1]
        T_final = T_inicial * (v_inicial / v_final) ** (gamma - 1)
        delta_U = n_moles * Cv * (T_final - T_inicial)
        W = -delta_U
        Q = 0.0

    else:  # Politrópico
        n = n_politropico
        p_array = p_inicial * (v_inicial / v_array) ** n
        p_final = p_array[-1]
        T_final = T_inicial * (v_inicial / v_final) ** (n - 1)
        W = (p_inicial * v_inicial - p_final * v_final) / (n - 1)
        delta_U = n_moles * Cv * (T_final - T_inicial)
        Q = delta_U + W

    return {
        "v_array": v_array,
        "p_array": p_array,
        "W_kJ": W / 1000,
        "Q_kJ": Q / 1000,
        "delta_U_kJ": delta_U / 1000,
        "T_final_C": T_final - 273.15,
        "P1_kPa": p_inicial / 1000,
        "P2_kPa": p_final / 1000,
        "V1": v_inicial,
        "V2": v_final,
        "gamma": gamma,
    }


# ==============================================================
# ABA 3 — ESTÁTICA E MANOMETRIA
# ==============================================================

def calcular_p_atm(altitude: float) -> float:
    """
    Pressão atmosférica local pela equação barométrica simplificada (Pa).

    Parâmetros
    ----------
    altitude : altitude acima do nível do mar (m)
    """
    p_mar = 101325.0
    rho_ar = 1.2
    g = 9.81
    return max(p_mar - rho_ar * g * altitude, 0.0)


def calcular_pressao_reservatorio(
    p_atm: float,
    rho_fluido: float,
    h_coluna: float,
    tipo_manometro: str,
    angulo_graus: float = 30.0,
) -> dict:
    """
    Pressão absoluta no reservatório conectado ao manômetro.

    Parâmetros
    ----------
    p_atm          : pressão atmosférica local (Pa)
    rho_fluido     : massa específica do fluido (kg/m³)
    h_coluna       : deflexão / altura lida no manômetro (m)
    tipo_manometro : "Tubo em U Vertical" ou "Tubo Inclinado"
    angulo_graus   : ângulo de inclinação (°), usado apenas no tubo inclinado

    Retorna
    -------
    dict com P_atm, P_hidrostatica, P_absoluta (todas em Pa e kPa)
    e h_efetivo usado no cálculo.
    """
    g = 9.81

    if tipo_manometro == "Tubo Inclinado":
        h_efetivo = h_coluna * np.sin(np.radians(angulo_graus))
    else:
        h_efetivo = h_coluna

    p_hidrostatica = rho_fluido * g * h_efetivo
    p_absoluta = p_atm + p_hidrostatica

    return {
        "P_atm_Pa": p_atm,
        "P_atm_kPa": p_atm / 1000,
        "P_hid_Pa": p_hidrostatica,
        "P_hid_kPa": p_hidrostatica / 1000,
        "P_abs_Pa": p_absoluta,
        "P_abs_kPa": p_absoluta / 1000,
        "h_efetivo": h_efetivo,
    }


# ==============================================================
# ABA 4 — SISTEMA ACOPLADO TERMO-HIDRÁULICO
# ==============================================================

def calcular_sistema_acoplado(
    rho_fluido: float,
    h_fluido: float,
    calor_kJ: float,
    area_piston: float = 0.05,
) -> dict:
    """
    Simula um atuador termo-hidráulico: gás confinado recebe calor
    e expande (processo isobárico) contra uma coluna de fluido.

    Parâmetros
    ----------
    rho_fluido  : massa específica do fluido sobre o pistão (kg/m³)
    h_fluido    : altura da coluna de fluido (m)
    calor_kJ    : calor injetado no gás (kJ)
    area_piston : área transversal do pistão (m²)

    Retorna
    -------
    dict com força, trabalho, ΔU, T_final, deslocamento e alturas do pistão.
    """
    g = 9.81
    R = 8.314
    n_moles = 10.0
    Cv = R / 0.4      # N₂, γ = 1.4
    Cp = Cv + R
    T0 = 300.0        # K

    P_total = 101325 + rho_fluido * g * h_fluido
    F_fluido = P_total * area_piston

    Q_J = calor_kJ * 1000
    delta_T = Q_J / (n_moles * Cp)
    T_final = T0 + delta_T

    V_inicial = (n_moles * R * T0) / P_total
    delta_V = (n_moles * R * delta_T) / P_total
    V_final = V_inicial + delta_V

    W_J = P_total * delta_V
    delta_U_J = n_moles * Cv * delta_T

    y_inicial = V_inicial / area_piston
    deslocamento = delta_V / area_piston
    y_final = y_inicial + deslocamento

    return {
        "P_total_kPa": P_total / 1000,
        "F_fluido_kN": F_fluido / 1000,
        "W_kJ": W_J / 1000,
        "delta_U_kJ": delta_U_J / 1000,
        "Q_kJ": calor_kJ,
        "T_inicial_C": T0 - 273.15,
        "T_final_C": T_final - 273.15,
        "delta_T": delta_T,
        "V_inicial_m3": V_inicial,
        "V_final_m3": V_final,
        "delta_V_L": delta_V * 1000,
        "y_inicial": y_inicial,
        "y_final": y_final,
        "deslocamento_m": deslocamento,
        "deslocamento_cm": deslocamento * 100,
    }