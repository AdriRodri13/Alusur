/**
 * Blog Preview JavaScript
 * Funcionalidad específica para la vista previa del blog en la SPA principal
 */

class BlogPreview {
    constructor() {
        this.container = document.querySelector('.blog-preview-section');
        if (this.container) {
            this.init();
        }
    }

    init() {
        this.setupAnimations();
        this.bindEvents();
        this.initializeCards();
    }

    setupAnimations() {
        // Configurar animaciones específicas para la vista previa
        const cards = this.container.querySelectorAll('.blog-preview-card');
        
        // Observer para animaciones de entrada
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('animate-in');
                    }, index * 100); // Stagger animation
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px'
        });

        cards.forEach(card => observer.observe(card));
    }

    bindEvents() {
        // Eventos específicos para la vista previa
        this.bindCardHoverEffects();
        this.bindViewAllButton();
        this.bindCardClickTracking();
    }

    bindCardHoverEffects() {
        const cards = this.container.querySelectorAll('.blog-preview-card');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                this.animateCardHover(card, true);
            });
            
            card.addEventListener('mouseleave', () => {
                this.animateCardHover(card, false);
            });
        });
    }

    animateCardHover(card, isHovering) {
        const image = card.querySelector('.blog-preview-card-image img');
        const readMore = card.querySelector('.blog-preview-card-read-more');
        
        if (isHovering) {
            image.style.transform = 'scale(1.05)';
            readMore.style.transform = 'translateX(5px)';
        } else {
            image.style.transform = 'scale(1)';
            readMore.style.transform = 'translateX(0)';
        }
    }

    bindViewAllButton() {
        const viewAllBtn = this.container.querySelector('.blog-preview-view-all');
        if (viewAllBtn) {
            viewAllBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.animateViewAll(viewAllBtn);
            });
        }
    }

    animateViewAll(button) {
        const originalHTML = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Cargando blog...';
        button.disabled = true;

        // Agregar efecto de transición suave
        this.container.style.opacity = '0.7';
        
        setTimeout(() => {
            window.location.href = button.getAttribute('data-href') || '/blog/';
        }, 600);
    }

    bindCardClickTracking() {
        // Tracking opcional para analytics
        const cards = this.container.querySelectorAll('.blog-preview-card');
        
        cards.forEach((card, index) => {
            const link = card.querySelector('.blog-preview-card-title a');
            if (link) {
                link.addEventListener('click', () => {
                    // Aquí podrías agregar Google Analytics tracking
                    // gtag('event', 'blog_preview_click', {
                    //     'card_position': index + 1,
                    //     'article_title': link.textContent.trim()
                    // });
                });
            }
        });
    }

    initializeCards() {
        // Agregar clases CSS dinámicamente si es necesario
        const cards = this.container.querySelectorAll('.blog-preview-card');
        cards.forEach((card, index) => {
            card.style.setProperty('--card-index', index);
            card.classList.add('blog-preview-card-interactive');
        });
    }

    // Método público para actualizar las tarjetas si es necesario
    updateCards(newEntries) {
        const cardsContainer = this.container.querySelector('.blog-preview-cards');
        if (!cardsContainer) return;

        // Limpiar tarjetas existentes
        cardsContainer.innerHTML = '';

        // Crear nuevas tarjetas
        newEntries.forEach((entry, index) => {
            const card = this.createCard(entry, index);
            cardsContainer.appendChild(card);
        });

        // Reinicializar efectos
        this.initializeCards();
        this.bindCardHoverEffects();
    }

    createCard(entry, index) {
        const card = document.createElement('div');
        card.className = 'blog-preview-card';
        card.setAttribute('data-aos', 'fade-up');
        card.setAttribute('data-aos-delay', index * 100);

        card.innerHTML = `
            <div class="blog-preview-card-image">
                <img src="${entry.imagen_portada || '/static/app/images/blog-placeholder.jpg'}" 
                     alt="${entry.titulo}" 
                     loading="lazy">
            </div>
            <div class="blog-preview-card-content">
                <h3 class="blog-preview-card-title">
                    <a href="/blog/${entry.slug}/">${entry.titulo}</a>
                </h3>
                <p class="blog-preview-card-description">
                    ${this.truncateText(entry.descripcion, 120)}
                </p>
                <div class="blog-preview-card-meta">
                    <span class="blog-preview-card-date">
                        <i class="fas fa-calendar-alt me-1"></i>
                        ${this.formatDate(entry.fecha_creacion)}
                    </span>
                    <a href="/blog/${entry.slug}/" class="blog-preview-card-read-more">
                        Leer más <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>
        `;

        return card;
    }

    // Utilidades
    formatDate(dateString) {
        const options = { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric'
        };
        return new Date(dateString).toLocaleDateString('es-ES', options);
    }

    truncateText(text, maxLength = 120) {
        if (!text || text.length <= maxLength) return text;
        return text.substr(0, maxLength).trim() + '...';
    }

    // Método para mostrar estado de carga
    showLoading() {
        const cardsContainer = this.container.querySelector('.blog-preview-cards');
        if (cardsContainer) {
            cardsContainer.innerHTML = `
                <div class="blog-preview-loading">
                    <div class="blog-loading-spinner"></div>
                    <p class="mt-3 text-muted">Cargando últimas entradas...</p>
                </div>
            `;
        }
    }

    // Método para mostrar estado vacío
    showEmpty() {
        const cardsContainer = this.container.querySelector('.blog-preview-cards');
        if (cardsContainer) {
            cardsContainer.innerHTML = `
                <div class="blog-preview-empty">
                    <i class="fas fa-blog mb-3 text-muted" style="font-size: 3rem;"></i>
                    <h4 class="text-muted">No hay entradas aún</h4>
                    <p class="text-muted">Pronto publicaremos contenido interesante sobre carpintería de aluminio.</p>
                </div>
            `;
        }
    }
}

// CSS adicional para efectos específicos de la vista previa
const blogPreviewStyles = `
<style>
.blog-preview-card-interactive {
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.blog-preview-card.animate-in {
    opacity: 1;
    transform: translateY(0);
}

.blog-preview-card {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}

.blog-preview-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    grid-column: 1 / -1;
}

.blog-preview-empty {
    text-align: center;
    padding: 3rem;
    grid-column: 1 / -1;
}

.blog-loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #dc3545;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .blog-preview-cards {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
}
</style>
`;

// Inyectar estilos si no están ya presentes
if (!document.querySelector('#blog-preview-styles')) {
    const styleElement = document.createElement('div');
    styleElement.id = 'blog-preview-styles';
    styleElement.innerHTML = blogPreviewStyles;
    document.head.appendChild(styleElement);
}

// Auto-inicializar cuando se carga el DOM
document.addEventListener('DOMContentLoaded', function() {
    new BlogPreview();
});

// Exportar para uso externo
window.BlogPreview = BlogPreview;