from flask import Flask, render_template, request, flash, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'prima_photo_secret_key'

# Configuration pour les images
UPLOAD_FOLDER = 'static/images/gallery'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Données du portfolio professionnel
GALLERY_IMAGES = [
    # Portraits
    {'filename': 'portrait-1.jpg', 'title': 'Portrait Corporate Élégant', 'category': 'portrait'},
    {'filename': 'portrait-2.jpg', 'title': 'Portrait Artistique en Studio', 'category': 'portrait'},
    {'filename': 'portrait-3.jpg', 'title': 'Portrait Professionnel Femme', 'category': 'portrait'},
    {'filename': 'portrait-4.jpg', 'title': 'Portrait Homme d\'Affaires', 'category': 'portrait'},
    
    # Mariages
    {'filename': 'mariage-1.jpg', 'title': 'Cérémonie Romantique', 'category': 'mariage'},
    {'filename': 'mariage-2.jpg', 'title': 'Premier Regard', 'category': 'mariage'},
    {'filename': 'mariage-3.jpg', 'title': 'Échange des Vœux', 'category': 'mariage'},
    {'filename': 'mariage-4.jpg', 'title': 'Danse des Mariés', 'category': 'mariage'},
    
    # Nature
    {'filename': 'nature-1.jpg', 'title': 'Paysage Montagneux', 'category': 'nature'},
    {'filename': 'nature-2.jpg', 'title': 'Forêt Mystique', 'category': 'nature'},
    {'filename': 'nature-3.jpg', 'title': 'Coucher de Soleil', 'category': 'nature'},
    {'filename': 'nature-4.jpg', 'title': 'Reflets sur l\'Eau', 'category': 'nature'},
    
    # Architecture
    {'filename': 'architecture-1.jpg', 'title': 'Gratte-Ciel Moderne', 'category': 'architecture'},
    {'filename': 'architecture-2.jpg', 'title': 'Détails Architecturaux', 'category': 'architecture'},
    {'filename': 'architecture-3.jpg', 'title': 'Perspective Urbaine', 'category': 'architecture'},
    {'filename': 'architecture-4.jpg', 'title': 'Jeux d\'Ombres', 'category': 'architecture'},
    
    # Mode
    {'filename': 'mode-1.jpg', 'title': 'Fashion Editorial', 'category': 'mode'},
    {'filename': 'mode-2.jpg', 'title': 'Street Style Urbain', 'category': 'mode'},
    {'filename': 'mode-3.jpg', 'title': 'Haute Couture', 'category': 'mode'},
    {'filename': 'mode-4.jpg', 'title': 'Mode Lifestyle', 'category': 'mode'},
    
    # Événements
    {'filename': 'evenement-1.jpg', 'title': 'Conférence Corporate', 'category': 'evenement'},
    {'filename': 'evenement-2.jpg', 'title': 'Gala de Prestige', 'category': 'evenement'},
    {'filename': 'evenement-3.jpg', 'title': 'Lancement Produit', 'category': 'evenement'},
    {'filename': 'evenement-4.jpg', 'title': 'Networking Event', 'category': 'evenement'}
]

@app.route('/')
def home():
    return render_template('index.html', images=GALLERY_IMAGES[:8])

@app.route('/galerie')
def gallery():
    category = request.args.get('category', 'all')
    if category == 'all':
        filtered_images = GALLERY_IMAGES
    else:
        filtered_images = [img for img in GALLERY_IMAGES if img['category'] == category]
    return render_template('gallery.html', images=filtered_images, current_category=category)

@app.route('/a-propos')
def about():
    return render_template('about.html')

# Services disponibles
SERVICES = {
    'portrait': {
        'name': 'Portrait Professionnel',
        'duration': '1-2 heures',
        'description': 'Séance portrait en studio ou extérieur avec retouches incluses',
        'includes': ['Séance photo', '10 photos retouchées', 'Galerie privée en ligne']
    },
    'mariage': {
        'name': 'Photographie de Mariage',
        'duration': 'Journée complète',
        'description': 'Couverture complète de votre mariage avec reportage photo',
        'includes': ['Préparatifs', 'Cérémonie', 'Cocktail', 'Soirée', '200+ photos retouchées']
    },
    'evenement': {
        'name': 'Événement Corporate',
        'duration': '2-4 heures',
        'description': 'Couverture photographique de vos événements professionnels',
        'includes': ['Reportage complet', 'Photos haute résolution', 'Livraison 48h']
    },
    'famille': {
        'name': 'Séance Famille',
        'duration': '1 heure',
        'description': 'Séance photo famille en extérieur ou à domicile',
        'includes': ['Séance photo', '15 photos retouchées', 'Impression offerte']
    }
}

@app.route('/services')
def services():
    return render_template('services.html', services=SERVICES)

@app.route('/reserver/<service_type>', methods=['GET', 'POST'])
def book_service(service_type):
    if service_type not in SERVICES:
        flash('Service non trouvé.', 'error')
        return redirect(url_for('services'))
    
    service = SERVICES[service_type]
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date = request.form.get('date')
        message = request.form.get('message')
        budget = request.form.get('budget', '')
        service_name = service['name']
        
        # Créer le message WhatsApp
        whatsapp_message = f"🔔 NOUVELLE RÉSERVATION - {service_name}\n\n"
        whatsapp_message += f"👤 Client: {name}\n"
        whatsapp_message += f"📧 Email: {email}\n"
        whatsapp_message += f"📱 Téléphone: {phone}\n"
        whatsapp_message += f"📅 Date souhaitée: {date}\n"
        if budget:
            whatsapp_message += f"💰 Budget: {budget}\n"
        whatsapp_message += f"\n💬 Message:\n{message}\n\n"
        whatsapp_message += f"Service: {service_name} ({service['price']})"
        
        # Numéro WhatsApp du photographe (à modifier avec votre vrai numéro)
        photographer_phone = "+18196745823"  # IMPORTANT: Remplacez par votre numéro WhatsApp
        
        # URL WhatsApp
        import urllib.parse
        whatsapp_url = f"https://wa.me/{photographer_phone.replace('+', '')}?text={urllib.parse.quote(whatsapp_message)}"
        
        # Rediriger vers WhatsApp
        return redirect(whatsapp_url)
    
    return render_template('book_service.html', service=service, service_type=service_type)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Ici vous pourriez envoyer l'email ou sauvegarder en base
        flash('Merci pour votre message ! Je vous répondrai rapidement.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    # Créer les dossiers nécessaires
    os.makedirs('static/images/gallery', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True)