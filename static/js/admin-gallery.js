// Script pour l'ajout d'images dans la galerie
document.addEventListener('DOMContentLoaded', function() {
    let selectedCrop = 'center';
    
    // Aperçu de l'image
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('previewImg').src = e.target.result;
                    document.getElementById('imagePreview').style.display = 'block';
                    document.getElementById('cropControls').style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Gestion du cadrage
    document.querySelectorAll('.crop-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.crop-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            selectedCrop = this.dataset.crop;
            document.getElementById('cropPosition').value = selectedCrop;
            
            // Appliquer l'aperçu du cadrage
            const img = document.getElementById('previewImg');
            img.style.objectPosition = getCropPosition(selectedCrop);
        });
    });
    
    function getCropPosition(crop) {
        switch(crop) {
            case 'top': return 'center top';
            case 'bottom': return 'center bottom';
            case 'left': return 'left center';
            case 'right': return 'right center';
            default: return 'center center';
        }
    }
    
    // Sélectionner "Centré" par défaut
    const centerBtn = document.querySelector('[data-crop="center"]');
    if (centerBtn) {
        centerBtn.classList.add('active');
    }
});