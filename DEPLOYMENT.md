# Deployment Guide - PythonAnywhere

This guide walks you through deploying the Victimes des Pesticides du Québec website to PythonAnywhere for the prototyping phase.

## Prerequisites

- A PythonAnywhere account (free or paid)
- Git repository with your code pushed to GitHub
- Basic familiarity with the command line

## Step 1: Set Up PythonAnywhere Account

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Choose a username (this will be part of your URL: `yourusername.pythonanywhere.com`)
3. Verify your email address

## Step 2: Create MySQL Database

1. Go to the **Databases** tab in PythonAnywhere
2. Under "Create a new database", choose MySQL
3. Set a MySQL password (save this - you'll need it later)
4. Create a new database with a name like `yourusername$vpq`
5. Note down your database details:
   - Database name: `yourusername$vpq`
   - Username: `yourusername`
   - Host: `yourusername.mysql.pythonanywhere-services.com`

## Step 3: Clone Your Repository

1. Go to the **Consoles** tab
2. Start a new **Bash console**
3. Clone your repository:

```bash
git clone https://github.com/manumilou/vpq-next.git
cd vpq-next
```

## Step 4: Set Up Python Virtual Environment

```bash
# Create virtual environment with Python 3.10 or 3.11
mkvirtualenv --python=/usr/bin/python3.10 vpq-env

# Activate it (should happen automatically, but if not):
workon vpq-env

# Install dependencies
pip install -r requirements.txt
```

## Step 5: Configure Environment Variables

Create a `.env` file in your project root:

```bash
nano .env
```

Copy the contents from `.env.example` and fill in your actual values:

```bash
# Django settings
SECRET_KEY=your-generated-secret-key-here
DEBUG=False

# Allowed hosts
ALLOWED_HOSTS=yourusername.pythonanywhere.com

# Database configuration
DATABASE_NAME=yourusername$vpq
DATABASE_USER=yourusername
DATABASE_PASSWORD=your-mysql-password
DATABASE_HOST=yourusername.mysql.pythonanywhere-services.com
DATABASE_PORT=3306

# Static and media files
STATIC_ROOT=/home/yourusername/vpq-next/static
MEDIA_ROOT=/home/yourusername/vpq-next/media

# Security settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Wagtail admin base URL
WAGTAILADMIN_BASE_URL=https://yourusername.pythonanywhere.com
```

**To generate a new SECRET_KEY**, run in the console:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Save and exit (Ctrl+X, then Y, then Enter).

## Step 6: Run Database Migrations

```bash
# Set the Django settings module
export DJANGO_SETTINGS_MODULE=victimes_pesticides.settings.pythonanywhere

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## Step 7: Import Sample Content (Optional)

If you want to populate the homepage with sample content:

```bash
# Import hero images (if you have them in home/management/commands/)
python manage.py import_hero_images

# Set up mobile-first homepage
python manage.py setup_mobile_first_homepage

# Update hero image (if you have the specific image)
python manage.py update_hero_image
```

## Step 8: Configure WSGI File

1. Go to the **Web** tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose "Manual configuration" (not Django - we'll configure it ourselves)
4. Choose Python 3.10 or 3.11
5. Once created, scroll down to the **Code** section
6. Click on the WSGI configuration file link
7. Delete everything and replace with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/vpq-next'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'victimes_pesticides.settings.pythonanywhere'

# Load environment variables from .env file
from pathlib import Path
env_file = Path('/home/yourusername/vpq-next/.env')
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Replace `yourusername` with your actual PythonAnywhere username.

## Step 9: Configure Static Files

Still in the **Web** tab, scroll to the **Static files** section:

| URL          | Directory                                    |
|--------------|----------------------------------------------|
| `/static/`   | `/home/yourusername/vpq-next/static`        |
| `/media/`    | `/home/yourusername/vpq-next/media`         |

Click the checkmark to add each mapping.

## Step 10: Configure Virtualenv

In the **Web** tab, scroll to the **Virtualenv** section:

Enter: `/home/yourusername/.virtualenvs/vpq-env`

## Step 11: Reload Your Web App

1. At the top of the **Web** tab, click the big green **Reload** button
2. Wait for it to finish reloading
3. Visit your site at `https://yourusername.pythonanywhere.com`

## Step 12: Access Admin Interface

1. Go to `https://yourusername.pythonanywhere.com/admin/`
2. Log in with the superuser credentials you created
3. Start managing your content!

## Troubleshooting

### Site Not Loading

1. Check the **Error log** and **Server log** in the Web tab
2. Common issues:
   - Wrong virtualenv path
   - Missing environment variables
   - Database connection issues
   - Incorrect WSGI configuration

### Static Files Not Loading

1. Make sure you ran `python manage.py collectstatic`
2. Check the static files mappings in the Web tab
3. Verify `STATIC_ROOT` in your `.env` file

### Database Connection Errors

1. Verify your MySQL password is correct
2. Check the database name format: `yourusername$dbname`
3. Ensure the database host is correct

### ImportError or ModuleNotFoundError

1. Make sure your virtualenv is activated: `workon vpq-env`
2. Reinstall requirements: `pip install -r requirements.txt`
3. Check the virtualenv path in the Web tab

## Mise à jour du site (Déploiement d'une nouvelle version)

### Procédure complète de déploiement

Quand vous faites des changements à votre code et que vous voulez les déployer sur PythonAnywhere:

#### Étape 1: Préparer les changements localement

```bash
# Sur votre machine locale, assurez-vous que tout fonctionne
source venv/bin/activate
python manage.py check
python manage.py test  # Si vous avez des tests

# Commitez vos changements
git add .
git commit -m "Description de vos changements"
git push origin main
```

#### Étape 2: Se connecter à PythonAnywhere

1. Allez sur [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Connectez-vous à votre compte
3. Allez dans l'onglet **Consoles**
4. Ouvrez une console Bash (ou réutilisez une existante)

#### Étape 3: Mettre à jour le code

```bash
# Naviguer vers votre projet
cd ~/vpq-next

# Activer l'environnement virtuel
workon vpq-env

# Récupérer les derniers changements
git pull origin main
```

#### Étape 4: Installer les nouvelles dépendances (si nécessaire)

```bash
# Installer les nouvelles dépendances si requirements.txt a changé
pip install -r requirements.txt
```

#### Étape 5: Appliquer les migrations de base de données (si nécessaire)

```bash
# Exporter la variable d'environnement pour les settings
export DJANGO_SETTINGS_MODULE=victimes_pesticides.settings.pythonanywhere

# Vérifier s'il y a des migrations à appliquer
python manage.py showmigrations

# Appliquer les migrations
python manage.py migrate
```

#### Étape 6: Collecter les fichiers statiques (si CSS/JS/images ont changé)

```bash
# Collecter tous les fichiers statiques
python manage.py collectstatic --noinput
```

#### Étape 7: Recharger l'application web

1. Allez dans l'onglet **Web** de PythonAnywhere
2. Cliquez sur le gros bouton vert **Reload** en haut de la page
3. Attendez quelques secondes que le rechargement se termine

#### Étape 8: Vérifier le déploiement

1. Visitez votre site : `https://yourusername.pythonanywhere.com`
2. Vérifiez que vos changements sont bien appliqués
3. Consultez les logs en cas de problème (voir section Troubleshooting)

### Script de déploiement rapide

Pour simplifier le processus, vous pouvez créer un script bash:

```bash
# Créer le fichier deploy.sh
nano ~/vpq-next/deploy.sh
```

Contenu du fichier:

```bash
#!/bin/bash
echo "🚀 Déploiement en cours..."

# Aller dans le répertoire du projet
cd ~/vpq-next

# Activer l'environnement virtuel
source ~/.virtualenvs/vpq-env/bin/activate

# Tirer les derniers changements
echo "📥 Récupération des changements..."
git pull origin main

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt --quiet

# Appliquer les migrations
echo "🗄️  Application des migrations..."
export DJANGO_SETTINGS_MODULE=victimes_pesticides.settings.pythonanywhere
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✅ Déploiement terminé!"
echo "⚠️  N'oubliez pas de cliquer sur 'Reload' dans l'onglet Web!"
```

Rendre le script exécutable:

```bash
chmod +x ~/vpq-next/deploy.sh
```

Utilisation:

```bash
~/vpq-next/deploy.sh
```

### Checklist de déploiement

- [ ] Code testé localement
- [ ] Changements committés et pushés sur GitHub
- [ ] Console Bash ouverte sur PythonAnywhere
- [ ] Virtualenv activé
- [ ] `git pull` exécuté
- [ ] Nouvelles dépendances installées (si nécessaire)
- [ ] Migrations appliquées (si nécessaire)
- [ ] Fichiers statiques collectés (si nécessaire)
- [ ] Application web rechargée via l'onglet Web
- [ ] Site vérifié et fonctionnel

### Fréquence des déploiements

- **Petits changements (CSS, texte)**: Immédiat après commit
- **Nouvelles fonctionnalités**: Après tests complets
- **Changements de modèles**: Toujours avec migrations
- **Urgences/Corrections**: Dès que possible

### Rollback (Retour en arrière)

En cas de problème après un déploiement:

```bash
# Voir l'historique git
git log --oneline -5

# Revenir à la version précédente
git checkout [hash-du-commit-précédent]

# Ou créer une nouvelle branche
git revert HEAD

# Puis redéployer
python manage.py migrate
python manage.py collectstatic --noinput
```

N'oubliez pas de recharger l'application dans l'onglet Web!

## Next Steps

Once your prototype is validated, you can migrate to a more robust hosting solution like:

- **DigitalOcean App Platform**: Easy deployment with managed PostgreSQL
- **Render**: Free tier available, easy setup
- **Fly.io**: Global CDN with edge computing

All these platforms support easy migration from your current setup. You'll mainly need to:
1. Export your MySQL database to PostgreSQL format
2. Update your settings to use PostgreSQL
3. Transfer your media files to object storage (S3, DigitalOcean Spaces, etc.)

## Security Reminders

- Never commit your `.env` file to Git
- Use strong passwords for your superuser and MySQL
- Keep your SECRET_KEY secret
- Regularly update your dependencies: `pip install --upgrade -r requirements.txt`
- Enable HSTS in production (uncomment lines in `pythonanywhere.py` after testing)

## Support

- PythonAnywhere Help: https://help.pythonanywhere.com/
- Django Documentation: https://docs.djangoproject.com/
- Wagtail Documentation: https://docs.wagtail.org/

---

**Good luck with your deployment!** 🚀
