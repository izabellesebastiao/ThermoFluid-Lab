"""Banco de dados de substâncias, fluidos e gases usados nos módulos de cálculo."""

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
    # Cores do tema DaisyUI "cupcake" — https://daisyui.com/docs/themes/
    "Água":          {"rho": 1000,  "cor": "#1c92f2"},  # info
    "Água do mar":   {"rho": 1030,  "cor": "#65c3c8"},  # primary
    "Etanol":        {"rho": 789,   "cor": "#ef9fbc"},  # secondary
    "Óleo mineral":  {"rho": 850,   "cor": "#ff9900"},  # warning
    "Óleo de motor": {"rho": 870,   "cor": "#ff5724"},  # error
    "Mercúrio":      {"rho": 13600, "cor": "#9aa0a6"},  # cinza metálico (sem token cupcake)
    "Glicerina":     {"rho": 1261,  "cor": "#009485"},  # success
    "Gasolina":      {"rho": 720,   "cor": "#eeaf3a"},  # accent
    "Fluido da Prova": {"rho": 3500, "cor": "#291334"},  # neutral
}

GASES_TERMICOS = {
    "Nitrogênio (N₂)": {"gamma": 1.4,  "M": 28.0},
    "Argônio (Ar)":    {"gamma": 1.67, "M": 39.9},
    "Ar Atmosférico":  {"gamma": 1.4,  "M": 29.0},
    "CO₂":             {"gamma": 1.3,  "M": 44.0},
    "Hidrogênio (H₂)": {"gamma": 1.41, "M": 2.0},
}
