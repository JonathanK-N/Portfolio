from flask import Flask, render_template, request, flash, redirect, url_for, session
import os
import json
import base64
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from openai import OpenAI
from PIL import Image
import io

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'prima_photo_secret_key_change_in_production')

# Configuration pour les images
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 30MB max

# Configuration admin
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'prima2024')

# Configuration OpenAI (initialisé à la demande)
client = None

# Configuration Cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

def upload_to_cloudinary(file, folder="prima_photo", crop_position="center"):
    """Upload une image vers Cloudinary avec redimensionnement automatique 4:3"""
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
                {'width': 1200, 'height': 900, 'crop': 'fill', 'gravity': gravity},
                {'quality': 'auto', 'fetch_format': 'auto'}
            ]
        )
        return result['secure_url']
    except Exception as e:
        print(f"Erreur upload Cloudinary: {e}")
        return None

def analyze_image_with_openai(image_file):
    """Analyse l'image avec OpenAI pour déterminer les meilleures dimensions"""
    try:
        # Initialiser OpenAI seulement si nécessaire
        global client
        if client is None:
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                return {'width': 1200, 'height': 900, 'gravity': 'center'}
            client = OpenAI(api_key=api_key)
        
        # Convertir l'image en base64
        image = Image.open(image_file)
        original_width, original_height = image.size
        image.thumbnail((512, 512))
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Analyse cette image (dimensions originales: {original_width}x{original_height}). Détermine les meilleures dimensions pour un portfolio photographique et le cadrage optimal. Réponds au format JSON: {{\"width\": nombre, \"height\": nombre, \"gravity\": \"center/top/bottom/left/right\"}}. Choisis des dimensions qui préservent le ratio et mettent en valeur le sujet principal."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content.strip()
        # Parser la réponse JSON
        import json
        ai_result = json.loads(result)
        
        # Valider et ajuster les dimensions
        width = max(400, min(2000, ai_result.get('width', 1200)))
        height = max(300, min(1500, ai_result.get('height', 900)))
        gravity = ai_result.get('gravity', 'center')
        
        valid_positions = ['center', 'top', 'bottom', 'left', 'right']
        if gravity not in valid_positions:
            gravity = 'center'
            
        return {'width': width, 'height': height, 'gravity': gravity}
        
    except Exception as e:
        print(f"Erreur analyse OpenAI: {e}")
        return {'width': 1200, 'height': 900, 'gravity': 'center'}

def upload_with_ai_optimization(file, folder="prima_photo", default_width=1200, default_height=900):
    """Upload avec redimensionnement automatique IA"""
    try:
        # Analyser l'image avec OpenAI pour déterminer les meilleures dimensions
        file.seek(0)
        ai_analysis = analyze_image_with_openai(file)
        file.seek(0)
        
        # Utiliser les dimensions déterminées par l'IA
        optimal_width = ai_analysis['width']
        optimal_height = ai_analysis['height']
        ai_gravity = ai_analysis['gravity']
        
        # Mapping pour Cloudinary
        gravity_map = {
            'center': 'center',
            'top': 'north',
            'bottom': 'south',
            'left': 'west',
            'right': 'east'
        }
        
        cloudinary_gravity = gravity_map.get(ai_gravity, 'center')
        
        print(f"IA recommande: {optimal_width}x{optimal_height}, cadrage: {ai_gravity}")
        
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            transformation=[
                {'width': optimal_width, 'height': optimal_height, 'crop': 'fill', 'gravity': cloudinary_gravity},
                {'quality': 'auto', 'fetch_format': 'auto'}
            ]
        )
        return result['secure_url']
        
    except Exception as e:
        print(f"Erreur upload avec IA: {e}")
        # Fallback avec dimensions par défaut
        try:
            result = cloudinary.uploader.upload(
                file,
                folder=folder,
                transformation=[
                    {'width': default_width, 'height': default_height, 'crop': 'fill', 'gravity': 'center'},
                    {'quality': 'auto', 'fetch_format': 'auto'}
                ]
            )
            return result['secure_url']
        except Exception as e2:
            print(f"Erreur upload fallback: {e2}")
            return None

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def home():
    # Afficher les 8 dernières images ajoutées (les plus récentes en premier)
    recent_images = GALLERY_IMAGES[-8:]
    recent_images.reverse()  # Inverser pour avoir les plus récentes en premier
    return render_template('index.html', images=recent_images, hero_bg=PAGE_CONTENT['hero']['background_image'])

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

# Fichier de sauvegarde des données
DATA_FILE = 'portfolio_data.json'

# Données par défaut
DEFAULT_DATA = {
    'page_content': {
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
            'email': 'primaphotoproduction@gmail.com',
            'phone': '+1 819 674 5823',
            'location': 'Sherbrooke, QC, Canada',
            'hours': 'Sur rendez-vous',
            'whatsapp': '+1 819 674 5823'
        },
        'hero': {
            'background_image': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=1920&h=1080&fit=crop'

        }
    },
    'gallery_images': [
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
    ],
    'services': {
        'portrait': {
            'name': 'Portrait Professionnel',
            'price': '',
            'duration': '1-2 heures',
            'description': 'Séance portrait en studio ou extérieur avec retouches incluses',
            'includes': ['Séance photo', '10 photos retouchées', 'Galerie privée en ligne'],
            'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop'
        },
        'mariage': {
            'name': 'Photographie de Mariage',
            'price': '',
            'duration': 'Journée complète',
            'description': 'Couverture complète de votre mariage avec reportage photo',
            'includes': ['Préparatifs', 'Cérémonie', 'Cocktail', 'Soirée', '200+ photos retouchées'],
            'image': 'https://images.unsplash.com/photo-1519741497674-611481863552?w=400&h=300&fit=crop'
        },
        'evenement': {
            'name': 'Événement Corporate',
            'price': '',
            'duration': '2-4 heures',
            'description': 'Couverture photographique de vos événements professionnels',
            'includes': ['Reportage complet', 'Photos haute résolution', 'Livraison 48h'],
            'image': 'https://images.unsplash.com/photo-1511578314322-379afb476865?w=400&h=300&fit=crop'
        },
        'famille': {
            'name': 'Séance Famille',
            'price': '',
            'duration': '1 heure',
            'description': 'Séance photo famille en extérieur ou à domicile',
            'includes': ['Séance photo', '15 photos retouchées', 'Impression offerte'],
            'image': 'https://images.unsplash.com/photo-1511895426328-dc8714191300?w=400&h=300&fit=crop'
        }
    }
}

def load_data():
    """Charge les données depuis le fichier JSON"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_DATA.copy()

def save_data(data):
    """Sauvegarde les données dans le fichier JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Charger les données au démarrage
app_data = load_data()
PAGE_CONTENT = app_data['page_content']
GALLERY_IMAGES = app_data['gallery_images']
SERVICES = app_data['services']



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
            # Upload avec IA pour optimisation automatique
            cloudinary_url = upload_with_ai_optimization(file, f"prima_photo/gallery/{category}")
            
            if cloudinary_url:
                new_image = {
                    'url': cloudinary_url,
                    'title': title,
                    'category': category
                }
                GALLERY_IMAGES.append(new_image)
                
                # Sauvegarder les modifications
                app_data['gallery_images'] = GALLERY_IMAGES
                save_data(app_data)
                
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
        
        # Sauvegarder les modifications
        app_data['gallery_images'] = GALLERY_IMAGES
        save_data(app_data)
        
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
        
        # Gestion de l'image avec IA
        file = request.files.get('service_image')
        if file and allowed_file(file.filename):
            cloudinary_url = upload_with_ai_optimization(file, f"prima_photo/services/{service_key}", 400, 300)
            if cloudinary_url:
                SERVICES[service_key]['image'] = cloudinary_url
        
        # Gestion des inclusions
        includes = []
        for i in range(10):  # Max 10 inclusions
            include = request.form.get(f'include_{i}')
            if include and include.strip():
                includes.append(include.strip())
        SERVICES[service_key]['includes'] = includes
        
        # Sauvegarder les modifications
        app_data['services'] = SERVICES
        save_data(app_data)
        
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
        
        # Gestion de la photo avec IA
        file = request.files.get('photo')
        if file and allowed_file(file.filename):
            cloudinary_url = upload_with_ai_optimization(file, "prima_photo/about", 600, 800)
            if cloudinary_url:
                PAGE_CONTENT['about']['photo'] = cloudinary_url
        
        # Sauvegarder les modifications
        app_data['page_content'] = PAGE_CONTENT
        save_data(app_data)
        
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
        
        # Sauvegarder les modifications
        app_data['page_content'] = PAGE_CONTENT
        save_data(app_data)
        
        flash('Page Contact mise à jour !', 'success')
        return redirect(url_for('admin_pages'))
    
    return render_template('admin/edit_contact.html', content=PAGE_CONTENT['contact'])

@app.route('/admin/pages/hero', methods=['GET', 'POST'])
def admin_edit_hero():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        file = request.files.get('background_image')
        if file and allowed_file(file.filename):
            cloudinary_url = upload_with_ai_optimization(file, "prima_photo/hero", 1920, 1080)
            if cloudinary_url:
                PAGE_CONTENT['hero']['background_image'] = cloudinary_url
                
                # Sauvegarder les modifications
                app_data['page_content'] = PAGE_CONTENT
                save_data(app_data)
                
                flash('Image de fond mise à jour !', 'success')
            else:
                flash('Erreur lors de l\'upload', 'error')
        else:
            flash('Fichier invalide', 'error')
        
        return redirect(url_for('admin_pages'))
    
    return render_template('admin/edit_hero.html', content=PAGE_CONTENT['hero'])

# Créer les dossiers nécessaires au démarrage
os.makedirs('static/images/gallery', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('templates/admin', exist_ok=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)