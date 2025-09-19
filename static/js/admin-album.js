// Script pour l'upload multiple d'images dans les albums
document.addEventListener('DOMContentLoaded', function() {
    
    const filesInput = document.getElementById('files');
    if (filesInput) {
        filesInput.addEventListener('change', function(e) {
            const files = e.target.files;
            const selectedFiles = document.getElementById('selectedFiles');
            const filesList = document.getElementById('filesList');
            
            if (files.length > 0) {
                selectedFiles.style.display = 'block';
                filesList.innerHTML = '';
                
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-item';
                    fileItem.style.cssText = 'display: flex; align-items: center; padding: 0.5rem; background: #f8f9fa; margin: 0.25rem 0; border-radius: 5px;';
                    
                    fileItem.innerHTML = `
                        <i class="fas fa-image" style="color: #28a745; margin-right: 0.5rem;"></i>
                        <span>${file.name}</span>
                        <small style="margin-left: auto; color: #666;">${(file.size / 1024 / 1024).toFixed(1)} MB</small>
                    `;
                    
                    filesList.appendChild(fileItem);
                }
                
                // Calculer la taille totale
                let totalSize = 0;
                for (let i = 0; i < files.length; i++) {
                    totalSize += files[i].size;
                }
                
                // Afficher le nombre total et la taille
                const totalInfo = document.createElement('div');
                totalInfo.style.cssText = 'margin-top: 0.5rem; font-weight: bold; color: #495057;';
                const totalSizeMB = (totalSize / 1024 / 1024).toFixed(1);
                totalInfo.innerHTML = `Total: ${files.length} fichier(s) - ${totalSizeMB} MB`;
                
                // Avertissement si trop gros
                if (totalSize > 100 * 1024 * 1024) { // 100MB
                    totalInfo.style.color = '#dc3545';
                    totalInfo.innerHTML += '<br><small>⚠️ Taille importante - Considérez uploader par petits groupes</small>';
                }
                
                filesList.appendChild(totalInfo);
            } else {
                selectedFiles.style.display = 'none';
            }
        });
    }
});