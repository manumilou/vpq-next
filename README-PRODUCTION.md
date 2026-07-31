# Production deployment — `www.victimespesticidesquebec.org`

This checklist explains how to put the VPQ site in production on the real domain:

```text
https://www.victimespesticidesquebec.org/
```

It assumes the site already works on PythonAnywhere at:

```text
https://vpq.pythonanywhere.com/
```

## 1. Deploy the latest code on PythonAnywhere

Open a Bash console on PythonAnywhere:

```bash
cd ~/vpq-next
workon vpq-env

git pull origin main

pip install -r requirements.txt

export DJANGO_SETTINGS_MODULE=victimes_pesticides.settings.pythonanywhere
python manage.py migrate
python manage.py collectstatic --noinput
```

Then reload the web app from the PythonAnywhere **Web** tab.

> Note: always run `migrate` after pulling code. Some content/admin changes, such as new Wagtail StreamField choices, are tracked through migrations.

## 2. Add the real domain in PythonAnywhere

In PythonAnywhere:

1. Go to **Web**.
2. Add or configure a custom domain web app for:

```text
www.victimespesticidesquebec.org
```

3. Use the same project configuration as the existing PythonAnywhere site:

```text
Source code: /home/vpq/vpq-next
Virtualenv:  /home/vpq/.virtualenvs/vpq-env
```

If the PythonAnywhere username is different, replace `/home/vpq/` with the correct home path.

4. The WSGI file should set:

```python
os.environ['DJANGO_SETTINGS_MODULE'] = 'victimes_pesticides.settings.pythonanywhere'
```

5. Static file mappings should be:

```text
/static/ -> /home/vpq/vpq-next/static
/media/  -> /home/vpq/vpq-next/media
```

Again, adjust `/home/vpq/` if needed.

## 3. Update `.env` on PythonAnywhere

Edit the production environment file:

```bash
nano ~/vpq-next/.env
```

Make sure these values include the real domain:

```env
DEBUG=False

ALLOWED_HOSTS=www.victimespesticidesquebec.org,victimespesticidesquebec.org,vpq.pythonanywhere.com

WAGTAILADMIN_BASE_URL=https://www.victimespesticidesquebec.org

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

Save the file, then reload the web app in PythonAnywhere.

## 4. Update DNS at the domain registrar

For the `www` domain, create a CNAME record:

```text
www  CNAME  <target provided by PythonAnywhere>
```

Use the exact CNAME target shown in the PythonAnywhere **Web** tab. It may look similar to:

```text
webapp-xxxx.pythonanywhere.com
```

For the root domain:

```text
victimespesticidesquebec.org
```

Recommended setup:

```text
victimespesticidesquebec.org -> redirects to https://www.victimespesticidesquebec.org/
```

This is usually configured at the domain registrar as URL forwarding/redirect.

If the registrar supports `ALIAS`, `ANAME`, or flattened CNAME records, the root domain can also point directly to PythonAnywhere, but redirecting root to `www` is the simplest setup.

## 5. Enable HTTPS certificate

After DNS has propagated:

1. Go to PythonAnywhere **Web**.
2. Find the HTTPS/certificate section.
3. Create or enable the Let's Encrypt certificate for:

```text
www.victimespesticidesquebec.org
```

4. Enable/force HTTPS if PythonAnywhere provides that option.

## 6. Update Wagtail Site settings

Open the Wagtail admin:

```text
https://www.victimespesticidesquebec.org/admin/
```

Go to:

```text
Settings -> Sites
```

Update the main site:

```text
Hostname: www.victimespesticidesquebec.org
Port: 443
Site name: Victimes des Pesticides du Québec
Default site: yes
```

If `vpq.pythonanywhere.com` remains available for staging/testing, it can stay in `ALLOWED_HOSTS`, but the main Wagtail site should use the real domain.

## 7. Final verification checklist

Verify these URLs:

```text
https://www.victimespesticidesquebec.org/
https://www.victimespesticidesquebec.org/a-propos/
https://www.victimespesticidesquebec.org/admin/
```

Check that:

- The homepage loads.
- The À propos page loads.
- Admin login works.
- CSS/static files load correctly.
- Uploaded images/media load correctly.
- Root domain redirects correctly:

```text
https://victimespesticidesquebec.org/ -> https://www.victimespesticidesquebec.org/
```

## 8. Troubleshooting

If something does not work, check PythonAnywhere:

- **Web -> Error log**
- **Web -> Server log**
- **Web -> Reload** after any `.env`, WSGI, migration, static file, or DNS-related change.

Common fixes:

```bash
cd ~/vpq-next
workon vpq-env
export DJANGO_SETTINGS_MODULE=victimes_pesticides.settings.pythonanywhere

python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
```

Then reload the app in the PythonAnywhere **Web** tab.
