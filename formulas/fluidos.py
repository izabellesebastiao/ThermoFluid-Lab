"""Estática dos fluidos: pressão atmosférica e manometria (Módulo 3)."""
import numpy as np

GRAVIDADE = 9.81  # m/s²
P_MAR = 101325.0  # Pa — pressão atmosférica ao nível do mar
RHO_AR = 1.2  # kg/m³ — densidade média do ar (válida até ~4000 m)


def calcular_p_atm(altitude: float) -> float:
    """
    Pressão atmosférica local pela equação barométrica simplificada (Pa).

    Parâmetros
    ----------
    altitude : altitude acima do nível do mar (m)
    """
    return max(P_MAR - RHO_AR * GRAVIDADE * altitude, 0.0)


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
    if tipo_manometro == "Tubo Inclinado":
        h_efetivo = h_coluna * np.sin(np.radians(angulo_graus))
    else:
        h_efetivo = h_coluna

    p_hidrostatica = rho_fluido * GRAVIDADE * h_efetivo
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
