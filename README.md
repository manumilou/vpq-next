# Victimes des Pesticides du Québec

Site web pour l'organisation Victimes des Pesticides du Québec, construit avec Wagtail CMS.

## Technologies

- **Python 3.13**
- **Django 5.2.7**
- **Wagtail 7.1.2** - CMS moderne et flexible
- **SQLite** (développement) / **PostgreSQL** (production)
- Interface d'administration entièrement en français

## Fonctionnalités

- **Gestion d'actualités** avec catégories, auteurs, et images
- **Pages d'information** avec contenu flexible (StreamField)
- **Formulaire de contact** intégré
- **Interface d'édition drag & drop** pour les contenus
- **Gestion de médias** (images, documents)
- **Optimisé pour SEO** et mobile-first
- **Authentification sécurisée** pour les éditeurs

## Installation

### Prérequis

- Python 3.13 ou supérieur
- pip (gestionnaire de paquets Python)

### Configuration locale

1. Cloner le dépôt et naviguer dans le répertoire :
```bash
cd victimes-pesticides-quebec
```

2. Créer un environnement virtuel et l'activer :
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Appliquer les migrations de base de données :
```bash
python manage.py migrate
```

5. Créer un compte administrateur :
```bash
python manage.py createsuperuser
```

6. Démarrer le serveur de développement :
```bash
python manage.py runserver
```

Le site sera accessible à : http://127.0.0.1:8000  
L'interface d'administration Wagtail : http://127.0.0.1:8000/admin

## Structure du projet

```
victimes-pesticides-quebec/
├── actualites/              # App pour les actualités
│   ├── models.py           # Modèles: ActualitePage, Categorie, Auteur
│   └── templates/          # Templates HTML pour actualités
├── pages_app/              # App pour les pages standards
│   ├── models.py           # Modèles: StandardPage, ContactPage
│   └── templates/          # Templates HTML pour pages
├── home/                   # App pour la page d'accueil
│   ├── models.py           # Modèle: HomePage
│   └── templates/          # Template de la page d'accueil
├── victimes_pesticides/    # Configuration Django
│   ├── settings/           # Paramètres (base, dev, production)
│   ├── static/             # Fichiers statiques (CSS, JS)
│   └── templates/          # Templates de base
└── requirements.txt        # Dépendances Python
```

## Utilisation

### Créer du contenu

1. Connectez-vous à l'admin : http://127.0.0.1:8000/admin
2. Pour créer une actualité :
   - Allez dans "Pages" → Créez une "Page d'index des actualités" (si pas déjà créée)
   - Sous cette page, créez des "Actualité"
3. Pour créer une page d'information :
   - Créez une "Page standard" n'importe où dans l'arborescence
4. Pour le formulaire de contact :
   - Créez une "Page de contact"
   - Ajoutez les champs du formulaire (nom, email, message, etc.)

### Gérer les catégories et auteurs

1. Dans l'admin, allez dans "Snippets"
2. Créez des "Catégories" pour organiser les actualités
3. Créez des "Auteurs" avec leurs informations

### StreamField - Contenu flexible

Le StreamField permet de construire des pages avec des blocs :
- **Paragraphe** : Texte enrichi avec formatage
- **Titre** : Titre de section
- **Image** : Image avec légende
- **Citation** : Bloc de citation
- **Appel à l'action** : Bouton avec lien
- **HTML brut** : Pour du contenu personnalisé

## Configuration

### Paramètres importants

Les paramètres se trouvent dans `victimes_pesticides/settings/`:

- `base.py` : Paramètres communs
- `dev.py` : Paramètres de développement
- `production.py` : Paramètres de production

**Variables d'environnement importantes pour la production :**

```bash
DJANGO_SECRET_KEY=votre-clé-secrète
DJANGO_DEBUG=False
DATABASE_URL=postgres://user:pass@host:port/dbname
ALLOWED_HOSTS=victimes-pesticides.qc.ca
```

### Localisation française

Le site est entièrement configuré en français :
- `LANGUAGE_CODE = 'fr-ca'`
- `TIME_ZONE = 'America/Montreal'`
- Interface d'administration en français
- Tous les modèles avec labels français

## Déploiement

### Option 1 : Railway

1. Créer un compte sur [Railway](https://railway.app)
2. Connecter votre dépôt GitHub
3. Ajouter une base de données PostgreSQL
4. Configurer les variables d'environnement
5. Railway détectera automatiquement Django et déploiera

### Option 2 : Render

1. Créer un compte sur [Render](https://render.com)
2. Créer un nouveau "Web Service"
3. Connecter votre dépôt
4. Ajouter une base de données PostgreSQL
5. Configurer les variables d'environnement

### Variables d'environnement requises

```
DJANGO_SECRET_KEY=générer-avec-get_random_secret_key
DJANGO_DEBUG=False
DJANGO_SETTINGS_MODULE=victimes_pesticides.settings.production
DATABASE_URL=fourni-par-votre-hébergeur
ALLOWED_HOSTS=votre-domaine.com
```

## Commandes utiles

```bash
# Créer des migrations après modification des modèles
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques pour la production
python manage.py collectstatic

# Créer une sauvegarde de la base de données
python manage.py dumpdata > backup.json

# Restaurer une sauvegarde
python manage.py loaddata backup.json
```

## Développement

### Ajouter un nouveau type de contenu

1. Créer une nouvelle app Django (optionnel) :
```bash
python manage.py startapp nom_app
```

2. Ajouter l'app à `INSTALLED_APPS` dans `settings/base.py`

3. Créer vos modèles dans `models.py` en héritant de `Page` ou `models.Model`

4. Créer les templates correspondants

5. Créer et appliquer les migrations :
```bash
python manage.py makemigrations
python manage.py migrate
```

## Support et documentation

- [Documentation Wagtail](https://docs.wagtail.org/)
- [Documentation Django](https://docs.djangoproject.com/)
- [Guide StreamField](https://docs.wagtail.org/en/stable/topics/streamfield.html)

## Licence

Ce projet est développé pour l'organisation Victimes des Pesticides du Québec.
