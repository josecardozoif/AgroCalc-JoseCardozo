# matriz_talhoes.py — AgroCalc
# Mapa de Talhões

# Representa a produtividade de uma fazenda como uma matriz NumPy.
# Cada elemento da matriz = produção em sacas/ha de um talhão (setor).
# Gera visualização tipo "mapa de calor" com Matplotlib.

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

PASTA_GRAFICOS = os.path.join(
    os.path.dirname(__file__), "..", "static", "img", "graficos"
)


def criar_matriz(valores: list[list[float]]) -> np.ndarray:
    """
    Converte a lista de listas recebida do formulário HTML em uma matriz NumPy.

    Parâmetros:
        valores -- lista de listas de floats
                   Ex: [[62, 58, 71], [70, 80, 75]]

    Retorna:
        np.ndarray 2D com os valores de produtividade
    """
    return np.array(valores, dtype=float)


def estatisticas(matriz: np.ndarray, unidade: str = "sc/ha") -> dict:
    """
    Calcula as estatísticas da matriz de produtividade.

    Usa funções do NumPy para operar sobre toda a matriz de uma vez.
    axis=0 → opera ao longo das linhas (resultado por coluna)
    axis=1 → opera ao longo das colunas (resultado por linha)

    Parâmetros:
        matriz  -- np.ndarray 2D de produtividade
        unidade -- unidade de medida (padrão: "sc/ha")

    Retorna:
        Dicionário com estatísticas gerais e por linha
    """
    n_lin, n_col = matriz.shape

    # Letras para nomear os setores (A, B, C...)
    letras = "ABCDEFGH"

    # Médias por linha (cada linha é um setor)
    medias_por_linha = matriz.mean(axis=1).tolist()

    # Monta lista de setores com nome e média
    setores = [
        {
            "nome":  f"Setor {letras[i]}",
            "media": round(medias_por_linha[i], 1)
        }
        for i in range(n_lin)
    ]

    return {
        "media_geral": round(float(matriz.mean()), 1),
        "maior_valor": round(float(matriz.max()), 1),
        "menor_valor": round(float(matriz.min()), 1),
        "desvio_padrao": round(float(matriz.std()), 2), # Variabilidade da produção
        "total_talhoes": int(matriz.size),
        "setores": setores,
        "unidade": unidade
    }


def montar_tabela_html(matriz: np.ndarray, unidade: str = "sc/ha") -> list[list]:
    """
    Prepara os dados da matriz para renderização na tabela HTML.
    Atribui uma classe CSS de cor (calor-alto/medio/baixo) para cada célula.

    Parâmetros:
        matriz  -- np.ndarray 2D
        unidade -- unidade de medida

    Retorna:
        Lista de linhas, cada linha é uma lista de dicionários com:
        valor, classe_css
    """
    minimo = float(matriz.min())
    maximo = float(matriz.max())
    escala = maximo - minimo if maximo != minimo else 1

    def classe_calor(v: float) -> str:
        # Determina a classe CSS pelo percentual no intervalo min-max.
        percentual = (v - minimo) / escala
        if percentual < 0.33:
            return "calor-baixo"
        elif percentual < 0.66:
            return "calor-medio"
        else:
            return "calor-alto"

    tabela = []
    for linha in matriz:
        linha_dados = [
            {"valor": round(float(v), 1), "classe": classe_calor(float(v)), "unidade": unidade}
            for v in linha
        ]
        tabela.append(linha_dados)

    return tabela


def gerar_grafico(matriz: np.ndarray, unidade: str = "sc/ha") -> str:
    """
    Gera um mapa de calor (heatmap) da produtividade dos talhões usando Matplotlib.

    O heatmap usa um gradiente de cores:
        vermelho → amarelo → verde
    representando baixa → média → alta produtividade.

    Parâmetros:
        matriz - np.ndarray 2D de produtividade
        unidade - unidade de medida para rótulos

    Retorna:
        Caminho relativo da imagem salva (str)
    """
    n_lin, n_col = matriz.shape
    letras = "ABCDEFGH"

    # Gradiente personalizado: vermelho → amarelo → verde (cores do CSS)
    cores = ["#ef5350", "#ffee58", "#66bb6a"]
    cmap  = mcolors.LinearSegmentedColormap.from_list("agro_calor", cores)

    fig, ax = plt.subplots(figsize=(max(6, n_col * 1.5), max(4, n_lin * 1.2)))
    fig.patch.set_facecolor("#f5f5f0")
    ax.set_facecolor("#f5f5f0")

    # imshow: exibe a matriz como imagem colorida
    im = ax.imshow(matriz, cmap=cmap, aspect="auto")

    # Barra de cores lateral
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(f"Produtividade ({unidade})", fontsize=10)

    # Rótulos dos eixos
    ax.set_xticks(range(n_col))
    ax.set_xticklabels([f"Col {c+1}" for c in range(n_col)])
    ax.set_yticks(range(n_lin))
    ax.set_yticklabels([f"Setor {letras[l]}" for l in range(n_lin)])

    # Valores dentro de cada célula
    for i in range(n_lin):
        for j in range(n_col):
            val = matriz[i, j]
            # Cor do texto contrasta com o fundo da célula
            cor_texto = "white" if val < (matriz.min() + (matriz.max() - matriz.min()) * 0.5) else "#1b2117"
            ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                    fontsize=11, fontweight="bold", color=cor_texto)

    ax.set_title("Mapa de Produtividade por Talhão", fontsize=13,
                 fontweight="bold", color="#2e7d32")
    plt.tight_layout()

    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    caminho = os.path.join(PASTA_GRAFICOS, "grafico_talhoes.png")
    plt.savefig(caminho, dpi=120, bbox_inches="tight")
    plt.close(fig)

    return "static/img/graficos/grafico_talhoes.png"