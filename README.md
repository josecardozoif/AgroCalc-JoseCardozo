# AgroCalc
## José Eduardo Cardozo Araújo

Sistema web voltado ao agronegócio que integra interface HTML/CSS, lógica de calculo em Python e fundamentos de computacao. Desenvolvido como Projeto Integrador das disciplinas LAEC, ITC e Matematica Aplicada.

---

## Descricao

O AgroCalc oferece ferramentas de calculo para pequenos e medios produtores rurais: calculo de custo de producao, simulacao de financiamento de maquinas, conversao entre sistemas de numeracao, mapeamento de produtividade por talhao e formulacao de blend de fertilizantes NPK.

A interface e servida pelo Flask, que tambem expoe uma API interna consumida pelo JavaScript de cada pagina via `fetch()`. Os calculos matematicos sao executados inteiramente em Python, e os graficos sao gerados pelo Matplotlib e salvos como imagens PNG exibidas no site.

---

## Estrutura do Projeto

```
AgroCalc/
|
|-- app.py                     Servidor Flask: rotas de paginas e rotas de API
|-- requirements.txt           Dependencias Python do projeto
|-- README.md
|
|-- python/                    Modulos de calculo em Python
|   |-- __init__.py
|   |-- custo.py               Funcao afim, ponto de equilibrio, grafico custo x receita
|   |-- financiamento.py       Formula Price, tabela de amortizacao, grafico de parcelas
|   |-- conversor.py           Conversao decimal/binario/hex, operacoes logicas, area de talhao
|   |-- matriz_talhoes.py      Matriz NumPy de produtividade, heatmap Matplotlib
|   |-- blend.py               Sistema linear NPK, determinante, grafico de pizza
|
|-- templates/                 Paginas HTML servidas pelo Flask
|   |-- base.html              Modelo base (nao acessado diretamente)
|   |-- index.html             Painel principal
|   |-- custo.html             Calculadora de custo de producao
|   |-- financiamento.html     Simulador de financiamento agricola
|   |-- conversor.html         Conversor de bases e area de talhao
|   |-- mapa_talhoes.html      Mapa de produtividade por setor
|   |-- blend.html             Blend de fertilizante NPK
|   |-- como_funciona.html     Pagina de ITC: CPU, memoria, glossario e linha do tempo
|
|-- static/
    |-- css/
    |   |-- style.css          Estilos globais, variaveis CSS, dark mode, responsividade
    |   |-- custo.css
    |   |-- financiamento.css
    |   |-- conversor.css
    |   |-- mapa_talhoes.css
    |   |-- blend.css
    |   |-- como_funciona.css
    |
    |-- js/
    |   |-- nav.js             Injeta header e footer em todas as paginas via JavaScript
    |   |-- custo.js
    |   |-- financiamento.js
    |   |-- conversor.js
    |   |-- mapa_talhoes.js
    |   |-- blend.js
    |
    |-- img/
        |-- graficos/          Graficos PNG gerados pelo Matplotlib em tempo de execucao
```

---

## Requisitos

- Python 3.10 ou superior
- pip

Bibliotecas utilizadas:

| Biblioteca   | Versao minima | Uso no projeto                              |
|--------------|---------------|---------------------------------------------|
| Flask        | 3.0.0         | Servidor web, roteamento, render_template   |
| NumPy        | 1.26.0        | Matrizes de talhoes, algebra linear (blend) |
| Matplotlib   | 3.8.0         | Geracao de graficos exportados como PNG     |

---

## Instalacao e Execucao

**1. Clone ou baixe o projeto e entre na pasta raiz:**

```bash
cd AgroCalc
```

**2. Instale as dependencias:**

```bash
pip install -r requirements.txt
```

**3. Execute o servidor:**

```bash
python app.py
```

**4. Acesse no navegador:**

```
http://localhost:5000
```

---

## Modulos

### Painel Principal
Pagina inicial com apresentacao do sistema, cards de acesso rapido a cada modulo, linha do tempo do desenvolvimento e glossario de termos tecnicos.

### Calculadora de Custo
Calcula o custo total de producao usando a funcao afim `C(x) = custo_fixo + custo_variavel * x`. Tambem calcula a receita, o lucro ou prejuizo e o ponto de equilibrio. Gera grafico de Custo x Receita com Matplotlib.

### Financiamento Agricola
Simula o financiamento de maquinas e equipamentos pelo Sistema Price (juros compostos). Calcula a parcela fixa com a formula `PMT = PV * [i*(1+i)^n] / [(1+i)^n - 1]` e exibe a tabela de amortizacao completa com saldo devedor mes a mes. Gera grafico de barras com a composicao de juros e amortizacao por parcela.

### Conversor de Dados
Realiza conversoes entre os sistemas de numeracao decimal, binario e hexadecimal usando o algoritmo de divisoes sucessivas. Executa operacoes logicas bit a bit: AND, OR e NOT. Calcula a area de talhoes retangulares em metros quadrados, hectares e alqueires paulistas.

### Mapa de Talhoes
Representa a produtividade de uma fazenda como uma matriz NumPy. O usuario define as dimensoes e os valores de cada talhao. O sistema calcula media, desvio padrao, maior e menor produtividade, e gera um heatmap com gradiente de cores indicando desempenho relativo de cada setor.

### Blend de Fertilizante
Resolve o sistema linear 3x3 `A * x = b` usando `numpy.linalg.solve` para determinar a quantidade de cada fertilizante necessaria para atingir um alvo NPK por hectare. Verifica o determinante da matriz antes de resolver: se `det = 0`, o sistema nao tem solucao unica. Classifica as fontes de fertilizante em conjuntos por origem (organico, quimico ou hibrido). Gera grafico de pizza com a proporcao de cada fertilizante no blend.

### Como Funciona
Pagina de conteudo de ITC explicando a arquitetura do sistema do ponto de vista computacional: CPU, memoria RAM e armazenamento. Apresenta o fluxo de dados desde o preenchimento do formulario ate a exibicao do resultado, a linha do tempo do desenvolvimento do projeto e um glossario com os principais termos tecnicos utilizados.

---

## Arquitetura de Integracao

```
Formulario HTML
     |
     | (evento onclick)
     v
  arquivo .js da pagina
     |
     | fetch() — envia JSON via POST
     v
  app.py (Flask)  — rota /api/modulo
     |
     | chama funcoes do modulo .py
     v
  modulo Python  — calcula e gera grafico
     |
     | retorna JSON com resultados + caminho da imagem
     v
  arquivo .js da pagina
     |
     | preenche os elementos HTML com os dados recebidos
     v
Resultado exibido na pagina sem recarregar
```

### Rotas de paginas (GET)

| Rota            | Template renderizado  |
|-----------------|-----------------------|
| /               | index.html            |
| /custo          | custo.html            |
| /financiamento  | financiamento.html    |
| /conversor      | conversor.html        |
| /mapa-talhoes   | mapa_talhoes.html     |
| /blend          | blend.html            |
| /como-funciona  | como_funciona.html    |

### Rotas de API (POST)

| Rota                   | Modulo Python       | Retorno                            |
|------------------------|---------------------|------------------------------------|
| /api/custo             | custo.py            | custo, receita, lucro, grafico     |
| /api/financiamento     | financiamento.py    | parcela, tabela, grafico           |
| /api/converter-numero  | conversor.py        | decimal, binario, hexadecimal      |
| /api/operacoes-logicas | conversor.py        | AND, OR, NOT nas tres bases        |
| /api/area-talhao       | conversor.py        | m2, hectares, alqueires            |
| /api/mapa-talhoes      | matriz_talhoes.py   | estatisticas, tabela, grafico      |
| /api/blend             | blend.py            | quantidades, determinante, grafico |

---

## Decisoes Tecnicas

**Por que Flask e nao HTML puro?**
HTML puro nao permite executar codigo Python no servidor. O Flask e necessario para receber os dados dos formularios, processar os calculos em Python e retornar os resultados sem recarregar a pagina.

**Por que os arquivos .js ainda existem se os calculos sao em Python?**
Python executa no servidor; JavaScript executa no navegador. O papel do `.js` e ler os campos do formulario, enviar os dados ao Flask via `fetch()` e exibir os resultados retornados na pagina. Sem ele, o botao calcular nao teria acao.

**Por que `matplotlib.use("Agg")`?**
O backend padrao do Matplotlib tenta abrir uma janela grafica no sistema operacional, o que nao e possivel em um servidor. O backend `Agg` renderiza o grafico diretamente em memoria e permite salvar como arquivo, sem interface grafica.

**Por que `nav.js` injeta o header via JavaScript?**
Em HTML puro nao existe heranca de templates. O `nav.js` simula esse comportamento injetando o mesmo `<header>` e `<footer>` em todas as paginas dinamicamente, de forma que qualquer alteracao na navegacao precise ser feita em um unico arquivo.

---

## Disciplinas Contempladas

**LAEC - Linguagem de Apresentacao e Estruturação de Conteudos**
Estrutura HTML com header, nav, main, section e footer. Formularios com validacao. Responsividade com CSS Grid e Flexbox. Animacao de botoes. Navegacao multipage.

**ITC - Introducao a Tecnologia da Computacao**
Conversao entre sistemas de numeracao: decimal, binario e hexadecimal. Operacoes logicas AND, OR e NOT. Pagina explicando CPU, memoria e armazenamento. Linha do tempo do projeto.

**Matematica Aplicada**
Funcao afim para calculo de custo de producao. Juros compostos e Sistema Price para financiamento. Matrizes NumPy para mapa de talhoes. Sistema linear 3x3 e determinante para blend NPK. Classificacao de insumos em conjuntos.