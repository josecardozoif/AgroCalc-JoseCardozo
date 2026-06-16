/* Controle de abas */
function trocarAba(id, btn) {
    /* Remove o ''.ativo' de todos os painéis e botões */
    document.querySelectorAll(".painel-aba").forEach(p => p.classList.remove("ativo"));
    document.querySelectorAll(".aba-btn").forEach(b => b.classList.remove("ativa"));

    document.getElementById("painel-" + id).classList.add("ativo");
    btn.classList.add("ativa");
}

/* Lê o valor e a base de origem, converte para decimal usando parseInt(), depois formata para binário e hexa.*/
function converterNumero() {
    const valor = document.getElementById("valor-numero").value.trim().toUpperCase();
    const base = parseInt(document.getElementById("base-origem").value);

    if (!valor) { alert("Digite um valor para converter."); return; }

    /* parseInt(valor, base) converte qualquer base para decimal */
    const decimal = parseInt(valor, base);

    if (isNaN(decimal)) {
        alert(`Valor inválido para a base ${base}. Verifique os dígitos digitados.`);
        return;
    }

    /* Converte decimal para as outras bases */
    document.getElementById("res-decimal").textContent = decimal.toString(10);
    document.getElementById("res-binario").textContent = decimal.toString(2);
    document.getElementById("res-hex").textContent = decimal.toString(16).toUpperCase();

    document.getElementById("resultado-bases").style.display = "grid";
}

/*
 Aplica os 'AND, OR e NOT' por bit a bit sobre dois números decimais
 NOT usa máscara de 8 bits (~A & 0xFF) para resultado legível
*/
function calcularLogica() {
    const A = parseInt(document.getElementById("logica-a").value) || 0;
    const B = parseInt(document.getElementById("logica-b").value) || 0;

    /* Operações lógicas bit a bit */
    const ops = [
        { nome: `A AND B  (${A} & ${B})`, valor: A & B },
        { nome: `A OR B   (${A} | ${B})`, valor: A | B },
        { nome: `NOT A    (~${A})`, valor: ~A & 0xFF }, /* Máscara 8 bits */
    ];

    const tbody = document.getElementById("corpo-logica");
    tbody.innerHTML = "";

    ops.forEach(op => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td style="text-align:left;">${op.nome}</td>
          <td>${op.valor}</td>
          <td>${op.valor.toString(2).padStart(8, "0")}</td>
          <td>${op.valor.toString(16).toUpperCase()}</td>
        `;
        tbody.appendChild(tr);
    });

    document.getElementById("tabela-logica").style.display = "table";
}

/*
 Multiplica comprimento × largura e converte para hectares
 1 ha = 10.000 m²
*/
function calcularArea() {
    const comp = parseFloat(document.getElementById("comprimento").value) || 0;
    const larg = parseFloat(document.getElementById("largura").value) || 0;

    if (comp <= 0 || larg <= 0) {
        alert("Informe comprimento e largura maiores que zero.");
        return;
    }

    const m2 = comp * larg;
    const ha = m2 / 10000;

    document.getElementById("area-ha").textContent = `${ha.toLocaleString("pt-BR", { maximumFractionDigits: 4 })} ha`;
    document.getElementById("area-m2").textContent = `${m2.toLocaleString("pt-BR")} m²`;
    document.getElementById("resultado-area").style.display = "block";
}
