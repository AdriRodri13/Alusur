document.addEventListener("DOMContentLoaded", () => {
    const navToggle = document.querySelector(".nav-toggle");
    const navMenu = document.querySelector(".nav-menu");

    navToggle.addEventListener("click", () => {
        navMenu.classList.toggle("active");
    });

    // Cerrar menú al hacer click en un enlace
    document.querySelectorAll(".nav-menu-link").forEach(n => n.addEventListener("click", () => {
        navMenu.classList.remove("active");
    }));
});