// Menu Hamburger - Funcionalidade responsiva

document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.querySelector(".hamburger");
  const navMenu = document.querySelector("nav ul");

  if (!hamburger || !navMenu) return;

  function fechar() {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
    hamburger.setAttribute("aria-expanded", "false");
    hamburger.setAttribute("aria-label", "Abrir menu");
  }

  function alternar() {
    const aberto = hamburger.classList.toggle("active");
    navMenu.classList.toggle("active", aberto);
    hamburger.setAttribute("aria-expanded", String(aberto));
    hamburger.setAttribute("aria-label", aberto ? "Fechar menu" : "Abrir menu");
  }

  hamburger.addEventListener("click", alternar);

  // Fechar ao clicar em um link do menu
  navMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", fechar);
  });

  // Fechar ao clicar fora do menu
  document.addEventListener("click", function (evento) {
    const dentroDoMenu = navMenu.contains(evento.target);
    const noHamburger = hamburger.contains(evento.target);

    if (!dentroDoMenu && !noHamburger && hamburger.classList.contains("active")) {
      fechar();
    }
  });

  // Fechar com a tecla Esc
  document.addEventListener("keydown", function (evento) {
    if (evento.key === "Escape") fechar();
  });
});