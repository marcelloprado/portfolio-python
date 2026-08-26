// Página /projetos: filtro por tecnologia e preview animado nos cartões.

document.addEventListener("DOMContentLoaded", () => {
  ativarFiltros();
  ativarPreviewAnimado();
});

/**
 * Filtra a grade pelos botões de tecnologia. O filtro fica na URL
 * (?tec=Python), então o estado sobrevive a recarregar ou compartilhar o link.
 */
function ativarFiltros() {
  const botoes = document.querySelectorAll(".filtro-btn");
  const cartoes = document.querySelectorAll(".projeto-card");
  const semResultado = document.getElementById("sem-resultado");

  if (!botoes.length || !cartoes.length) return;

  function aplicar(filtro) {
    let visiveis = 0;

    cartoes.forEach((cartao) => {
      const tecnologias = (cartao.dataset.tecnologias || "").split("|");
      const combina = filtro === "todos" || tecnologias.includes(filtro);

      cartao.classList.toggle("is-hidden", !combina);
      if (combina) visiveis += 1;
    });

    botoes.forEach((botao) => {
      const ativo = botao.dataset.filtro === filtro;
      botao.classList.toggle("is-active", ativo);
      botao.setAttribute("aria-pressed", String(ativo));
    });

    if (semResultado) semResultado.hidden = visiveis > 0;
  }

  botoes.forEach((botao) => {
    botao.addEventListener("click", () => {
      const filtro = botao.dataset.filtro;
      aplicar(filtro);

      const url = new URL(window.location.href);
      if (filtro === "todos") {
        url.searchParams.delete("tec");
      } else {
        url.searchParams.set("tec", filtro);
      }
      window.history.replaceState({}, "", url);
    });
  });

  // Restaura o filtro vindo da URL, se ele existir entre os botões.
  const filtroInicial = new URLSearchParams(window.location.search).get("tec");
  const existe = [...botoes].some((botao) => botao.dataset.filtro === filtroInicial);
  aplicar(existe ? filtroInicial : "todos");
}

/**
 * Troca a capa pelo GIF do projeto quando o cartão recebe o cursor ou o foco.
 * O GIF só é baixado no primeiro hover — carregar os oito de uma vez
 * custaria vários megabytes no carregamento da página.
 */
function ativarPreviewAnimado() {
  // Em telas de toque não existe hover: o GIF nunca apareceria e o download seria desperdiçado.
  if (window.matchMedia("(hover: none)").matches) return;

  document.querySelectorAll(".projeto-card").forEach((cartao) => {
    const gif = cartao.querySelector(".thumb-gif[data-gif]");
    if (!gif) return;

    const carregar = () => {
      if (gif.dataset.carregado) return;
      gif.dataset.carregado = "true";
      gif.src = gif.dataset.gif;
      gif.addEventListener("load", () => gif.classList.add("is-ready"), { once: true });
    };

    cartao.addEventListener("mouseenter", carregar, { once: true });
    cartao.addEventListener("focusin", carregar, { once: true });
  });
}