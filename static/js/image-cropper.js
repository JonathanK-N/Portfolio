// Outil de rognage d'image
class ImageCropper {
    constructor(imageElement, aspectRatio = 1) {
        this.image = imageElement;
        this.aspectRatio = aspectRatio;
        this.cropBox = null;
        this.isDragging = false;
        this.startX = 0;
        this.startY = 0;
        this.cropData = { x: 0, y: 0, width: 0, height: 0 };
        this.init();
    }

    init() {
        this.image.style.position = 'relative';
        this.image.style.maxWidth = '100%';
        this.image.style.height = 'auto';
        
        this.createCropBox();
        this.addEventListeners();
        this.resetCrop();
    }

    createCropBox() {
        this.cropBox = document.createElement('div');
        this.cropBox.className = 'crop-box';
        this.cropBox.style.cssText = `
            position: absolute;
            border: 2px solid #e74c3c;
            background: rgba(231, 76, 60, 0.1);
            cursor: move;
            z-index: 10;
        `;
        
        this.image.parentElement.style.position = 'relative';
        this.image.parentElement.appendChild(this.cropBox);
    }

    addEventListeners() {
        this.cropBox.addEventListener('mousedown', this.startDrag.bind(this));
        document.addEventListener('mousemove', this.drag.bind(this));
        document.addEventListener('mouseup', this.endDrag.bind(this));
    }

    startDrag(e) {
        this.isDragging = true;
        this.startX = e.clientX - this.cropBox.offsetLeft;
        this.startY = e.clientY - this.cropBox.offsetTop;
        e.preventDefault();
    }

    drag(e) {
        if (!this.isDragging) return;
        
        const rect = this.image.getBoundingClientRect();
        const parentRect = this.image.parentElement.getBoundingClientRect();
        
        let newX = e.clientX - parentRect.left - this.startX;
        let newY = e.clientY - parentRect.top - this.startY;
        
        // Limiter aux bordures de l'image
        newX = Math.max(0, Math.min(newX, this.image.offsetWidth - this.cropBox.offsetWidth));
        newY = Math.max(0, Math.min(newY, this.image.offsetHeight - this.cropBox.offsetHeight));
        
        this.cropBox.style.left = newX + 'px';
        this.cropBox.style.top = newY + 'px';
        
        this.updateCropData();
    }

    endDrag() {
        this.isDragging = false;
    }

    resetCrop() {
        const imageWidth = this.image.offsetWidth;
        const imageHeight = this.image.offsetHeight;
        
        let cropWidth, cropHeight;
        
        if (imageWidth / imageHeight > this.aspectRatio) {
            cropHeight = imageHeight * 0.8;
            cropWidth = cropHeight * this.aspectRatio;
        } else {
            cropWidth = imageWidth * 0.8;
            cropHeight = cropWidth / this.aspectRatio;
        }
        
        const x = (imageWidth - cropWidth) / 2;
        const y = (imageHeight - cropHeight) / 2;
        
        this.cropBox.style.left = x + 'px';
        this.cropBox.style.top = y + 'px';
        this.cropBox.style.width = cropWidth + 'px';
        this.cropBox.style.height = cropHeight + 'px';
        
        this.updateCropData();
    }

    updateCropData() {
        const imageWidth = this.image.naturalWidth;
        const imageHeight = this.image.naturalHeight;
        const displayWidth = this.image.offsetWidth;
        const displayHeight = this.image.offsetHeight;
        
        const scaleX = imageWidth / displayWidth;
        const scaleY = imageHeight / displayHeight;
        
        this.cropData = {
            x: Math.round(this.cropBox.offsetLeft * scaleX),
            y: Math.round(this.cropBox.offsetTop * scaleY),
            width: Math.round(this.cropBox.offsetWidth * scaleX),
            height: Math.round(this.cropBox.offsetHeight * scaleY)
        };
    }

    getCropData() {
        return this.cropData;
    }

    destroy() {
        if (this.cropBox) {
            this.cropBox.remove();
        }
    }
}