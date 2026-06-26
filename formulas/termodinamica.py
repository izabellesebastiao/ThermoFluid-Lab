"""Termodinâmica de gás ideal: 1ª Lei, processos P×V e sistema acoplado (Módulos 2 e 4)."""
import numpy as np

from engine import GASES_TERMICOS

R = 8.314  # J/mol·K — constante universal dos gases
T_REF = 300.0  # K (27 °C) — temperatura inicial de referência usada nas simulações
P_ATM_PADRAO = 101325.0  # Pa — pressão atmosférica ao nível do mar
GRAVIDADE = 9.81  # m/s²
N_MOLES_PADRAO = 10.0  # mol — quantidade de gás usada nas simulações


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
    if tipo_processo == "Politrópico" and abs(n_politropico - 1.0) < 1e-9:
        raise ValueError("n_politropico não pode ser 1.0 (divisão por zero); use o processo Isotérmico nesse caso.")

    n_moles = N_MOLES_PADRAO
    T_inicial = T_REF

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


def calcular_sistema_acoplado(
    rho_fluido: float,
    h_fluido: float,
    calor_kJ: float,
    area_piston: float = 0.05,
    gas: str = "Nitrogênio (N₂)",
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
    gas         : chave em GASES_TERMICOS — define γ do gás confinado

    Retorna
    -------
    dict com força, trabalho, ΔU, T_final, deslocamento e alturas do pistão.
    """
    if area_piston <= 0:
        raise ValueError("area_piston deve ser positiva.")

    props = GASES_TERMICOS.get(gas, GASES_TERMICOS["Nitrogênio (N₂)"])
    gamma = props["gamma"]

    n_moles = N_MOLES_PADRAO
    Cv = R / (gamma - 1)
    Cp = Cv + R
    T0 = T_REF

    P_total = P_ATM_PADRAO + rho_fluido * GRAVIDADE * h_fluido
    if P_total <= 0:
        raise ValueError("P_total deve ser positiva.")
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
        "gamma": gamma,
    }
