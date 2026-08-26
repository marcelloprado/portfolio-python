// Comportamentos compartilhados por todas as páginas.

document.addEventListener("DOMContentLoaded", () => {
  ativarTooltips();
  ativarRevelacao();
});

/**
 * Liga os tooltips do Bootstrap em todo elemento marcado com data-bs-toggle.
 * (Antes existia um tooltip.js que nunca chegava a ser carregado no layout.)
 */
function ativarTooltips() {
  if (typeof bootstrap === "undefined") return;

  document
    .querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach((elemento) => new bootstrap.Tooltip(elemento));
}

/**
 * Revela os elementos [data-reveal] conforme entram na tela.
 * Sem IntersectionObserver, tudo aparece de imediato.
 */
function ativarRevelacao() {
  const alvos = document.querySelectorAll("[data-reveal]");
  if (!alvos.length) return;

  if (!("IntersectionObserver" in window)) {
    alvos.forEach((alvo) => alvo.classList.add("is-visible"));
    return;
  }

  const observador = new IntersectionObserver(
    (entradas) => {
      entradas.forEach((entrada) => {
        if (!entrada.isIntersecting) return;
        entrada.target.classList.add("is-visible");
        observador.unobserve(entrada.target);
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  alvos.forEach((alvo) => observador.observe(alvo));
}