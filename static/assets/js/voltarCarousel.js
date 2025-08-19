document.addEventListener("DOMContentLoaded", function () {
  const params = new URLSearchParams(window.location.search);
  const projectId = params.get("id"); // pega o id pela URL

  if (projectId) {
    const carousel = document.querySelector('#carrosselProjetos'); // ajuste o id do seu carrossel
    if (carousel) {
      const carouselInstance = new bootstrap.Carousel(carousel);
      const targetIndex = parseInt(projectId) - 1; // se o id for sequencial
      carouselInstance.to(targetIndex);
    }
  }
});