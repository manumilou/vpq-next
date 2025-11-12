# Railway Deployment Guide

Complete guide to deploy Victimes des Pesticides du Québec from PythonAnywhere to Railway.

## Prerequisites

- Git repository pushed to GitHub (✅ Done: https://github.com/manumilou/vpq-next.git)
- Railway account (sign up at https://railway.app)
- Access to your PythonAnywhere MySQL database

---

## Part 1: Export Data from PythonAnywhere

### Step 1: Export Database

On PythonAnywhere Bash console:

```bash
cd ~/vpq-next
workon vpq-env

# Export to Django JSON format (easier to import to PostgreSQL)
python manage.py dumpdata \
  --natural-foreign \
  --natural-primary \
  --exclude contenttypes \
  --exclude auth.permission \
  --exclude sessions \
  --indent 2 \
  > vpq_data.json

# Download this file to your local machine
# You can use the Files tab in PythonAnywhere to download it
```

**Alternative: Export specific apps only**
```bash
# If full export is too large, export by app:
python manage.py dumpdata home --natural-foreign --indent 2 > home_data.json
python manage.py dumpdata actualites --natural-foreign --indent 2 > actualites_data.json
python manage.py dumpdata pages_app --natural-foreign --indent 2 > pages_app_data.json
python manage.py dumpdata wagtailcore --natural-foreign --indent 2 > wagtailcore_data.json
python manage.py dumpdata wagtailimages --natural-foreign --indent 2 > wagtailimages_data.json
```

### Step 2: Download Media Files

```bash
# Create a tarball of media files
cd ~/vpq-next
tar -czf media_backup.tar.gz media/

# Download via Files tab or SCP
```

---

## Part 2: Set Up Railway

### Step 1: Create Railway Project

1. Go to https://railway.app
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose **"manumilou/vpq-next"** repository
6. Railway will auto-detect Django

### Step 2: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically:
   - Create a PostgreSQL database
   - Generate a `DATABASE_URL` environment variable
   - Link it to your Django app

### Step 3: Configure Environment Variables

In Railway dashboard, go to your Django service → **Variables** tab:

Add these variables:

```bash
DJANGO_SETTINGS_MODULE=victimes_pesticides.settings.railway

SECRET_KEY=<generate-new-secret-key>

# Optional: Set to True temporarily for initial setup debugging
DEBUG=False

# Railway provides DATABASE_URL automatically - don't set it manually

# Your Wagtail admin URL (will be your Railway URL initially)
WAGTAILADMIN_BASE_URL=https://your-app.up.railway.app

# Python version
PYTHON_VERSION=3.10
```

**Generate SECRET_KEY locally:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Deploy

Railway will automatically deploy when you:
1. Push to GitHub `main` branch, OR
2. Click **"Deploy"** in Railway dashboard

Watch the deployment logs in Railway.

---

## Part 3: Import Data to Railway

### Step 1: Access Railway Shell

Install Railway CLI:
```bash
# macOS
brew install railway

# Or via npm
npm i -g @railway/cli
```

Login and link to project:
```bash
railway login
railway link  # Select your project
```

### Step 2: Run Migrations

```bash
# Run migrations to create database schema
railway run python manage.py migrate
```

### Step 3: Create Superuser

```bash
# Create a new superuser for Railway
railway run python manage.py createsuperuser
```

### Step 4: Import Data

Upload your `vpq_data.json` to your repo or use Railway CLI:

```bash
# Option 1: If you committed vpq_data.json to repo
railway run python manage.py loaddata vpq_data.json

# Option 2: Upload and import via Railway shell
railway run python manage.py shell
>>> from django.core.management import call_command
>>> call_command('loaddata', '/path/to/vpq_data.json')
```

**If you exported by app:**
```bash
railway run python manage.py loaddata wagtailcore_data.json
railway run python manage.py loaddata wagtailimages_data.json
railway run python manage.py loaddata home_data.json
railway run python manage.py loaddata actualites_data.json
railway run python manage.py loaddata pages_app_data.json
```

### Step 5: Upload Media Files

**Option 1: Use Railway Volumes (Recommended for small sites)**

1. In Railway project, add a Volume:
   - Click **"+ New"** → **"Volume"**
   - Mount path: `/app/media`
   - Link to your Django service

2. Upload media files:
```bash
# Extract your media backup locally
tar -xzf media_backup.tar.gz

# Use Railway CLI to copy files (requires setting up volume mount)
# Or manually upload via SFTP/SCP once Railway volume is mounted
```

**Option 2: Use External Storage (Recommended for larger sites)**

Consider DigitalOcean Spaces, AWS S3, or Cloudinary for media files:
- Install `django-storages` and `boto3`
- Configure in `railway.py` settings
- Upload media to storage bucket

---

## Part 4: Post-Deployment

### Step 1: Verify Deployment

1. Visit your Railway URL: `https://your-app.up.railway.app`
2. Check homepage loads correctly
3. Test admin: `https://your-app.up.railway.app/admin/`
4. Verify news articles: `/actualites/`
5. Test donation page: `/soutenez-vpq/`

### Step 2: Update Wagtail Site Settings

```bash
railway run python manage.py shell
```

Then in shell:
```python
from wagtail.models import Site
site = Site.objects.get(is_default_site=True)
site.hostname = 'your-app.up.railway.app'  # Or your custom domain
site.port = 80
site.save()
print(f"Site updated: {site.hostname}")
exit()
```

### Step 3: Run Management Commands

Re-populate content if needed:
```bash
railway run python manage.py update_donation_page
railway run python manage.py reimport_actualites
```

### Step 4: Collect Static Files

```bash
railway run python manage.py collectstatic --noinput
```

---

## Part 5: Custom Domain (Optional)

### Step 1: Configure Custom Domain in Railway

1. Go to your Django service in Railway
2. Click **Settings** → **Networking**
3. Under **Custom Domains**, click **"Generate Domain"** or add your own
4. Railway provides a CNAME target

### Step 2: Update DNS

At your domain registrar (e.g., Namecheap, GoDaddy):

```
Type: CNAME
Name: www
Target: <railway-provided-cname>

Type: CNAME  (or ALIAS/ANAME for root domain)
Name: @
Target: <railway-provided-cname>
```

### Step 3: Update Settings

Update environment variables in Railway:
```bash
WAGTAILADMIN_BASE_URL=https://victimespesticidesquebec.org
```

Update Wagtail site settings:
```bash
railway run python manage.py shell
```
```python
from wagtail.models import Site
site = Site.objects.get(is_default_site=True)
site.hostname = 'victimespesticidesquebec.org'
site.save()
```

---

## Part 6: Monitoring & Maintenance

### View Logs
```bash
railway logs
```

Or in Railway dashboard → Service → **Logs** tab

### Database Backups

Railway PostgreSQL includes automatic backups. You can also:

```bash
# Manual backup
railway run python manage.py dumpdata --natural-foreign --indent 2 > backup_$(date +%Y%m%d).json
```

### Scale Resources

In Railway dashboard → Service → **Settings** → **Resources**:
- Adjust memory/CPU as needed
- Monitor usage in **Metrics** tab

### Deploy Updates

```bash
# Push to GitHub main branch
git push origin main

# Railway auto-deploys
# Or manually trigger in Railway dashboard
```

---

## Troubleshooting

### Issue: Deployment Fails

**Check logs:**
```bash
railway logs
```

**Common fixes:**
- Verify `DJANGO_SETTINGS_MODULE=victimes_pesticides.settings.railway`
- Check SECRET_KEY is set
- Ensure DATABASE_URL is provided by PostgreSQL service

### Issue: Static Files Not Loading

**Run collectstatic:**
```bash
railway run python manage.py collectstatic --noinput
```

**Verify WhiteNoise is in MIDDLEWARE** (already configured in railway.py)

### Issue: Media Files Not Showing

- Check media files were uploaded to Railway Volume
- Or configure external storage (S3, Spaces)

### Issue: Database Import Errors

**Try importing in smaller chunks:**
```bash
railway run python manage.py loaddata wagtailcore_data.json
# Then import other apps one by one
```

**Or use fresh migrations + management commands:**
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py update_donation_page
railway run python manage.py reimport_actualites
```

---

## Cost Estimate

Railway pricing (as of 2024):

- **Hobby Plan**: $5/month
  - 512 MB RAM, shared CPU
  - PostgreSQL included
  - Good for low-traffic sites

- **Pro Plan**: $20/month
  - More resources
  - Priority support
  - Better for growing traffic

**Your estimated cost: $5-10/month** (Hobby plan should be sufficient)

---

## Rollback Plan

If issues occur, PythonAnywhere site is still running. You can:

1. Keep PythonAnywhere live during Railway testing
2. Update DNS only when Railway is fully validated
3. PythonAnywhere can serve as backup

---

## Next Steps After Migration

1. ✅ Test all functionality on Railway
2. ✅ Point DNS to Railway
3. ✅ Monitor for 24-48 hours
4. 🗑️ Decommission PythonAnywhere once stable

---

## Support

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/

---

**Ready to deploy!** 🚀

Start with Part 1 (Export from PythonAnywhere) and work through each section.
