# PRiMA PHOTO - Portfolio Photographe Professionnel

🎯 **Portfolio photographique moderne avec administration complète et stockage cloud**

Un portfolio professionnel créé avec Flask, incluant un panneau d'administration complet et l'intégration Cloudinary pour le stockage permanent des images.

## ✨ Fonctionnalités Principales

### 🎨 **Frontend**
- **Design Moderne** : Interface élégante et minimaliste adaptée aux photographes
- **Responsive** : Compatible avec tous les appareils (desktop, tablette, mobile)
- **Galerie Interactive** : Système de filtres par catégorie et lightbox
- **Réservation WhatsApp** : Système de réservation automatique via WhatsApp
- **Pages Dynamiques** : Contenu modifiable via l'administration
- **SEO Optimisé** : Structure HTML sémantique

### 🛠️ **Administration**
- **Panneau Admin Complet** : Interface d'administration moderne
- **Gestion Galerie** : Ajout/suppression d'images avec cadrage personnalisé
- **Gestion Services** : Modification des prix, descriptions, prestations
- **Gestion Pages** : Édition des pages À Propos et Contact
- **Upload Intelligent** : Images jusqu'à 30MB avec aperçu et cadrage
- **Stockage Cloud** : Intégration Cloudinary pour images permanentes

### 📱 **Fonctionnalités Avancées**
- **WhatsApp Integration** : Réservations automatiques avec détails pré-remplis
- **Cloudinary CDN** : Images optimisées et servies via CDN mondial
- **Variables d'Environnement** : Configuration sécurisée pour production
- **Prêt Railway** : Déploiement one-click sur Railway

## 🏗️ Structure du Projet

```
Portfolio/
├── app.py                    # Application Flask principale
├── requirements.txt          # Dépendances Python + Cloudinary
├── Procfile                  # Configuration Railway
├── railway.json              # Configuration déploiement
├── runtime.txt               # Version Python
├── .gitignore               # Fichiers à ignorer
├── DEPLOYMENT.md            # Guide de déploiement
├── CLOUDINARY_SETUP.md      # Guide Cloudinary
├── templates/               # Templates HTML
│   ├── base.html            # Template de base
│   ├── index.html           # Page d'accueil
│   ├── gallery.html         # Galerie photos
│   ├── about.html           # Page à propos (dynamique)
│   ├── contact.html         # Page contact (dynamique)
│   ├── services.html        # Page services
│   ├── book_service.html    # Formulaire réservation
│   └── admin/               # Templates administration
│       ├── login.html       # Connexion admin
│       ├── dashboard.html   # Tableau de bord
│       ├── gallery.html     # Gestion galerie
│       ├── add_image.html   # Ajout d'images
│       ├── services.html    # Gestion services
│       ├── edit_service.html # Édition service
│       ├── pages.html       # Gestion pages
│       ├── edit_about.html  # Édition À Propos
│       └── edit_contact.html # Édition Contact
└── static/                  # Fichiers statiques
    ├── css/
    │   ├── style.css        # Styles frontend
    │   └── admin.css        # Styles administration
    ├── js/
    │   └── script.js        # JavaScript frontend
    └── images/              # Images locales (backup)
```

## 🚀 Installation et Utilisation

### **Installation Locale**

1. **Cloner le projet**
   ```bash
   git clone https://github.com/JonathanK-N/prima-photo-portfolio.git
   cd prima-photo-portfolio
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python app.py
   ```

4. **Accéder au site**
   - Site : `http://localhost:5000`
   - Admin : `http://localhost:5000/admin`
   - Identifiants : `admin` / `prima2024`

### **Déploiement Production (Railway)**

1. **Configurer Cloudinary** (voir `CLOUDINARY_SETUP.md`)
2. **Variables d'environnement Railway** :
   ```
   SECRET_KEY=votre_cle_secrete_forte
   ADMIN_USERNAME=votre_admin
   ADMIN_PASSWORD=votre_mot_de_passe
   CLOUDINARY_CLOUD_NAME=votre_cloud_name
   CLOUDINARY_API_KEY=votre_api_key
   CLOUDINARY_API_SECRET=votre_api_secret
   ```
3. **Déployer** : Connecter le repo GitHub à Railway

## 🎛️ Administration

### **Accès Admin**
- **URL** : `/admin`
- **Fonctionnalités** :
  - 📊 Tableau de bord avec statistiques
  - 🖼️ Gestion complète de la galerie
  - ⚙️ Configuration des services et tarifs
  - 📄 Édition des pages À Propos et Contact
  - 📱 Configuration WhatsApp

### **Gestion des Images**
- **Upload** : Jusqu'à 30MB par image
- **Cadrage** : 5 options (centré, haut, bas, gauche, droite)
- **Stockage** : Cloudinary avec CDN mondial
- **Formats** : JPG, PNG, GIF
- **Optimisation** : Automatique (WebP, compression)

## 📋 Catégories Supportées

- **Portrait** : Portraits professionnels et artistiques
- **Mariage** : Photographie de mariage complète
- **Nature** : Paysages et photographie nature
- **Architecture** : Photographie architecturale
- **Mode** : Fashion et lifestyle
- **Événement** : Événements corporate et privés

## 🛡️ Sécurité

- **Variables d'environnement** pour les secrets
- **Sessions sécurisées** pour l'administration
- **Validation des fichiers** uploadés
- **Protection CSRF** intégrée Flask
- **Stockage cloud sécurisé** Cloudinary

## 🔧 Technologies

### **Backend**
- **Flask 2.3.3** : Framework web Python
- **Cloudinary** : Stockage et optimisation d'images
- **Gunicorn** : Serveur WSGI pour production
- **Werkzeug** : Utilitaires web et sécurité

### **Frontend**
- **HTML5 Sémantique** : Structure moderne
- **CSS3 Grid/Flexbox** : Layout responsive
- **JavaScript Vanilla** : Interactions fluides
- **Font Awesome 6** : Icônes professionnelles

### **Déploiement**
- **Railway** : Plateforme de déploiement
- **Git** : Contrôle de version
- **Variables d'environnement** : Configuration sécurisée

## 📱 URLs Principales

- **Accueil** : `/`
- **Galerie** : `/galerie`
- **Services** : `/services`
- **À Propos** : `/a-propos`
- **Contact** : `/contact`
- **Administration** : `/admin`
- **Réservation** : `/reserver/<service>`

## 🎯 Fonctionnalités Uniques

- **Réservation WhatsApp** : Messages pré-formatés automatiques
- **Cadrage Intelligent** : Aperçu et ajustement avant upload
- **Administration Complète** : Gestion 100% du contenu
- **Stockage Permanent** : Plus de perte d'images lors des redéploiements
- **Optimisation Automatique** : Images servies via CDN mondial

## 📞 Support

- **Documentation** : Fichiers `DEPLOYMENT.md` et `CLOUDINARY_SETUP.md`
- **Issues** : GitHub Issues pour les bugs
- **Configuration** : Variables d'environnement documentées

## 📄 Licence

Ce projet est libre d'utilisation pour des projets personnels et commerciaux.

---

**Développé avec ❤️ pour les photographes professionnels**