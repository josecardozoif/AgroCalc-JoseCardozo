/*
  Conecta o formulário de custo à API Flask (/api/custo).

  Fluxo do que será feito:
    1. Usuário preenche o form e clica em "Calcular"
    2. fetch() envia os dados como JSON para o Flask (app.py)
    3. Flask chama custo.py e retorna os resultados + caminho do gráfico
    4. Este script exibe os resultados e a imagem na página
*/

async function calcularCusto() {
    /* Leitura dos campos — IDs batem com os do custo.html */
    const payload = {
        custo_fixo: parseFloat(document.getElementById("custo-fixo").value) || 0,
        custo_variavel: parseFloat(document.getElementById("custo-variavel").value) || 0,
        preco_venda: parseFloat(document.getElementById("preco-venda").value) || 0,
        sacas: parseFloat(document.getElementById("sacas").value) || 0,
    };

    /* Validação básica */
    if (payload.sacas <= 0) {
        alert("Informe a quantidade de sacas produzidas.");
        return;
    }

    try {
        /* Envia os dados ao Flask como JSON */
        const resposta = await fetch("/api/custo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const dados = await resposta.json();

        if (!dados.sucesso) {
            alert("Erro: " + dados.erro);
            return;
        }

        /* Preenche os cards de resultado — IDs batem com o custo.html */
        document.getElementById("res-custo-total").textContent = fmt(dados.custo_total);
        document.getElementById("res-receita").textContent = fmt(dados.receita);
        document.getElementById("res-lucro").textContent = fmt(dados.lucro);
        document.getElementById("res-equilibrio").textContent = dados.ponto_equilibrio
            ? `${dados.ponto_equilibrio.toLocaleString("pt-BR")} sacas`
            : "Sem equilíbrio (PV ≤ CV)";

        /* Exibe o gráfico gerado pelo Matplotlib */
        if (dados.grafico) {
            const img = document.getElementById("grafico-custo");
            img.src = "/" + dados.grafico + "?t=" + Date.now(); /* ?t= evita cache */
            img.style.display = "block";
        }

        /* Exibe o bloco de resultado */
        document.getElementById("resultado").style.display = "block";
        document.getElementById("resultado").scrollIntoView({ behavior: "smooth" });

    } catch (erro) {
        alert("Falha na conexão com o servidor: " + erro.message);
    }
}

/* Formata número como moeda brasileira */
function fmt(valor) {
    return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}