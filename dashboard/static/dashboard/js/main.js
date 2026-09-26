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
const sidebarToggle = document.createElement('button');
sidebarToggle.innerHTML = '☰';
sidebarToggle.style.cssText = 'display:none;position:fixed;top:10px;left:10px;z-index:1001;background:#1f2937;color:white;border:none;padding:10px;border-radius:8px;font-size:20px;cursor:pointer;';
document.body.appendChild(sidebarToggle);

const sidebar = document.querySelector('.sidebar');
if (sidebar) {
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });
}

// Responsive sidebar
function checkWidth() {
    if (window.innerWidth <= 768) {
        if (sidebar) sidebar.style.display = 'none';
        if (sidebarToggle) sidebarToggle.style.display = 'block';
    } else {
        if (sidebar) sidebar.style.display = 'block';
        if (sidebarToggle) sidebarToggle.style.display = 'none';
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
