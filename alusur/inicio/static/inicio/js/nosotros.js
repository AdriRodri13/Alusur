document.addEventListener('DOMContentLoaded', function() {
    // Funciones para animaciones de scroll
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    function handleScrollAnimations() {
        // Animaciones fade-in
        document.querySelectorAll('.fade-in').forEach(element => {
            if (isElementInViewport(element)) {
                element.classList.add('visible');
            }
        });

        // Animaciones slide-in
        document.querySelectorAll('.slide-in-left, .slide-in-right').forEach(element => {
            if (isElementInViewport(element)) {
                element.classList.add('visible');
            }
        });
    }

    // Slider de instalaciones
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;

    function showSlide(index) {
        // Ocultar todas las slides
        slides.forEach(slide => {
            slide.style.display = 'none';
        });

        // Mostrar la slide actual
        slides[index].style.display = 'block';
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        showSlide(currentSlide);
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        showSlide(currentSlide);
    }

    // Event listeners para los botones del slider
    const nextButton = document.querySelector('.next-slide');
    const prevButton = document.querySelector('.prev-slide');

    if (nextButton && prevButton) {
        nextButton.addEventListener('click', nextSlide);
        prevButton.addEventListener('click', prevSlide);
    }

    // Inicializar el slider
    showSlide(currentSlide);

    // Cambiar slide automáticamente cada 5 segundos
    setInterval(nextSlide, 5000);

    // Event listener para las animaciones de scroll
    window.addEventListener('scroll', handleScrollAnimations);
    
    // Ejecutar las animaciones al cargar la página
    handleScrollAnimations();

    // Animación suave para los miembros del equipo
    const miembros = document.querySelectorAll('.miembro-card');
    miembros.forEach((miembro, index) => {
        miembro.style.opacity = '0';
        miembro.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            miembro.style.transition = 'all 0.6s ease';
            miembro.style.opacity = '1';
            miembro.style.transform = 'translateY(0)';
        }, 200 * index); // Retraso escalonado para cada miembro
    });
});