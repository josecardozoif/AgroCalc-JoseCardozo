# financiamento.py — AgroCalc
# Módulo: Financiamento Agrícola
# Disciplina: Matemática Aplicada — Matemática Financeira
#
# Simula o financiamento de máquinas e equipamentos agrícolas
# usando o Sistema de Amortização Price (parcelas fixas, juros compostos).
# Fórmula PMT: parcela = PV * [i*(1+i)^n] / [(1+i)^n - 1]

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

PASTA_GRAFICOS = os.path.join(
    os.path.dirname(__file__), "..", "static", "img", "graficos"
)


def calcular_parcela(pv: float, taxa: float, n: int) -> float:
    """
    Calcula o valor da parcela fixa pelo Sistema Price (juros compostos).

    Fórmula PMT:
        parcela = PV * [i * (1+i)^n] / [(1+i)^n - 1]

    Parâmetros:
        pv   -- Valor Presente: total financiado após a entrada (R$)
        taxa -- Taxa de juros mensal em decimal (ex: 0.015 para 1,5%)
        n    -- Número de parcelas (meses)

    Retorna:
        Valor da parcela mensal fixa (float)

    Lança:
        ValueError se taxa ou n forem inválidos
    """
    if taxa <= 0:
        raise ValueError("Taxa de juros deve ser maior que zero.")
    if n <= 0:
        raise ValueError("Número de parcelas deve ser maior que zero.")

    fator = (1 + taxa) ** n              # (1+i)^n — fator de capitalização
    return pv * (taxa * fator) / (fator - 1)


def tabela_amortizacao(pv: float, taxa: float, n: int) -> list[dict]:
    """
    Gera a tabela de amortização completa mês a mês (Sistema Price).

    A cada mês:
      - Juros   = saldo_devedor * taxa
      - Amort.  = parcela - juros
      - Saldo   = saldo anterior - amortização

    Parâmetros:
        pv   -- valor financiado (R$)
        taxa -- taxa mensal em decimal
        n    -- número de parcelas

    Retorna:
        Lista de dicionários, um por parcela, com as chaves:
        mes, parcela, juros, amortizacao, saldo
    """
    parcela = calcular_parcela(pv, taxa, n)
    saldo = pv
    tabela = []

    for mes in range(1, n + 1):
        juros = saldo * taxa          # Juros incidem sobre o saldo devedor
        amortizacao  = parcela - juros       # Parte que reduz a dívida
        saldo       -= amortizacao           # Atualiza saldo

        tabela.append({
            "mes": mes,
            "parcela": round(parcela, 2),
            "juros": round(juros, 2),
            "amortizacao": round(amortizacao, 2),
            "saldo": round(max(saldo, 0), 2) # Evita -0.00 por arredondamento
        })

    return tabela


def resumo(pv: float, taxa: float, n: int, entrada: float = 0) -> dict:
    """
    Calcula o resumo financeiro do financiamento.

    Parâmetros:
        pv - valor total do bem (R$)
        taxa - taxa mensal em decimal
        n - número de parcelas
        entrada - valor de entrada pago (R$); padrão = 0

    Retorna:
        Dicionário com: parcela, total_pago, total_juros, valor_financiado
    """
    valor_financiado = pv - entrada
    parcela = calcular_parcela(valor_financiado, taxa, n)
    total_pago = parcela * n + entrada
    total_juros = total_pago - pv

    return {
        "parcela": round(parcela, 2),
        "total_pago": round(total_pago, 2),
        "total_juros": round(total_juros, 2),
        "valor_financiado": round(valor_financiado, 2)
    }


def gerar_grafico(pv: float, taxa: float, n: int) -> str:
    """
    Gera gráfico de barras empilhadas mostrando a evolução de
    juros e amortização ao longo das parcelas.

    Parâmetros:
        pv   -- valor financiado (R$)
        taxa -- taxa mensal em decimal
        n    -- número de parcelas

    Retorna:
        Caminho relativo da imagem salva (str)
    """
    tabela = tabela_amortizacao(pv, taxa, n)

    meses = [r["mes"]         for r in tabela]
    juros_vals = [r["juros"]       for r in tabela]
    amort_vals = [r["amortizacao"] for r in tabela]

    # Agrupa por grupos de meses se n > 24 para melhor visualização
    if n > 24:
        passo = n // 12
        meses = meses[::passo]
        juros_vals = juros_vals[::passo]
        amort_vals = amort_vals[::passo]

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#f5f5f0")
    ax.set_facecolor("#f5f5f0")

    # Barras empilhadas: amortização (verde) embaixo, juros (vermelho) em cima
    ax.bar(meses, amort_vals, label="Amortização",
           color="#2e7d32", alpha=0.85, width=0.6)
    ax.bar(meses, juros_vals, bottom=amort_vals, label="Juros",
           color="#c62828", alpha=0.85, width=0.6)

    ax.set_xlabel("Parcela (mês)", fontsize=11)
    ax.set_ylabel("Valor (R$)", fontsize=11)
    ax.set_title("Composição das Parcelas — Sistema Price", fontsize=13,
                 fontweight="bold", color="#2e7d32")
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda v, _: f"R$ {v:,.0f}".replace(",", "."))
    )

    plt.tight_layout()

    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    caminho = os.path.join(PASTA_GRAFICOS, "grafico_financiamento.png")
    plt.savefig(caminho, dpi=120, bbox_inches="tight")
    plt.close(fig)

    return "static/img/graficos/grafico_financiamento.png"