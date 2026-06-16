/*
 det3x3(m)
 Calcula o determinante de uma matriz 3×3 pela Regra de Sarrus.
 m é um array de 3 linhas × 3 colunas: m[linha][coluna]
 
|a b c|
|d e f|  →  det = a(ei−fh) − b(di−fg) + c(dh−eg)
|g h i|
 */
function det3x3(m) {
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
        m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
        m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    );
}

/*
 substituirColuna(matriz, coluna, vetor)
 Retorna nova matriz com a coluna substituída pelo vetor.
 Usado na Regra de Cramer para resolver o sistema.
*/
function substituirColuna(matriz, coluna, vetor) {
    return matriz.map((linha, i) =>
        linha.map((val, j) => (j === coluna ? vetor[i] : val))
    );
}

/*
 Monta a matriz de coeficientes A (composição das fontes em decimal) e o vetor b (alvo NPK), depois aplica Regra de Cramer:
   x1 = det(A1)/det(A)
   x2 = det(A2)/det(A)
   x3 = det(A3)/det(A)
 Cada xi representa quantos kg da fonte i usar por hectare.
*/
function resolverBlend() {
    /* Leitura das fontes (converte % para decimal: /100) */
    const nomes = [
        document.getElementById("f1-nome").value || "Fonte 1",
        document.getElementById("f2-nome").value || "Fonte 2",
        document.getElementById("f3-nome").value || "Fonte 3",
    ];

    /* Matriz A: cada coluna é a composição de uma fonte */
    const A = [
        [parseFloat(document.getElementById("f1-n").value) / 100,
        parseFloat(document.getElementById("f2-n").value) / 100,
        parseFloat(document.getElementById("f3-n").value) / 100], /* linha N */

        [parseFloat(document.getElementById("f1-p").value) / 100,
        parseFloat(document.getElementById("f2-p").value) / 100,
        parseFloat(document.getElementById("f3-p").value) / 100], /* linha P */

        [parseFloat(document.getElementById("f1-k").value) / 100,
        parseFloat(document.getElementById("f2-k").value) / 100,
        parseFloat(document.getElementById("f3-k").value) / 100], /* linha K */
    ];

    /* Vetor b: alvo NPK */
    const b = [
        parseFloat(document.getElementById("alvo-n").value) || 0,
        parseFloat(document.getElementById("alvo-p").value) || 0,
        parseFloat(document.getElementById("alvo-k").value) || 0,
    ];

    const detA = det3x3(A);
    const el = document.getElementById("resultado");

    /* Verifica se o sistema tem solução única (det ≠ 0) */
    if (Math.abs(detA) < 1e-10) {
        el.innerHTML = `
          <div class="aviso-erro">
            <strong>Sistema sem solução única (det = 0)</strong><br>
            As composições das fontes informadas são linearmente dependentes —
            não é possível atingir o alvo NPK com essa combinação.
            Tente usar fontes com composições diferentes.
          </div>`;
        el.style.display = "block";
        return;
    }

    /* Regra de Cramer: x_i = det(A_i) / det(A) */
    const x1 = det3x3(substituirColuna(A, 0, b)) / detA;
    const x2 = det3x3(substituirColuna(A, 1, b)) / detA;
    const x3 = det3x3(substituirColuna(A, 2, b)) / detA;

    /* Verifica se alguma quantidade é negativa (solução inviável) */
    const invalido = [x1, x2, x3].some(v => v < -0.01);

    el.innerHTML = `
        <div class="card">
          <h2 style="margin-bottom:1rem;">Blend calculado</h2>

          <div class="resultado-blend">
            <div class="blend-item">
              <span class="blend-kg">${x1.toFixed(1)} kg</span>
              <span class="blend-label">${nomes[0]}</span>
            </div>
            <div class="blend-item">
              <span class="blend-kg">${x2.toFixed(1)} kg</span>
              <span class="blend-label">${nomes[1]}</span>
            </div>
            <div class="blend-item">
              <span class="blend-kg">${x3.toFixed(1)} kg</span>
              <span class="blend-label">${nomes[2]}</span>
            </div>
          </div>

          ${invalido ? `
            <div class="aviso-erro" style="margin-top:1rem;">
              Uma ou mais quantidades resultaram negativas, o que indica que
              o alvo NPK informado não é atingível com essas fontes nas proporções calculadas.
            </div>` : ""}

          <div class="detalhe-matematico">
            <strong>Detalhes matemáticos (Regra de Cramer)</strong><br><br>
            Matriz de coeficientes A (composição em decimal):<br>
            | N: ${A[0].map(v => (v * 100).toFixed(1) + "%").join("  ")} |<br>
            | P: ${A[1].map(v => (v * 100).toFixed(1) + "%").join("  ")} |<br>
            | K: ${A[2].map(v => (v * 100).toFixed(1) + "%").join("  ")} |<br><br>
            Vetor b (alvo):  N=${b[0]} kg  P=${b[1]} kg  K=${b[2]} kg<br><br>
            det(A) = ${detA.toFixed(6)}  →  Sistema com <strong>solução única ✓</strong><br><br>
            x₁ = ${x1.toFixed(2)} kg  |  x₂ = ${x2.toFixed(2)} kg  |  x₃ = ${x3.toFixed(2)} kg
          </div>
        </div>`;

    el.style.display = "block";
    el.scrollIntoView({ behavior: "smooth" });
}