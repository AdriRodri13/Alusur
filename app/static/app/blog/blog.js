/**
 * Blog JavaScript - Simple y funcional
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Search functionality
    const searchInput = document.getElementById('blogSearch');
    const searchBtn = document.getElementById('searchBtn');
    
    if (searchInput && searchBtn) {
        function performSearch() {
            const searchTerm = searchInput.value.trim();
            if (searchTerm) {
                filterPosts(searchTerm);
            } else {
                showAllPosts();
            }
        }
        
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch();
            }
        });
    }
    
    // Category filtering
    const categoryLinks = document.querySelectorAll('[data-category]');
    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.category;
            
            // Update active state
            categoryLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Filter posts by category
            filterByCategory(category);
        });
    });
    
    // Newsletter form
    const newsletterForm = document.querySelector('.newsletter-section form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            
            if (email) {
                alert('¡Gracias por suscribirte! Pronto recibirás noticias de ALUSUR.');
                this.reset();
            }
        });
    }
    
    // Smooth scrolling for internal links
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
});

// Helper functions
function filterPosts(searchTerm) {
    const posts = document.querySelectorAll('.blog-card');
    const lowerSearchTerm = searchTerm.toLowerCase();
    
    posts.forEach(post => {
        const title = post.querySelector('.blog-card-title')?.textContent.toLowerCase() || '';
        const description = post.querySelector('.blog-card-description')?.textContent.toLowerCase() || '';
        
        if (title.includes(lowerSearchTerm) || description.includes(lowerSearchTerm)) {
            post.style.display = 'block';
        } else {
            post.style.display = 'none';
        }
    });
}

function filterByCategory(category) {
    const posts = document.querySelectorAll('.blog-card');
    
    posts.forEach(post => {
        if (category === 'all') {
            post.style.display = 'block';
        } else {
            // Esta funcionalidad requiere que los posts tengan atributos data-category
            const postCategory = post.dataset.category || 'general';
            if (postCategory === category) {
                post.style.display = 'block';
            } else {
                post.style.display = 'none';
            }
        }
    });
}

function showAllPosts() {
    const posts = document.querySelectorAll('.blog-card');
    posts.forEach(post => {
        post.style.display = 'block';
    });
}