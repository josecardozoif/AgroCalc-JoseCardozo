# alculadora de Custo de Produção

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

PASTA_GRAFICOS = os.path.join(
    os.path.dirname(__file__), "..", "static", "img", "graficos"
)

def custo_total(sacas: float, custo_fixo: float, custo_variavel: float) -> float:
    """
    Calcula o custo total usando função afim.
    Fórmula: C(x) = custo_fixo + custo_variavel * x
    """
    return custo_fixo + custo_variavel * sacas


def receita_total(sacas: float, preco_venda: float) -> float:
    """
    Calcula a receita total.
    Fórmula: R(x) = preco_venda * x
    """
    return preco_venda * sacas


def lucro(sacas: float, custo_fixo: float, custo_variavel: float, preco_venda: float) -> float:
    """
    Calcula o lucro: L(x) = R(x) - C(x)
    Valor negativo indica prejuízo.
    """
    return receita_total(sacas, preco_venda) - custo_total(sacas, custo_fixo, custo_variavel)


def ponto_equilibrio(custo_fixo: float, preco_venda: float, custo_variavel: float) -> float:
    """
    Calcula a quantidade mínima para cobrir todos os custos (break-even).
    Fórmula: x* = custo_fixo / (preco_venda - custo_variavel)
    """
    if preco_venda <= custo_variavel:
        raise ValueError("Preço de venda deve ser maior que o custo variável.")
    return custo_fixo / (preco_venda - custo_variavel)


def gerar_grafico(custo_fixo: float, custo_variavel: float,
                  preco_venda: float, sacas_max: float) -> str:
    """
    Gera gráfico de Custo x Receita com ponto de equilíbrio.
    Salva como PNG e retorna o caminho relativo para uso no HTML.
    """
    x = np.linspace(0, sacas_max, 300)
    y_custo   = custo_total(x, custo_fixo, custo_variavel)
    y_receita = receita_total(x, preco_venda)

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor("#f5f5f0")
    ax.set_facecolor("#f5f5f0")

    ax.plot(x, y_custo,   color="#c62828", linewidth=2, label="Custo Total C(x)")
    ax.plot(x, y_receita, color="#2e7d32", linewidth=2, label="Receita R(x)")
    

    if preco_venda > custo_variavel:
        pe = ponto_equilibrio(custo_fixo, preco_venda, custo_variavel)
        if 0 < pe < sacas_max:
            ax.axvline(x=pe, color="#f9a825", linestyle="--",
                       linewidth=1.5, label=f"Equilíbrio: {pe:.0f} sacas")

    ax.set_xlabel("Sacas produzidas")
    ax.set_ylabel("Valor (R$)")
    ax.set_title("Custo de Produção × Receita", fontsize=13,
                 fontweight="bold", color="#2e7d32")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda v, _: f"R$ {v:,.0f}".replace(",", "."))
    )

    fig.tight_layout()
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    caminho = os.path.join(PASTA_GRAFICOS, "grafico_custo.png")
    fig.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return "static/img/graficos/grafico_custo.png"