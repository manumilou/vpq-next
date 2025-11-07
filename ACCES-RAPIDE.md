# 🚀 Accès rapide au site

## ✅ Le serveur est démarré !

### 🔑 Identifiants

**Username:** `admin`  
**Password:** `admin123`

### 🌐 URLs du site

- **Admin Wagtail:** http://127.0.0.1:8000/admin
- **Site public:** http://127.0.0.1:8000

## 📋 Pour démarrer le serveur manuellement

Si le serveur n'est pas déjà en cours d'exécution :

```bash
# 1. Aller dans le répertoire du projet
cd /Users/manu/src/github.com/victimes-pesticides-quebec

# 2. Activer l'environnement virtuel et démarrer
source venv/bin/activate
python3 manage.py runserver
```

## 🛑 Pour arrêter le serveur

```bash
# Trouver le processus
lsof -ti:8000

# Arrêter le processus
lsof -ti:8000 | xargs kill
```

## 🔄 Changer le mot de passe

Si vous voulez changer le mot de passe `admin123` :

```bash
source venv/bin/activate
python3 manage.py shell << 'ENDSCRIPT'
from django.contrib.auth.models import User
admin = User.objects.get(username='admin')
admin.set_password('votre_nouveau_mot_de_passe')
admin.save()
print("✅ Mot de passe changé!")
ENDSCRIPT
```

## 📖 Prochaines étapes

1. **Connectez-vous à l'admin** : http://127.0.0.1:8000/admin
2. **Lisez le guide de démarrage** : [PREMIERS-PAS.md](PREMIERS-PAS.md)
3. **Créez vos premiers contenus** : Catégories, Auteurs, Actualités

## 📚 Documentation complète

- [PREMIERS-PAS.md](PREMIERS-PAS.md) - Guide de démarrage (⭐ À LIRE)
- [COMMANDES.md](COMMANDES.md) - Toutes les commandes utiles
- [DEMARRAGE-RAPIDE.md](DEMARRAGE-RAPIDE.md) - Guide détaillé
- [README.md](README.md) - Documentation technique
- [SUMMARY.md](SUMMARY.md) - Vue d'ensemble du projet

## ⚠️ Note importante

Sur macOS, utilisez toujours `python3` au lieu de `python` !

---

**Bon travail avec votre nouveau CMS ! 🎉**
