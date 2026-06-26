"""Ciências térmicas: temperatura e calor sensível (Módulo 1)."""


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
