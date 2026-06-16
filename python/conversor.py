'''
Realiza conversões entre sistemas de numeração:
 Decimal (base 10) ↔ Binário (base 2) ↔ Hexadecimal (base 16)
 Operações lógicas bit a bit: AND, OR, NOT
 Cálculo de área de talhão em m² e hectares
'''

def decimal_para_binario(n: int) -> str:
    """
    Converte um número decimal inteiro para binário.

    Usa o algoritmo de divisões sucessivas por 2,
    coletando os restos de baixo para cima.

    Parâmetros:
        n -- número inteiro não negativo

    Retorna:
        String com a representação binária (ex: '11111111' para 255)

    Lança:
        ValueError se n for negativo
    """
    if n < 0:
        raise ValueError("Este conversor trabalha apenas com inteiros não negativos.")
    if n == 0:
        return "0"

    resultado = ""
    numero = n

    # Algoritmo: divide por 2 e coleta os restos
    while numero > 0:
        resultado = str(numero % 2) + resultado # Resto vai para a esquerda
        numero  //= 2 # Quociente inteiro
    return resultado


def decimal_para_hex(n: int) -> str:
    """
    Converte decimal para hexadecimal.

    Símbolos hex: 0-9 e A-F (onde A=10, B=11 ... F=15)
    Mesmo algoritmo do binário, mas dividindo por 16.

    Parâmetros:
        n -- número inteiro não negativo

    Retorna:
        String hexadecimal em maiúsculas (ex: 'FF' para 255)
    """
    if n < 0:
        raise ValueError("Este conversor trabalha apenas com inteiros não negativos.")
    if n == 0:
        return "0"

    # Tabela de dígitos hexadecimais
    digitos   = "0123456789ABCDEF"
    resultado = ""
    numero    = n

    while numero > 0:
        resultado = digitos[numero % 16] + resultado
        numero //= 16

    return resultado


def binario_para_decimal(b: str) -> int:
    """
    Converte string binária para decimal.

    Algoritmo posicional: cada bit vale 2^posição da direita.
    Ex: '1010' = 1*8 + 0*4 + 1*2 + 0*1 = 10

    Parâmetros:
        b -- string de 0s e 1s (ex: '1010')

    Retorna:
        Inteiro decimal

    Lança:
        ValueError se a string contiver caracteres que não sejam 0 ou 1
    """
    if not all(c in "01" for c in b):
        raise ValueError(f"'{b}' não é um número binário válido. Use apenas 0 e 1.")

    decimal = 0
    for i, bit in enumerate(reversed(b)): # Percorre da direita para esquerda
        decimal += int(bit) * (2 ** i) # Valor posicional

    return decimal


def hex_para_decimal(h: str) -> int:
    """
    Converte string hexadecimal para decimal.

    Algoritmo posicional: cada dígito vale 16^posição.
    Ex: 'FF' = 15*16 + 15 = 255

    Parâmetros:
        h -- string hexadecimal (ex: 'FF' ou 'ff')

    Retorna:
        Inteiro decimal

    Lança:
        ValueError se a string não for hexadecimal válida
    """
    h = h.upper().strip()
    digitos_validos = "0123456789ABCDEF"

    if not all(c in digitos_validos for c in h):
        raise ValueError(f"'{h}' não é um hexadecimal válido.")

    tabela  = {c: i for i, c in enumerate(digitos_validos)} # Mapa dígito → valor
    decimal = 0

    for i, digito in enumerate(reversed(h)):
        decimal += tabela[digito] * (16 ** i)

    return decimal


def converter_numero(valor: str, base_origem: int) -> dict:
    """
    Converte um número de qualquer base para as três representações.

    Parâmetros:
        valor - string do número na base de origem
        base_origem: 10 (decimal), 2 (binário) ou 16 (hexadecimal)

    Retorna:
        Dicionário com chaves: decimal, binario, hexadecimal
    """
    
    # Primeiro converte tudo para decimal
    if base_origem == 10:
        n = int(valor)
    elif base_origem == 2:
        n = binario_para_decimal(valor)
    elif base_origem == 16:
        n = hex_para_decimal(valor)
    else:
        raise ValueError(f"Base {base_origem} não suportada. Use 10, 2 ou 16.")

    # Depois converte de decimal para as outras bases
    return {
        "decimal": str(n),
        "binario": decimal_para_binario(n),
        "hexadecimal": decimal_para_hex(n)
    }


def operacoes_logicas(a: int, b: int) -> dict:
    """
    Realiza operações lógicas bit a bit entre dois inteiros.

    Operações:
        AND -- bits 1 apenas onde AMBOS são 1   (a & b)
        OR  -- bits 1 onde PELO MENOS UM é 1    (a | b)
        NOT -- inverte todos os bits de A        (~a, máscara 8 bits)

    Parâmetros:
        a -- primeiro operando (inteiro)
        b -- segundo operando (inteiro)

    Retorna:
        Dicionário com resultados de AND, OR, NOT em decimal, binário e hex
    """
    resultado_and = a & b
    resultado_or = a | b
    resultado_not = (~a) & 0xFF  # Máscara de 8 bits para resultado legível

    def formatar(v):
        """Formata um valor nas três bases."""
        return {
            "decimal": v,
            "binario": decimal_para_binario(v).zfill(8),  # Preenche com zeros à esquerda
            "hexadecimal": decimal_para_hex(v)
        }

    return {
        "AND": formatar(resultado_and),
        "OR": formatar(resultado_or),
        "NOT": formatar(resultado_not)
    }


def calcular_area(comprimento: float, largura: float) -> dict:
    """
    Calcula a área de um talhão retangular

    Conversão: 1 hectare = 10.000 m²
    A área em alqueires paulistas também é calculada:
    1 alqueire paulista ≈ 24.200 m²

    Parâmetros:
        comprimento -- comprimento do talhão em metros
        largura -- largura do talhão em metros

    Retorna:
        Dicionário com: metros_quadrados, hectares, alqueires
    """
    if comprimento <= 0 or largura <= 0:
        raise ValueError("Comprimento e largura devem ser maiores que zero.")

    m2 = comprimento * largura
    hectares = m2 / 10_000
    alqueires = m2 / 24_200 # Conversão para alqueire paulista

    return {
        "metros_quadrados": round(m2, 2),
        "hectares": round(hectares, 4),
        "alqueires": round(alqueires, 4)
    }