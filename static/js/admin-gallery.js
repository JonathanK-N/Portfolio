// Script pour l'ajout d'images dans la galerie avec rognage
document.addEventListener('DOMContentLoaded', function() {
    let cropper = null;
    
    // Aperçu de l'image avec rognage
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const previewImg = document.getElementById('previewImg');
                    previewImg.src = e.target.result;
                    document.getElementById('imagePreview').style.display = 'block';
                    
                    // Attendre que l'image soit chargée
                    previewImg.onload = function() {
                        // Détruire l'ancien cropper s'il existe
                        if (cropper) {
                            cropper.destroy();
                        }
                        
                        // Créer le nouveau cropper (ratio 4:3)
                        cropper = new ImageCropper(previewImg, 4/3);
                        document.getElementById('cropControls').style.display = 'block';
                        
                        // Mettre à jour les données de rognage
                        updateCropData();
                    };
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Fonction globale pour réinitialiser le rognage
    window.resetCrop = function() {
        if (cropper) {
            cropper.resetCrop();
            updateCropData();
        }
    };
    
    function updateCropData() {
        if (cropper) {
            const cropData = cropper.getCropData();
            document.getElementById('cropData').value = JSON.stringify(cropData);
        }
    }
    
    // Mettre à jour les données de rognage quand on bouge la zone
    document.addEventListener('mouseup', function() {
        setTimeout(updateCropData, 100);
    });
});