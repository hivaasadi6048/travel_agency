// === آژانس هواپیمایی ورزان گشت - JavaScript ===

// Fade-in animation on scroll
document.addEventListener('DOMContentLoaded', function() {
    const fadeElements = document.querySelectorAll('.fade-in');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });
    fadeElements.forEach(el => observer.observe(el));
});

// Confirmation dialogs for delete actions
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn-delete') || e.target.closest('.btn-delete')) {
        const link = e.target.closest('a') || e.target;
        if (!confirm('آیا مطمئن هستید که می‌خواهید حذف کنید؟')) {
            e.preventDefault();
        }
    }
});

// Auto-hide messages after 5 seconds
function autoHideMessages() {
    const messages = document.querySelectorAll('.messages p');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300);
        }, 5000);
    });
}
autoHideMessages();

// Search functionality
const searchInputs = document.querySelectorAll('input[placeholder*="جستجو"], input[placeholder*="search"]');
searchInputs.forEach(input => {
    input.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            this.form?.submit();
        }
    });
});

// Toggle sidebar on mobile
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.querySelector('.sidebar');
const sidebarOverlay = document.querySelector('.sidebar-overlay');

if (sidebar && sidebarToggle) {
    function toggleSidebar() {
        sidebar.classList.toggle('active');
        if (sidebarOverlay) sidebarOverlay.classList.toggle('active');
    }
    sidebarToggle.addEventListener('click', toggleSidebar);
    if (sidebarOverlay) sidebarOverlay.addEventListener('click', toggleSidebar);
}

// Responsive sidebar
function checkWidth() {
    if (window.innerWidth <= 1024) {
        if (sidebar) sidebar.classList.remove('active');
    }
}
window.addEventListener('resize', checkWidth);
checkWidth();

// Print functionality
function printPage() {
    window.print();
}

// Export to Excel shortcut
function exportExcel() {
    window.open(window.location.href + '/excel/');
}

console.log('✅ ورزان گشت - سیستم بارگذاری شد');
