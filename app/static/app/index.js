// DOM Content Loaded - Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar AOS (Animate On Scroll)
    AOS.init({
        duration: 800,
        easing: 'ease-out-cubic',
        once: true,
        offset: 100,
        delay: 100
    });

    // Inicializar funcionalidades
    initNavbar();
    initSmoothScroll();
    initTypewriter();
    initParallax();
    initCounters();
    initLazyLoading();
    initContactForm();

    // Inicializar Swiper cuando esté disponible
    if (typeof Swiper !== 'undefined') {
        initProjectsSwiper();
    } else {
        // Esperar a que Swiper se cargue
        setTimeout(function() {
            if (typeof Swiper !== 'undefined') {
                initProjectsSwiper();
            }
        }, 200);
    }

    // Preloader (opcional)
    hidePreloader();
});

// NAVBAR SCROLL EFFECT
function initNavbar() {
    const navbar = document.getElementById('mainNavbar');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    // Efecto de scroll en navbar
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Highlight active section en navbar
        highlightActiveSection();
    });

    // Cerrar navbar móvil al hacer click en enlace
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            const navbarCollapse = document.querySelector('.navbar-collapse');
            if (navbarCollapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                bsCollapse.hide();
            }
        });
    });
}

// SMOOTH SCROLL
function initSmoothScroll() {
    const smoothScrollLinks = document.querySelectorAll('.smooth-scroll');

    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80; // Ajuste para navbar fijo

                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// HIGHLIGHT ACTIVE SECTION
function highlightActiveSection() {
    const sections = document.querySelectorAll('section[id], header[id]');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    let currentSection = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 120;
        const sectionHeight = section.offsetHeight;

        if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + currentSection) {
            link.classList.add('active');
        }
    });
}

// TYPEWRITER EFFECT PARA EL HERO
function initTypewriter() {
    const heroSubtitle = document.querySelector('.hero-subtitle');
    if (!heroSubtitle) return;

    const text = heroSubtitle.textContent;
    heroSubtitle.textContent = '';

    let i = 0;
    const typeSpeed = 50;

    setTimeout(() => {
        function typeWriter() {
            if (i < text.length) {
                heroSubtitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, typeSpeed);
            }
        }
        typeWriter();
    }, 1000);
}

// PARALLAX EFFECT
function initParallax() {
    const parallaxElements = document.querySelectorAll('.hero-section, .value-card, .service-card');

    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.05;

        // Efecto parallax en hero
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            heroSection.style.transform = `translateY(${rate}px)`;
        }
    });
}

// CONTADOR ANIMADO
function initCounters() {
    const counters = document.querySelectorAll('[data-count]');
    const speed = 200;

    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-count'));
                const count = parseInt(counter.innerText);
                const increment = target / speed;

                if (count < target) {
                    counter.innerText = Math.ceil(count + increment);
                    setTimeout(() => {
                        observer.observe(counter);
                    }, 1);
                } else {
                    counter.innerText = target;
                }

                observer.unobserve(counter);
            }
        });
    }, observerOptions);

    counters.forEach(counter => {
        observer.observe(counter);
    });
}

// LAZY LOADING PARA IMÁGENES
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => {
        imageObserver.observe(img);
    });
}

// FORMULARIO DE CONTACTO (Funcionalidad básica)
function initContactForm() {
    const contactForms = document.querySelectorAll('form[data-contact]');

    contactForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // Aquí puedes agregar la lógica para enviar el formulario
            // Por ejemplo, usando fetch() para enviar a tu backend Django

            showNotification('Mensaje enviado correctamente', 'success');
        });
    });
}

// INICIALIZACIÓN DE SWIPER PARA PROYECTOS
function initProjectsSwiper() {
    const swiperElement = document.querySelector('.projects-swiper');
    
    if (!swiperElement) {
        console.log('Projects swiper element not found');
        return;
    }

    try {
        const swiper = new Swiper('.projects-swiper', {
            // Slides por vista según pantalla
            slidesPerView: 1,
            spaceBetween: 20,
            
            // Responsive breakpoints
            breakpoints: {
                576: {
                    slidesPerView: 2,
                    spaceBetween: 20
                },
                768: {
                    slidesPerView: 3,
                    spaceBetween: 25
                },
                992: {
                    slidesPerView: 4,
                    spaceBetween: 30
                }
            },
            
            // Navigation
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            
            // Pagination
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
                dynamicBullets: true
            },
            
            // Auto height
            autoHeight: false,
            
            // Loop si hay suficientes slides
            loop: false,
            
            // Centrar slides incompletas
            centeredSlides: false,
            
            // Efecto de transición
            effect: 'slide',
            speed: 500,
            
            // Touch/swipe
            touchRatio: 1,
            touchAngle: 45,
            grabCursor: true,
            
            // Lazy loading
            lazy: {
                loadPrevNext: true,
                loadOnTransitionStart: false,
            },
            
            // A11y
            a11y: {
                enabled: true,
                nextSlideMessage: 'Siguiente proyecto',
                prevSlideMessage: 'Proyecto anterior',
                firstSlideMessage: 'Este es el primer proyecto',
                lastSlideMessage: 'Este es el último proyecto'
            },
            
            // Keyboard control
            keyboard: {
                enabled: true,
                onlyInViewport: true,
            },
            
            // Mouse wheel
            mousewheel: {
                enabled: false,
            },
            
            // Autoplay (opcional - descomentad para activar)
            /*
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
                pauseOnMouseEnter: true
            },
            */
            
            // Callbacks
            on: {
                init: function() {
                    console.log('Swiper initialized successfully');
                },
                slideChange: function() {
                    // Se ejecuta cuando cambia de slide
                }
            }
        });
        
        // Guardar referencia para uso posterior si es necesario
        window.projectsSwiper = swiper;
        
    } catch (error) {
        console.error('Error initializing Swiper:', error);
    }
}

// SISTEMA DE NOTIFICACIONES
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)} me-2"></i>
            ${message}
            <button class="notification-close">&times;</button>
        </div>
    `;

    document.body.appendChild(notification);

    // Mostrar notificación
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    // Auto-hide después de 5 segundos
    setTimeout(() => {
        hideNotification(notification);
    }, 5000);

    // Cerrar al hacer click
    notification.querySelector('.notification-close').addEventListener('click', () => {
        hideNotification(notification);
    });
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function hideNotification(notification) {
    notification.classList.remove('show');
    setTimeout(() => {
        notification.remove();
    }, 300);
}

// PRELOADER
function hidePreloader() {
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        setTimeout(() => {
            preloader.classList.add('fade-out');
            setTimeout(() => {
                preloader.remove();
            }, 500);
        }, 1000);
    }
}

// ANIMACIONES DE HOVER PARA TARJETAS
function initCardAnimations() {
    const cards = document.querySelectorAll('.value-card, .service-card, .project-card, .company-card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// EFECTO DE TYPING EN MÚLTIPLES ELEMENTOS
function initMultipleTypewriter() {
    const typewriterElements = document.querySelectorAll('[data-typewriter]');

    typewriterElements.forEach((element, index) => {
        const text = element.textContent;
        const speed = parseInt(element.dataset.speed) || 50;
        const delay = parseInt(element.dataset.delay) || 0;

        element.textContent = '';

        setTimeout(() => {
            typeWriter(element, text, speed);
        }, delay + (index * 500));
    });
}

function typeWriter(element, text, speed) {
    let i = 0;
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

// INTERSECTION OBSERVER PARA ANIMACIONES
function initIntersectionAnimations() {
    const animatedElements = document.querySelectorAll('[data-animate]');

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const animation = element.dataset.animate;
                element.classList.add('animate__animated', `animate__${animation}`);
                observer.unobserve(element);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// PERFORMANCE OPTIMIZATION
function optimizePerformance() {
    // Debounce para resize y scroll
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            AOS.refresh();
            
            // Reinicializar Swiper si existe
            if (window.projectsSwiper) {
                window.projectsSwiper.update();
            }
        }, 250);
    });

    // Lazy load para elementos pesados
    const heavyElements = document.querySelectorAll('[data-heavy]');
    const heavyObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                loadHeavyContent(entry.target);
                heavyObserver.unobserve(entry.target);
            }
        });
    });

    heavyElements.forEach(element => {
        heavyObserver.observe(element);
    });
}

function loadHeavyContent(element) {
    // Cargar contenido pesado cuando sea necesario
    const contentType = element.dataset.heavy;

    switch(contentType) {
        case 'map':
            loadMap(element);
            break;
        case 'video':
            loadVideo(element);
            break;
        default:
            console.log('Cargando contenido pesado:', contentType);
    }
}

// INIT FINAL
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todas las funcionalidades adicionales
    initCardAnimations();
    initIntersectionAnimations();
    optimizePerformance();

    console.log('SPA Aluminios del Sureste cargada correctamente');
});