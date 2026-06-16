'''
Servidor Flask
Conectar os formulários HTML aos módulos Python.
Cada rota recebe os dados do formulário (POST), chama o módulo Python correspondente e retorna os resultados como JSON para o JavaScript da página.

Executar:
 pip install flask numpy matplotlib
 python app.py

Acesse: http://localhost:5000
'''

from flask import Flask, render_template, request, jsonify, send_file

# Importa os módulos Python da pasta python/
# Os nomes batem com os arquivos .py dentro de python/
from python import custo as mod_custo # custo.py
from python import blend as mod_blend # blend.py
from python import conversor as mod_conv # conversor.py
from python import financiamento as mod_fin # financiamento.py
from python import matriz_talhoes as mod_mat # matriz_talhoes.py

# Configuração do Flask
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Rotas de Páginas (Get)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/custo")
def pagina_custo():
    return render_template("custo.html")

@app.route("/financiamento")
def pagina_financiamento():
    return render_template("financiamento.html")

@app.route("/conversor")
def pagina_conversor():
    return render_template("conversor.html")

@app.route("/mapa-talhoes")
def pagina_mapa():
    return render_template("mapa_talhoes.html")

@app.route("/blend")
def pagina_blend():
    return render_template("blend.html")

@app.route("/como-funciona")
def pagina_como_funciona():
    return render_template("como_funciona.html")

@app.route('/baixar-grafico')
def baixar_grafico():
    return send_file(
        'static/img/graficos/grafico_custo.png',
        as_attachment=True,
        download_name='grafico_custo.png'
)


# Rotas de API (Post)

@app.route("/api/custo", methods=["POST"])
def api_custo():
    # Recebe dados do formulário de custo, retorna cálculos e gráfico
    try:
        dados = request.get_json()

        custo_fixo = float(dados["custo_fixo"])
        custo_var = float(dados["custo_variavel"])
        preco_venda = float(dados["preco_venda"])
        sacas = float(dados["sacas"])

        ct = mod_custo.custo_total(sacas, custo_fixo, custo_var)
        rt = mod_custo.receita_total(sacas, preco_venda)
        lc = mod_custo.lucro(sacas, custo_fixo, custo_var, preco_venda)

        try:
            pe = mod_custo.ponto_equilibrio(custo_fixo, preco_venda, custo_var)
        except ValueError:
            pe = None

        grafico = mod_custo.gerar_grafico(custo_fixo, custo_var, preco_venda, sacas * 1.5)

        return jsonify({
            "sucesso": True,
            "custo_total": round(ct, 2),
            "receita": round(rt, 2),
            "lucro": round(lc, 2),
            "ponto_equilibrio": round(pe, 1) if pe else None,
            "grafico": grafico
        })

    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


@app.route("/api/financiamento", methods=["POST"])
def api_financiamento():
    # Recebe dados do financiamento, retorna tabela de amortização e gráfico
    try:
        dados = request.get_json()
        valor = float(dados["valor_total"])
        taxa = float(dados["taxa_juros"]) / 100
        n = int(dados["num_parcelas"])
        entrada = float(dados.get("entrada", 0))

        pv = valor - entrada

        res = mod_fin.resumo(valor, taxa, n, entrada)
        tabela = mod_fin.tabela_amortizacao(pv, taxa, n)
        grafico = mod_fin.gerar_grafico(pv, taxa, n)

        return jsonify({"sucesso": True, "resumo": res, "tabela": tabela, "grafico": grafico})

    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


@app.route("/api/converter-numero", methods=["POST"])
def api_converter_numero():
    # Converte um número entre bases decimal, binário e hexadecimal
    try:
        dados = request.get_json()
        valor = str(dados["valor"]).strip()
        base_origem = int(dados["base"])

        resultado = mod_conv.converter_numero(valor, base_origem)
        return jsonify({"sucesso": True, **resultado})

    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


@app.route("/api/operacoes-logicas", methods=["POST"])
def api_operacoes_logicas():
    # Aplica AND, OR e NOT bit a bit sobre dois números
    try:
        dados = request.get_json()
        a = int(dados["a"])
        b = int(dados["b"])

        resultado = mod_conv.operacoes_logicas(a, b)
        return jsonify({"sucesso": True, "operacoes": resultado})

    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


@app.route("/api/area-talhao", methods=["POST"])
def api_area_talhao():
    # Calcula área de talhão retangular em m², hectares e alqueires
    try:
        dados       = request.get_json()
        comprimento = float(dados["comprimento"])
        largura     = float(dados["largura"])

        resultado = mod_conv.calcular_area(comprimento, largura)
        return jsonify({"sucesso": True, **resultado})

    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


@app.route("/api/mapa-talhoes", methods=["POST"])
def api_mapa_talhoes():
    # Processa matriz de produtividade, retorna estatísticas e heatmap
    try:
        dados   = request.get_json()
        valores = dados["valores"]
        unidade = dados.get("unidade", "sc/ha")

        matriz  = mod_mat.criar_matriz(valores)
        stats   = mod_mat.estatisticas(matriz, unidade)
        tabela  = mod_mat.montar_tabela_html(matriz, unidade)
        grafico = mod_mat.gerar_grafico(matriz, unidade)

        return jsonify({"sucesso": True, "estatisticas": stats, "tabela": tabela, "grafico": grafico})

    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


@app.route("/api/blend", methods=["POST"])
def api_blend():
    # Resolve sistema linear NPK e retorna quantidades de cada fertilizante
    try:
        dados  = request.get_json()
        fontes = dados["fontes"]
        alvo_n = float(dados["alvo_n"])
        alvo_p = float(dados["alvo_p"])
        alvo_k = float(dados["alvo_k"])

        resultado = mod_blend.calcular_blend(fontes, alvo_n, alvo_p, alvo_k)

        grafico = None
        if resultado["sucesso"] and resultado["quantidades"]:
            grafico = mod_blend.gerar_grafico(fontes, resultado["quantidades"])

        resultado["grafico"] = grafico
        return jsonify(resultado)

    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


# Inicialização
if __name__ == "__main__":
    print("=" * 50)
    print("  AgroCalc — Servidor Flask")
    print("  Acesse: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)