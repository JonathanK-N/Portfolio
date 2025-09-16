# Configuration Cloudinary - PRiMA PHOTO

## 🔧 Étapes de configuration

### 1. Créer un compte Cloudinary
- Aller sur https://cloudinary.com
- S'inscrire gratuitement (25GB gratuits)
- Noter vos identifiants

### 2. Récupérer les clés API
Dans votre dashboard Cloudinary :
- **Cloud Name** : `votre_cloud_name`
- **API Key** : `votre_api_key` 
- **API Secret** : `votre_api_secret`

### 3. Variables d'environnement Railway
Ajouter dans Railway > Settings > Variables :

```
CLOUDINARY_CLOUD_NAME=votre_cloud_name
CLOUDINARY_API_KEY=votre_api_key
CLOUDINARY_API_SECRET=votre_api_secret
```

### 4. Installation locale (pour tester)
```bash
pip install cloudinary
```

## 📸 Fonctionnalités Cloudinary

### **Upload automatique**
- Images uploadées via l'admin → Cloudinary
- Optimisation automatique (qualité, format)
- Redimensionnement intelligent

### **Organisation**
- Dossiers : `prima_photo/gallery/portrait/`
- Dossiers : `prima_photo/about/`
- URLs permanentes

### **Avantages**
- ✅ **Stockage permanent** (pas de perte lors redéploiement)
- ✅ **CDN mondial** (chargement rapide)
- ✅ **Optimisation auto** (WebP, compression)
- ✅ **Transformations** (resize, crop, filters)
- ✅ **25GB gratuits** puis payant selon usage

## 🚀 Après configuration

1. **Tester l'upload** via l'admin
2. **Vérifier** les images dans Cloudinary dashboard
3. **Les anciennes images** restent en local (backup)

## 📱 URLs générées

Format : `https://res.cloudinary.com/votre_cloud/image/upload/prima_photo/gallery/portrait/image.jpg`

Maintenant vos images sont stockées de façon permanente dans le cloud ! 🎉