from flask import Flask, render_template, request, flash, redirect, url_for, session
import os
import json
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'prima_photo_secret_key_change_in_production')

# Configuration pour les images
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 30MB max

# Configuration admin
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'prima2024')

# Configuration Cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

def upload_to_cloudinary(file, folder="prima_photo", crop_position="center"):
    """Upload une image vers Cloudinary avec cadrage personnalisé"""
    try:
        # Mapping des positions de cadrage
        gravity_map = {
            'center': 'center',
            'top': 'north',
            'bottom': 'south',
            'left': 'west',
            'right': 'east'
        }
        
        gravity = gravity_map.get(crop_position, 'center')
        
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            transformation=[
                {'width': 800, 'height': 600, 'crop': 'fill', 'gravity': gravity},
                {'quality': 'auto', 'fetch_format': 'auto'}
            ]
        )
        return result['secure_url']
    except Exception as e:
        print(f"Erreur upload Cloudinary: {e}")
        return None

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Données du portfolio professionnel (URLs Cloudinary)
GALLERY_IMAGES = [
    # Portraits
    {'url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop', 'title': 'Portrait Corporate Élégant', 'category': 'portrait'},
    {'url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=800&h=600&fit=crop', 'title': 'Portrait Artistique en Studio', 'category': 'portrait'},
    {'url': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=800&h=600&fit=crop', 'title': 'Portrait Professionnel Femme', 'category': 'portrait'},
    {'url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=800&h=600&fit=crop', 'title': 'Portrait Homme d\'Affaires', 'category': 'portrait'},
    
    # Mariages
    {'url': 'https://images.unsplash.com/photo-1519741497674-611481863552?w=800&h=600&fit=crop', 'title': 'Cérémonie Romantique', 'category': 'mariage'},
    {'url': 'https://images.unsplash.com/photo-1606216794074-735e91aa2c92?w=800&h=600&fit=crop', 'title': 'Premier Regard', 'category': 'mariage'},
    {'url': 'https://images.unsplash.com/photo-1583939003579-730e3918a45a?w=800&h=600&fit=crop', 'title': 'Échange des Vœux', 'category': 'mariage'},
    {'url': 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=800&h=600&fit=crop', 'title': 'Danse des Mariés', 'category': 'mariage'}
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
    return render_template('about.html', content=PAGE_CONTENT['about'])

# Contenu des pages
PAGE_CONTENT = {
    'about': {
        'title': 'Bonjour, je suis PRiMA',
        'subtitle': 'Photographe professionnel passionné par l\'art de capturer les moments uniques et les émotions authentiques.',
        'description': 'J\'ai eu le privilège de travailler avec des clients variés, des particuliers aux entreprises, en passant par les événements les plus prestigieux.',
        'philosophy': 'Ma philosophie est simple : chaque photo raconte une histoire. Mon rôle est de révéler la beauté naturelle de chaque instant, que ce soit lors d\'un portrait intime, d\'un mariage romantique, ou d\'un événement corporate.',
        'photo': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=600&h=800&fit=crop',
        'stats': {
            'projects': '100+',
            'experience': '2+',
            'satisfaction': '100%'
        }
    },
    'contact': {
        'email': 'contact@primaphoto.com',
        'phone': '+1 819 674 5823',
        'location': 'Sherbrooke, QC, Canada',
        'hours': 'Sur rendez-vous',
        'whatsapp': '+1 819 674 5823'
    }
}

# Services disponibles
SERVICES = {
    'portrait': {
        'name': 'Portrait Professionnel',
        'price': '',
        'duration': '1-2 heures',
        'description': 'Séance portrait en studio ou extérieur avec retouches incluses',
        'includes': ['Séance photo', '10 photos retouchées', 'Galerie privée en ligne']
    },
    'mariage': {
        'name': 'Photographie de Mariage',
        'price': '',
        'duration': 'Journée complète',
        'description': 'Couverture complète de votre mariage avec reportage photo',
        'includes': ['Préparatifs', 'Cérémonie', 'Cocktail', 'Soirée', '200+ photos retouchées']
    },
    'evenement': {
        'name': 'Événement Corporate',
        'price': '',
        'duration': '2-4 heures',
        'description': 'Couverture photographique de vos événements professionnels',
        'includes': ['Reportage complet', 'Photos haute résolution', 'Livraison 48h']
    },
    'famille': {
        'name': 'Séance Famille',
        'price': '',
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
        whatsapp_message += f"Service: {service_name} ({service.get('price', 'Prix sur demande')})"
        
        # Numéro WhatsApp du photographe (à modifier avec votre vrai numéro)
        photographer_phone = PAGE_CONTENT['contact']['whatsapp']
        
        # URL WhatsApp
        import urllib.parse
        # Nettoyer le numéro (enlever espaces, tirets, etc.)
        clean_phone = photographer_phone.replace('+', '').replace(' ', '').replace('-', '')
        whatsapp_url = f"https://wa.me/{clean_phone}?text={urllib.parse.quote(whatsapp_message)}"
        
        # Rediriger directement vers WhatsApp
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
    
    return render_template('contact.html', content=PAGE_CONTENT['contact'])

# Routes Admin
@app.route('/admin')
def admin_login():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        flash('Connexion réussie !', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Identifiants incorrects', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Déconnexion réussie', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin/dashboard.html', images=GALLERY_IMAGES, services=SERVICES, content=PAGE_CONTENT)

@app.route('/admin/gallery')
def admin_gallery():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin/gallery.html', images=GALLERY_IMAGES)

@app.route('/admin/gallery/add', methods=['GET', 'POST'])
def admin_add_image():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        file = request.files.get('file')
        
        if file and allowed_file(file.filename):
            # Récupérer la position de cadrage
            crop_position = request.form.get('crop_position', 'center')
            
            # Upload vers Cloudinary avec cadrage
            cloudinary_url = upload_to_cloudinary(file, f"prima_photo/gallery/{category}", crop_position)
            
            if cloudinary_url:
                new_image = {
                    'url': cloudinary_url,
                    'title': title,
                    'category': category
                }
                GALLERY_IMAGES.append(new_image)
                
                flash('Image ajoutée avec succès !', 'success')
                return redirect(url_for('admin_gallery'))
            else:
                flash('Erreur lors de l\'upload', 'error')
        else:
            flash('Fichier invalide', 'error')
    
    return render_template('admin/add_image.html')

@app.route('/admin/gallery/delete/<int:image_id>')
def admin_delete_image(image_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    if 0 <= image_id < len(GALLERY_IMAGES):
        GALLERY_IMAGES.pop(image_id)
        flash('Image supprimée !', 'success')
    
    return redirect(url_for('admin_gallery'))

@app.route('/admin/services')
def admin_services():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin/services.html', services=SERVICES)

@app.route('/admin/services/edit/<service_key>', methods=['GET', 'POST'])
def admin_edit_service(service_key):
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    if service_key not in SERVICES:
        flash('Service non trouvé', 'error')
        return redirect(url_for('admin_services'))
    
    if request.method == 'POST':
        SERVICES[service_key]['name'] = request.form.get('name')
        SERVICES[service_key]['price'] = request.form.get('price')
        SERVICES[service_key]['duration'] = request.form.get('duration')
        SERVICES[service_key]['description'] = request.form.get('description')
        
        # Gestion des inclusions
        includes = []
        for i in range(10):  # Max 10 inclusions
            include = request.form.get(f'include_{i}')
            if include and include.strip():
                includes.append(include.strip())
        SERVICES[service_key]['includes'] = includes
        
        flash('Service mis à jour !', 'success')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/edit_service.html', service=SERVICES[service_key], service_key=service_key)

@app.route('/admin/pages')
def admin_pages():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin/pages.html', content=PAGE_CONTENT)

@app.route('/admin/pages/about', methods=['GET', 'POST'])
def admin_edit_about():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        PAGE_CONTENT['about']['title'] = request.form.get('title')
        PAGE_CONTENT['about']['subtitle'] = request.form.get('subtitle')
        PAGE_CONTENT['about']['description'] = request.form.get('description')
        PAGE_CONTENT['about']['philosophy'] = request.form.get('philosophy')
        PAGE_CONTENT['about']['stats']['projects'] = request.form.get('projects')
        PAGE_CONTENT['about']['stats']['experience'] = request.form.get('experience')
        PAGE_CONTENT['about']['stats']['satisfaction'] = request.form.get('satisfaction')
        
        # Gestion de la photo
        file = request.files.get('photo')
        if file and allowed_file(file.filename):
            cloudinary_url = upload_to_cloudinary(file, "prima_photo/about")
            if cloudinary_url:
                PAGE_CONTENT['about']['photo'] = cloudinary_url
        
        flash('Page À propos mise à jour !', 'success')
        return redirect(url_for('admin_pages'))
    
    return render_template('admin/edit_about.html', content=PAGE_CONTENT['about'])

@app.route('/admin/pages/contact', methods=['GET', 'POST'])
def admin_edit_contact():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        PAGE_CONTENT['contact']['email'] = request.form.get('email')
        PAGE_CONTENT['contact']['phone'] = request.form.get('phone')
        PAGE_CONTENT['contact']['location'] = request.form.get('location')
        PAGE_CONTENT['contact']['hours'] = request.form.get('hours')
        PAGE_CONTENT['contact']['whatsapp'] = request.form.get('whatsapp')
        
        flash('Page Contact mise à jour !', 'success')
        return redirect(url_for('admin_pages'))
    
    return render_template('admin/edit_contact.html', content=PAGE_CONTENT['contact'])

# Créer les dossiers nécessaires au démarrage
os.makedirs('static/images/gallery', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('templates/admin', exist_ok=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)