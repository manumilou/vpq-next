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

## Updating Your Site

When you make changes to your code:

```bash
# SSH into PythonAnywhere console
cd ~/vpq-next

# Pull latest changes
git pull origin main

# Activate virtualenv
workon vpq-env

# Install any new dependencies
pip install -r requirements.txt

# Run migrations if any
python manage.py migrate

# Collect static files if CSS/JS changed
python manage.py collectstatic --noinput

# Reload web app from Web tab
```

Or use the "Reload" button in the Web tab.

## Next Steps

Once your prototype is validated, you can migrate to a more robust hosting solution:

- **DigitalOcean App Platform**: Easy deployment with managed PostgreSQL
- **Railway**: Git-based deployments with PostgreSQL
- **Fly.io**: Global CDN with edge computing
- **Heroku**: Classic PaaS with many add-ons

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
