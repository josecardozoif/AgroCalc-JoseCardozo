/*
   nav.js — AgroCalc
   Injeta o header (com nav) e o footer em todas as páginas.
   Cada página deve ter:
     - <div id="site-header"></div>
     - <div id="site-footer"></div>
     - <body data-page="NOME_DA_PAGINA">
*/

const NAV_LINKS = [
  { id: "index", href: "/", label: "Painel" },
  { id: "custo", href: "/custo", label: "Custo" },
  { id: "financiamento", href: "/financiamento", label: "Financiamento" },
  { id: "conversor", href: "/conversor", label: "Conversor" },
  { id: "mapa_talhoes", href: "/mapa-talhoes", label: "Talhões" },
  { id: "blend", href: "/blend", label: "Blend NPK" },
  { id: "como_funciona", href: "/como-funciona", label: "Como Funciona" },
];

/* Detecta a página atual pelo atributo data-page do <body> */
const paginaAtual = document.body.dataset.page || "";

/* Monta o HTML do header + nav */
function montarHeader() {
  const itensNav = NAV_LINKS.map(link => {
    const ativo = link.id === paginaAtual ? ' class="ativo"' : "";
    return `<li><a href="${link.href}"${ativo}>${link.label}</a></li>`;
  }).join("\n        ");

  return `
  <header class="site-header">
    <div class="header-inner">
      <div class="logo">
        <span class="logo-texto">AgroCalc</span>
      </div>

      <button id="btn-menu" class="btn-menu" aria-label="Abrir menu">
        <span></span><span></span><span></span>
      </button>

      <nav id="nav-principal" class="nav-principal" aria-label="Navegação principal">
        <ul>
        ${itensNav}
        </ul>
      </nav>

      <button id="btn-dark" class="btn-dark" aria-label="Alternar modo escuro">🌙</button>
    </div>
  </header>`;
}

/* Monta o HTML do footer */
function montarFooter() {
  const ano = new Date().getFullYear();
  return `
  <footer class="site-footer">
    <p>AgroCalc &copy; ${ano} — Projeto Integrador</p>
    <p class="footer-sub">LAEC · ITC · Matemática Aplicada</p>
  </footer>`;
}

/* Injeta header e footer e ativa os eventos */
document.addEventListener("DOMContentLoaded", () => {
  const elHeader = document.getElementById("site-header");
  const elFooter = document.getElementById("site-footer");

  if (elHeader) elHeader.innerHTML = montarHeader();
  if (elFooter) elFooter.innerHTML = montarFooter();

  /* Hambúrguer: abre/fecha nav no mobile */
  const btnMenu = document.getElementById("btn-menu");
  const nav = document.getElementById("nav-principal");

  if (btnMenu && nav) {
    btnMenu.addEventListener("click", () => {
      const aberto = nav.classList.toggle("aberto");
      btnMenu.setAttribute("aria-expanded", aberto);
    });
  }

  /* Dark Mode: alterna classe e salva preferência */
  const btnDark = document.getElementById("btn-dark");

  if (localStorage.getItem("tema") === "escuro") {
    document.body.classList.add("dark");
    if (btnDark) btnDark.innerHTML = '<i class="bi bi-sun-fill"></i>';
  }

  if (btnDark) {
    btnDark.addEventListener("click", () => {
      const escuro = document.body.classList.toggle("dark");
      btnDark.innerHTML = escuro
        ? '<i class="bi bi-sun-fill"></i>'
        : '<i class="bi bi-moon-fill"></i>';
      localStorage.setItem("tema", escuro ? "escuro" : "claro");
    });
  }
});