# ThermoFluid Lab

Simulador interativo em Streamlit para o estudo de Fenômenos de Transporte: ciências térmicas, 1ª Lei da Termodinâmica, estática dos fluidos e um sistema termo-hidráulico acoplado.

## Módulos

1. **Ciências Térmicas** — temperatura, calor sensível e energia interna.
2. **Energia e Trabalho** — 1ª Lei da Termodinâmica com diagramas P×V para processos isotérmico, isobárico, adiabático e politrópico.
3. **Estática e Manometria** — pressão hidrostática, pressão atmosférica e manômetros (tubo em U e tubo inclinado).
4. **Sistema Acoplado** — simulação de um atuador termo-hidráulico que integra os três módulos anteriores.

## Estrutura

```
app.py            # ponto de entrada (st.navigation)
engine.py         # bancos de dados de substâncias, fluidos e gases
formulas/         # funções de cálculo físico, por domínio
components/       # componentes de UI reutilizáveis (cards, gráficos, layout)
pages/            # uma página Streamlit por módulo
assets/           # CSS, imagens e ícones
```

## Setup

```bash
uv sync
uv run streamlit run app.py
```

Ou, sem `uv`:

```bash
pip install -e .
streamlit run app.py
```
