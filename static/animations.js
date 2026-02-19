// EcoPlan - Enhanced UI Interactions & Animations

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeMicroInteractions();
    initializeProgressAnimations();
    initializeTooltips();
});

// Initialize page animations
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe all cards and metric elements - but don't hide them initially
    document.querySelectorAll('.card, .metric-card, .hero-section').forEach(el => {
        el.style.opacity = '1'; // Ensure visibility
        observer.observe(el);
    });
}

// Initialize micro-interactions
function initializeMicroInteractions() {
    // Add ripple effect to buttons
    document.addEventListener('click', function(e) {
        if (e.target.matches('.btn, .btn *')) {
            const button = e.target.closest('.btn');
            createRipple(e, button);
        }
    });

    // Add hover effects to cards
    document.querySelectorAll('.card, .metric-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add focus effects to form inputs
    document.querySelectorAll('.form-control, .form-select').forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('input-focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('input-focused');
        });
    });
}

// Create ripple effect
function createRipple(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple-effect');

    element.appendChild(ripple);

    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Initialize progress bar animations
function initializeProgressAnimations() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    const progressObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                progressBar.style.width = '0%';
                
                setTimeout(() => {
                    progressBar.style.width = width;
                }, 200);
            }
        });
    }, { threshold: 0.5 });

    progressBars.forEach(bar => {
        progressObserver.observe(bar);
    });
}

// Initialize tooltips
function initializeTooltips() {
    // Create tooltip element
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip glass-effect';
    tooltip.style.cssText = `
        position: absolute;
        z-index: 9999;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 0.875rem;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.3s ease;
        max-width: 200px;
    `;
    document.body.appendChild(tooltip);

    // Add tooltip functionality
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const text = this.getAttribute('data-tooltip');
            tooltip.textContent = text;
            tooltip.style.opacity = '1';
            updateTooltipPosition(e, tooltip);
        });

        element.addEventListener('mousemove', function(e) {
            updateTooltipPosition(e, tooltip);
        });

        element.addEventListener('mouseleave', function() {
            tooltip.style.opacity = '0';
        });
    });
}

// Update tooltip position
function updateTooltipPosition(event, tooltip) {
    const x = event.clientX + 10;
    const y = event.clientY - 10;
    
    tooltip.style.left = x + 'px';
    tooltip.style.top = y + 'px';
}

// Animate numbers counting up
function animateCountUp(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

// Initialize count-up animations for metric values
function initializeCountUpAnimations() {
    const metricValues = document.querySelectorAll('.metric-value, .score-number');
    
    const countUpObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                const target = parseInt(entry.target.textContent) || 0;
                entry.target.classList.add('animated');
                animateCountUp(entry.target, target);
            }
        });
    }, { threshold: 0.5 });

    metricValues.forEach(element => {
        countUpObserver.observe(element);
    });
}

// Smooth scroll for anchor links
function initializeSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Add loading states
function showLoading(element, text = 'Loading...') {
    element.classList.add('loading');
    const originalContent = element.innerHTML;
    element.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${text}`;
    
    return () => {
        element.classList.remove('loading');
        element.innerHTML = originalContent;
    };
}

// Add success/error states
function showStatus(element, type, message, duration = 3000) {
    const statusClass = type === 'success' ? 'alert-success' : 'alert-danger';
    const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
    
    element.innerHTML = `
        <div class="alert ${statusClass} glass-effect fade-in-up">
            <i class="fas ${icon} me-2"></i>${message}
        </div>
    `;
    
    if (duration > 0) {
        setTimeout(() => {
            element.innerHTML = '';
        }, duration);
    }
}

// Enhanced form validation
function enhanceFormValidation() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const invalidInputs = form.querySelectorAll(':invalid');
            
            invalidInputs.forEach(input => {
                input.classList.add('is-invalid');
                input.addEventListener('input', function() {
                    if (this.checkValidity()) {
                        this.classList.remove('is-invalid');
                        this.classList.add('is-valid');
                    }
                });
            });
        });
    });
}

// Initialize all enhancements
function initializeEnhancements() {
    initializeCountUpAnimations();
    initializeSmoothScroll();
    enhanceFormValidation();
}

// Call initialization functions
setTimeout(initializeEnhancements, 500);

// Export functions for use in other scripts
window.EcoPlanUI = {
    showLoading,
    showStatus,
    animateCountUp,
    createRipple
};

// Add CSS for additional animations
const additionalStyles = `
    .animate-in {
        animation: fadeInUp 0.8s ease-out forwards;
        opacity: 1 !important;
    }
    
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .input-focused {
        transform: scale(1.02);
        transition: transform 0.3s ease;
    }
    
    .custom-tooltip {
        background: var(--glass-bg);
        backdrop-filter: var(--glass-blur);
        border: 1px solid var(--glass-border);
        color: var(--light-text);
        box-shadow: var(--glass-shadow);
    }
    
    .is-invalid {
        border-color: #ef4444 !important;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1) !important;
    }
    
    .is-valid {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);