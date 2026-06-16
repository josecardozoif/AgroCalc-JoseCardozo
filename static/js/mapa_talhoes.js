/* Letras para nomear as linhas (setores) */
const LETRAS = "ABCDEFGH";
let nLin = 3, nCol = 4;

/*
  Cria uma grade de <input> com base nas dimensões escolhidas.
  Cada input representa um talhão da matriz.
*/
function gerarInputs() {
    nLin = parseInt(document.getElementById("num-linhas").value) || 3;
    nCol = parseInt(document.getElementById("num-colunas").value) || 4;

    const grade = document.getElementById("grade-inputs");

    /* CSS grid dinâmico: 1 col de rótulo + nCol colunas de dados */
    grade.style.gridTemplateColumns = `60px repeat(${nCol}, 1fr)`;

    grade.innerHTML = "";

    /* Cabeçalho da grade de inputs */
    grade.innerHTML += `<div></div>`; /* célula vazia no canto */
    for (let c = 1; c <= nCol; c++) {
        grade.innerHTML += `<div style="text-align:center;font-weight:700;font-size:.85rem;color:var(--cor-texto-suave);">Col ${c}</div>`;
    }

    /* Linhas com rótulo + inputs */
    for (let l = 0; l < nLin; l++) {
        grade.innerHTML += `<div style="display:flex;align-items:center;font-weight:700;color:var(--cor-primaria);">Setor ${LETRAS[l]}</div>`;
        for (let c = 0; c < nCol; c++) {
            grade.innerHTML += `<input class="celula-input" type="number" id="cel-${l}-${c}" placeholder="0" min="0" step="0.1">`;
        }
    }

    document.getElementById("secao-inputs").style.display = "block";
    document.getElementById("resultado").style.display = "none";
}

/*
  Lê os valores dos inputs, monta a matriz, aplica cores de calor com base em percentis (baixo/médio/alto) e calcula estatísticas.
*/
function gerarMapa() {
    const unidade = document.getElementById("unidade").value || "sc/ha";
    const valores = [];
    const todos = [];

    /* Lê todos os valores e monta matriz bidimensional */
    for (let l = 0; l < nLin; l++) {
        const linha = [];
        for (let c = 0; c < nCol; c++) {
            const v = parseFloat(document.getElementById(`cel-${l}-${c}`).value) || 0;
            linha.push(v);
            todos.push(v);
        }
        valores.push(linha);
    }

    /* Calcula min e max para determinar cor de calor */
    const minVal = Math.min(...todos);
    const maxVal = Math.max(...todos);
    const range = maxVal - minVal || 1;

    /*
      classeCalor(v): retorna a classe CSS de cor conforme posição no intervalo
      Baixo: < 33% | Médio: 33-66% | Alto: > 66%
    */
    function classeCalor(v) {
        const pct = (v - minVal) / range;
        if (pct < 0.33) return "calor-baixo";
        if (pct < 0.66) return "calor-medio";
        return "calor-alto";
    }

    /* Monta a tabela HTML */
    const tabela = document.getElementById("tabela-mapa");
    tabela.innerHTML = "";

    /* Cabeçalho da tabela */
    let thead = `<thead><tr><th>Setor</th>`;
    for (let c = 1; c <= nCol; c++) thead += `<th>Col ${c}</th>`;
    thead += `<th>Média (${unidade})</th></tr></thead>`;
    tabela.innerHTML = thead;

    /* Corpo da tabela com mapa de calor */
    let tbody = "<tbody>";
    valores.forEach((linha, l) => {
        const mediLinha = linha.reduce((a, b) => a + b, 0) / linha.length;
        tbody += `<tr><td class="setor-label">Setor ${LETRAS[l]}</td>`;
        linha.forEach(v => {
            tbody += `<td class="${classeCalor(v)}">${v.toLocaleString("pt-BR")} ${unidade}</td>`;
        });
        tbody += `<td style="font-weight:600;">${mediLinha.toFixed(1)} ${unidade}</td></tr>`;
    });
    tbody += "</tbody>";
    tabela.innerHTML += tbody;

    /* Estatísticas gerais */
    const soma = todos.reduce((a, b) => a + b, 0);
    const media = soma / todos.length;
    const statsEl = document.getElementById("stats-grid");
    statsEl.innerHTML = `
        <div class="stat-card">
          <div class="stat-valor">${media.toFixed(1)}</div>
          <div class="stat-label">Média geral (${unidade})</div>
        </div>
        <div class="stat-card">
          <div class="stat-valor">${maxVal.toLocaleString("pt-BR")}</div>
          <div class="stat-label">Maior produtividade</div>
        </div>
        <div class="stat-card">
          <div class="stat-valor">${minVal.toLocaleString("pt-BR")}</div>
          <div class="stat-label">Menor produtividade</div>
        </div>
        <div class="stat-card">
          <div class="stat-valor">${todos.length}</div>
          <div class="stat-label">Total de talhões</div>
        </div>
      `;

    document.getElementById("resultado").style.display = "block";
    document.getElementById("resultado").scrollIntoView({ behavior: "smooth" });
}

/* Gera grade inicial ao carregar a página */
window.addEventListener("DOMContentLoaded", gerarInputs);