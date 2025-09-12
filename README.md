# PRiMA PHOTO - Portfolio Photographe

Un portfolio professionnel moderne créé avec Flask pour présenter le travail photographique de PRiMA PHOTO.

## Fonctionnalités

- **Design Moderne** : Interface élégante et minimaliste adaptée aux photographes
- **Responsive** : Compatible avec tous les appareils (desktop, tablette, mobile)
- **Galerie Interactive** : Système de filtres par catégorie et lightbox
- **Formulaire de Contact** : Système de contact intégré avec validation
- **Navigation Fluide** : Animations et transitions modernes
- **SEO Optimisé** : Structure HTML sémantique

## Structure du Projet

```
Portfolio/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation
├── templates/            # Templates HTML
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   ├── gallery.html      # Galerie photos
│   ├── about.html        # Page à propos
│   └── contact.html      # Page contact
└── static/              # Fichiers statiques
    ├── css/
    │   └── style.css     # Styles CSS
    ├── js/
    │   └── script.js     # JavaScript
    └── images/           # Images du site
        └── gallery/      # Photos de la galerie
```

## Installation

1. **Cloner ou télécharger le projet**
2. **Installer Python** (version 3.7 ou supérieure)
3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. **Lancer l'application** :
   ```bash
   python app.py
   ```

2. **Ouvrir votre navigateur** et aller à : `http://localhost:5000`

## Personnalisation

### Ajouter des Photos

1. Placez vos photos dans le dossier `static/images/gallery/`
2. Modifiez la liste `GALLERY_IMAGES` dans `app.py` :
   ```python
   GALLERY_IMAGES = [
       {'filename': 'votre-photo.jpg', 'title': 'Titre', 'category': 'portrait'},
       # Ajoutez vos photos ici
   ]
   ```

### Modifier les Informations

- **Nom du photographe** : Modifiez "PRiMA PHOTO" dans les templates
- **Informations de contact** : Éditez `templates/contact.html` et `templates/base.html`
- **À propos** : Personnalisez `templates/about.html`

### Personnaliser le Design

- **Couleurs** : Modifiez les variables CSS dans `static/css/style.css`
- **Polices** : Changez les `font-family` dans le CSS
- **Layout** : Ajustez les grilles CSS Grid dans le fichier de styles

## Catégories de Photos

Le site supporte les catégories suivantes :
- Portrait
- Mariage
- Nature
- Architecture
- Mode
- Événement

Vous pouvez ajouter de nouvelles catégories en modifiant :
1. La liste `GALLERY_IMAGES` dans `app.py`
2. Les filtres dans `templates/gallery.html`

## Déploiement

Pour déployer en production :

1. **Configurez une clé secrète sécurisée** dans `app.py`
2. **Désactivez le mode debug** : `app.run(debug=False)`
3. **Utilisez un serveur WSGI** comme Gunicorn
4. **Configurez un serveur web** (Nginx, Apache)

## Technologies Utilisées

- **Backend** : Flask (Python)
- **Frontend** : HTML5, CSS3, JavaScript
- **Icons** : Font Awesome
- **Design** : CSS Grid, Flexbox
- **Responsive** : Media Queries

## Support

Pour toute question ou personnalisation, consultez la documentation Flask officielle ou contactez le développeur.

## Licence

Ce projet est libre d'utilisation pour des projets personnels et commerciaux.