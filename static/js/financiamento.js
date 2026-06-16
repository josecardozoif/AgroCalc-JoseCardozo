/*
    Aplica a fórmula Price (juros compostos) para calcular as parcelas e monta a tabela de amortização completa.
    Fórmula da parcela:
     PMT = PV × [i × (1+i)^n] / [(1+i)^n − 1]
     
    Onde:
     PV = valor presente (financiado após entrada)
     i  = taxa de juros mensal (decimal)
     n  = número de parcelas
*/

function calcularFinanciamento() {
    /* Leitura dos campos */
    const valorTotal = parseFloat(document.getElementById("valor-total").value) || 0;
    const taxaMensal = parseFloat(document.getElementById("taxa-juros").value) || 0;
    const nParcelas = parseInt(document.getElementById("num-parcelas").value) || 0;
    const entrada = parseFloat(document.getElementById("entrada").value) || 0;

    /* Validação básica */
    if (valorTotal <= 0 || taxaMensal <= 0 || nParcelas <= 0) {
        alert("Preencha todos os campos obrigatórios com valores válidos.");
        return;
    }
    if (entrada >= valorTotal) {
        alert("A entrada não pode ser maior ou igual ao valor financiado.");
        return;
    }

    const PV = valorTotal - entrada; /* Valor presente (financiado) */
    const i = taxaMensal / 100; /* Taxa em decimal */

    /* Cálculo da parcela fixa (fórmula Price) */
    const fator = Math.pow(1 + i, nParcelas);
    const PMT = PV * (i * fator) / (fator - 1);

    /* Monta a tabela de amortização mês a mês */
    let saldo = PV;
    let totalJuros = 0;
    const tbody = document.getElementById("corpo-tabela");
    tbody.innerHTML = "";

    for (let mes = 1; mes <= nParcelas; mes++) {
        const jurosMes = saldo * i; /* Juros do mês */
        const amort = PMT - jurosMes; /* Amortização do mês */
        saldo -= amort; /* Saldo devedor restante */
        totalJuros += jurosMes;

        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${mes}</td>
          <td>${fmt(PMT)}</td>
          <td>${fmt(jurosMes)}</td>
          <td>${fmt(amort)}</td>
          <td>${fmt(Math.max(saldo, 0))}</td>
        `;
        tbody.appendChild(tr);
    }

    /* Preenche os cards de resumo */
    document.getElementById("res-parcela").textContent = fmt(PMT);
    document.getElementById("res-total").textContent = fmt(PMT * nParcelas + entrada);
    document.getElementById("res-juros").textContent = fmt(totalJuros);

    /* Exibe o bloco de resultado */
    document.getElementById("resultado").style.display = "block";
    document.getElementById("resultado").scrollIntoView({ behavior: "smooth" });
}

/* Formata número como moeda brasileira */
function fmt(valor) {
    return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}