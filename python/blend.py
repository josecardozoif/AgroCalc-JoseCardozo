'''
Blend de Fertilizante NPK
Resolve o sistema de equações lineares 3×3 para descobrir quanto de cada fertilizante usar para atingir o alvo NPK.

Sistema: A * x = b
   A = matriz de composição dos fertilizantes (% de N, P, K)
   x = vetor incógnita (kg de cada fertilizante por hectare)
   b = vetor alvo (kg de N, P e K desejados por hectare)
'''

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

PASTA_GRAFICOS = os.path.join(
    os.path.dirname(__file__), "..", "static", "img", "graficos"
)


def montar_matriz(fontes: list[dict]) -> np.ndarray:
    """
    Monta a matriz de coeficientes A a partir das fontes de fertilizante.

    Cada coluna de A representa uma fonte; cada linha representa um nutriente.
    Os valores de % são convertidos para decimal (÷100).

    Parâmetros:
        fontes -- lista de 3 dicionários, cada um com chaves:
                  nome, n (% N), p (% P), k (% K)

    Retorna:
        np.ndarray 3×3 com a composição em decimal

    Exemplo:
        Ureia (45%N, 0%P, 0%K) → coluna [0.45, 0.00, 0.00]
    """
    if len(fontes) != 3:
        raise ValueError("São necessárias exatamente 3 fontes de fertilizante.")

    # Cada coluna da matriz = composição de uma fonte
    # Transposta porque é mais legível montar linha por linha e depois transpor
    A = np.array([
        [fontes[0]["n"] / 100, fontes[1]["n"] / 100, fontes[2]["n"] / 100],  # Linha N
        [fontes[0]["p"] / 100, fontes[1]["p"] / 100, fontes[2]["p"] / 100],  # Linha P
        [fontes[0]["k"] / 100, fontes[1]["k"] / 100, fontes[2]["k"] / 100],  # Linha K
    ], dtype=float)

    return A


def calcular_determinante(A: np.ndarray) -> float:
    """
    Calcula o determinante da matriz de coeficientes usando NumPy.

    O determinante indica se o sistema tem solução única:
        det != 0 > sistema determinado (solução única)
        det = 0 > sistema indeterminado ou impossível

    Parâmetros:
        A -- np.ndarray 3×3

    Retorna:
        Determinante como float
    """
    return float(np.linalg.det(A))


def resolver_sistema(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Resolve o sistema linear A * x = b usando NumPy.

    numpy.linalg.solve usa eliminação de Gauss internamente,
    equivalente a calcular x = A⁻¹ * b.

    Parâmetros:
        A -- np.ndarray 3×3 (matriz de coeficientes)
        b -- np.ndarray 1D com 3 elementos (vetor alvo NPK em kg/ha)

    Retorna:
        np.ndarray com as quantidades de cada fertilizante (kg/ha)

    Lança:
        np.linalg.LinAlgError se a matriz for singular (det ≈ 0)
    """
    return np.linalg.solve(A, b)


def classificar_insumos(fontes: list[dict]) -> dict:
    """
    Classifica as fontes de fertilizante em conjuntos por origem.

    Classificação baseada no campo 'tipo' de cada fonte:
        orgânicos -- derivados de matéria orgânica (esterco, compostagem)
        quimicos  -- sintetizados industrialmente (ureia, superfosfato, KCl)
        hibridos  -- mistura de origem orgânica e sintética

    Parâmetros:
        fontes -- lista de dicionários com chave 'tipo':
                  'organico', 'quimico' ou 'hibrido'

    Retorna:
        Dicionário com três conjuntos (sets): organicos, quimicos, hibridos
    """
    organicos = set()
    quimicos  = set()
    hibridos  = set()

    for fonte in fontes:
        nome = fonte.get("nome", "?")
        tipo = fonte.get("tipo", "quimico").lower()

        if tipo == "organico":
            organicos.add(nome)
        elif tipo == "hibrido":
            hibridos.add(nome)
        else:
            quimicos.add(nome) # Padrão: químico

    return {
        "organicos": organicos,
        "quimicos":  quimicos,
        "hibridos":  hibridos
    }


def calcular_blend(fontes: list[dict], alvo_n: float,
                   alvo_p: float, alvo_k: float) -> dict:
    """
    Função principal: recebe os dados do formulário e resolve o blend.

    Parâmetros:
        fontes -- lista de 3 dicionários com nome, n, p, k, tipo
        alvo_n -- kg de Nitrogênio desejado por hectare
        alvo_p -- kg de Fósforo desejado por hectare
        alvo_k -- kg de Potássio desejado por hectare

    Retorna:
        Dicionário com:
            sucesso      -- True se o sistema tem solução única
            determinante -- valor do det(A)
            quantidades  -- lista com kg de cada fertilizante (ou None)
            classificacao-- resultado de classificar_insumos()
            erro         -- mensagem de erro (ou None)
    """
    A = montar_matriz(fontes)
    b = np.array([alvo_n, alvo_p, alvo_k], dtype=float)
    det = calcular_determinante(A)

    # Classifica os insumos independente do resultado do sistema
    classificacao = classificar_insumos(fontes)

    # Verifica se o sistema tem solução única
    if abs(det) < 1e-10:
        return {
            "sucesso": False,
            "determinante": round(det, 6),
            "quantidades": None,
            "classificacao": classificacao,
            "erro": (
                "Sistema sem solução única (det ≈ 0). "
                "As composições das fontes são linearmente dependentes. "
                "Tente fontes com composições de N, P e K diferentes."
            )
        }

    try:
        x = resolver_sistema(A, b)

        # Verifica se alguma quantidade é negativa
        aviso = None
        if any(v < -0.01 for v in x):
            aviso = (
                "Uma ou mais quantidades resultaram negativas. "
                "O alvo NPK pode não ser atingível com estas fontes."
            )

        quantidades = [
            {"nome": fontes[i]["nome"], "kg_ha": round(float(x[i]), 2)}
            for i in range(3)
        ]

        return {
            "sucesso": True,
            "determinante": round(det, 6),
            "quantidades": quantidades,
            "classificacao": classificacao,
            "aviso": aviso,
            "erro": None
        }

    except np.linalg.LinAlgError as e:
        return {
            "sucesso": False,
            "determinante": round(det, 6),
            "quantidades": None,
            "classificacao": classificacao,
            "erro": f"Erro ao resolver o sistema: {str(e)}"
        }


def gerar_grafico(fontes: list[dict], quantidades: list[dict]) -> str:
    """
    Gera gráfico de pizza mostrando a proporção de cada fertilizante no blend.

    Parâmetros:
        fontes      -- lista com os dados das fontes
        quantidades -- lista de dicionários com nome e kg_ha

    Retorna:
        Caminho relativo da imagem salva (str)
    """
    # Filtra as quantidades positivas
    dados = [(q["nome"], q["kg_ha"]) for q in quantidades if q["kg_ha"] > 0]

    if not dados:
        return None

    nomes  = [d[0] for d in dados]
    valores = [d[1] for d in dados]

    cores = ["#2e7d32", "#f9a825", "#1565c0"][:len(dados)]

    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor("#f5f5f0")

    wedges, texts, autotexts = ax.pie(
        valores,
        labels=nomes,
        colors=cores,
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops=dict(edgecolor="white", linewidth=2)
    )

    for text in texts:
        text.set_fontsize(10)
    for at in autotexts:
        at.set_fontsize(9)
        at.set_color("white")
        at.set_fontweight("bold")

    ax.set_title("Proporção do Blend de Fertilizantes (kg/ha)",
                 fontsize=12, fontweight="bold", color="#2e7d32")

    # Legenda com os valores absolutos
    legenda = [f"{n}: {v:.1f} kg/ha" for n, v in zip(nomes, valores)]
    ax.legend(legenda, loc="lower center", bbox_to_anchor=(0.5, -0.12),
              ncol=len(dados), fontsize=9)

    plt.tight_layout()

    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    caminho = os.path.join(PASTA_GRAFICOS, "grafico_blend.png")
    plt.savefig(caminho, dpi=120, bbox_inches="tight")
    plt.close(fig)

    return "static/img/graficos/grafico_blend.png"