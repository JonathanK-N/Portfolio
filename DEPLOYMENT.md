# Déploiement Railway - PRiMA PHOTO

## 📋 Étapes de déploiement

### 1. Préparer le projet
✅ Tous les fichiers sont prêts dans le dossier Portfolio/

### 2. Créer un compte Railway
- Aller sur https://railway.app
- Se connecter avec GitHub

### 3. Déployer le projet
1. Cliquer sur "New Project"
2. Sélectionner "Deploy from GitHub repo"
3. Connecter votre repository GitHub
4. Sélectionner le dossier Portfolio/

### 4. Variables d'environnement (IMPORTANT)
Dans Railway, aller dans Settings > Variables et ajouter :

```
SECRET_KEY=votre_cle_secrete_super_forte_ici
ADMIN_USERNAME=votre_nom_admin
ADMIN_PASSWORD=votre_mot_de_passe_fort
```

### 5. Domaine personnalisé (optionnel)
- Aller dans Settings > Domains
- Ajouter votre domaine personnalisé

## 🔧 Fichiers créés pour le déploiement

- `Procfile` : Commande de démarrage
- `runtime.txt` : Version Python
- `requirements.txt` : Dépendances (avec Gunicorn)
- `railway.json` : Configuration Railway
- `.gitignore` : Fichiers à ignorer
- `app.py` : Modifié pour la production

## 🚀 Après déploiement

1. **Tester l'admin** : `https://votre-app.railway.app/admin`
2. **Changer les mots de passe** via les variables d'environnement
3. **Ajouter vos vraies images** via l'interface admin
4. **Configurer votre WhatsApp** dans la page Contact

## 📱 URLs importantes

- Site principal : `https://votre-app.railway.app`
- Administration : `https://votre-app.railway.app/admin`
- Galerie : `https://votre-app.railway.app/galerie`
- Services : `https://votre-app.railway.app/services`

## 🔒 Sécurité

- Changez OBLIGATOIREMENT les mots de passe par défaut
- Utilisez une clé secrète forte et unique
- Gardez vos variables d'environnement privées

## 💡 Support

En cas de problème :
1. Vérifier les logs dans Railway
2. Vérifier les variables d'environnement
3. S'assurer que tous les fichiers sont bien uploadés