// Página /certificados: busca por título e visualizador em tela cheia.

document.addEventListener("DOMContentLoaded", () => {
  ativarBusca();
  ativarLightbox();
});

/** Filtra a grade conforme o usuário digita, comparando com o título do certificado. */
function ativarBusca() {
  const campo = document.getElementById("busca-certificado");
  const itens = document.querySelectorAll(".certificado-item");
  const semResultado = document.getElementById("sem-certificado");

  if (!campo || !itens.length) return;

  campo.addEventListener("input", () => {
    const termo = campo.value.trim().toLowerCase();
    let visiveis = 0;

    itens.forEach((item) => {
      const titulo = (item.dataset.titulo || "").toLowerCase();
      const combina = !termo || titulo.includes(termo);

      item.classList.toggle("is-hidden", !combina);
      if (combina) visiveis += 1;
    });

    if (semResultado) semResultado.hidden = visiveis > 0;
  });
}

/** Abre o certificado em tela cheia ao clicar, com navegação por teclado. */
function ativarLightbox() {
  const lightbox = document.getElementById("lightbox");
  const imagem = document.getElementById("lightbox-img");
  const legenda = document.getElementById("lightbox-legenda");
  const botaoFechar = lightbox && lightbox.querySelector(".lightbox-fechar");
  const itens = document.querySelectorAll(".certificado-item");

  if (!lightbox || !imagem || !itens.length) return;

  // Guarda quem abriu o visualizador, para devolver o foco ao fechar.
  let gatilhoAnterior = null;

  function abrir(item) {
    gatilhoAnterior = item;
    imagem.src = item.dataset.imagem;
    imagem.alt = "Certificado: " + item.dataset.titulo;
    legenda.textContent = item.dataset.titulo;
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
    if (botaoFechar) botaoFechar.focus();
  }

  function fechar() {
    lightbox.hidden = true;
    imagem.src = "";
    document.body.style.overflow = "";
    if (gatilhoAnterior) gatilhoAnterior.focus();
  }

  itens.forEach((item) => item.addEventListener("click", () => abrir(item)));

  if (botaoFechar) botaoFechar.addEventListener("click", fechar);

  // Clique fora da imagem também fecha.
  lightbox.addEventListener("click", (evento) => {
    if (evento.target === lightbox) fechar();
  });

  document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape" && !lightbox.hidden) fechar();
  });
}
