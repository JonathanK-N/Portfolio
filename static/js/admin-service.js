// Script pour l'édition des services
document.addEventListener('DOMContentLoaded', function() {
    
    // Fonctions globales pour les inclusions
    window.removeInclude = function(button) {
        const item = button.parentElement;
        const input = item.querySelector('input');
        input.value = '';
        item.style.display = 'none';
    };

    window.addInclude = function() {
        const container = document.getElementById('includes-container');
        const hiddenItems = container.querySelectorAll('.include-item[style*="none"]');
        
        if (hiddenItems.length > 0) {
            const item = hiddenItems[0];
            item.style.display = 'flex';
            item.querySelector('input').focus();
        }
    };

    // Aperçu de l'image
    const serviceImageInput = document.getElementById('service_image');
    if (serviceImageInput) {
        serviceImageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('previewImg').src = e.target.result;
                    document.getElementById('imagePreview').style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    }
});