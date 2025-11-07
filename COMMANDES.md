# Commandes essentielles - Victimes des Pesticides du Québec

## ⚠️ Important : Utiliser python3

Sur macOS, utilisez toujours `python3` au lieu de `python`.

## 🚀 Démarrage rapide

```bash
# 1. Activer l'environnement virtuel
source venv/bin/activate

# 2. Définir le mot de passe admin (première fois seulement)
python3 manage.py changepassword admin

# 3. Démarrer le serveur
python3 manage.py runserver
```

Puis ouvrez : http://127.0.0.1:8000/admin

## 📝 Commandes courantes

### Gestion du serveur

```bash
# Démarrer le serveur de développement
python3 manage.py runserver

# Démarrer sur un autre port
python3 manage.py runserver 8001

# Démarrer et rendre accessible sur le réseau local
python3 manage.py runserver 0.0.0.0:8000
```

### Gestion des utilisateurs

```bash
# Changer le mot de passe d'un utilisateur
python3 manage.py changepassword admin

# Créer un nouveau superutilisateur
python3 manage.py createsuperuser

# Lister tous les superutilisateurs
python3 manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).values_list('username', flat=True))"
```

### Gestion de la base de données

```bash
# Créer des migrations après modification des modèles
python3 manage.py makemigrations

# Appliquer les migrations
python3 manage.py migrate

# Voir l'état des migrations
python3 manage.py showmigrations

# Revenir en arrière d'une migration
python3 manage.py migrate nom_app numero_migration
```

### Gestion du contenu

```bash
# Créer une sauvegarde complète
python3 manage.py dumpdata > backup_$(date +%Y%m%d).json

# Créer une sauvegarde sans les sessions/logs
python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude sessions > backup.json

# Restaurer une sauvegarde
python3 manage.py loaddata backup.json

# Supprimer toutes les données (ATTENTION!)
python3 manage.py flush
```

### Gestion des fichiers statiques

```bash
# Collecter tous les fichiers statiques (pour production)
python3 manage.py collectstatic

# Collecter sans confirmation
python3 manage.py collectstatic --noinput

# Nettoyer les fichiers statiques orphelins
python3 manage.py collectstatic --clear
```

### Utilitaires

```bash
# Ouvrir un shell Python avec Django chargé
python3 manage.py shell

# Ouvrir un shell de base de données
python3 manage.py dbshell

# Vérifier les problèmes potentiels
python3 manage.py check

# Voir toutes les commandes disponibles
python3 manage.py help
```

## 🔧 Dépannage

### Problème : "python: command not found"

**Solution :** Utilisez `python3` au lieu de `python`

```bash
python3 manage.py runserver
```

### Problème : "No module named 'django'"

**Solution :** Activez l'environnement virtuel

```bash
source venv/bin/activate
python3 manage.py runserver
```

### Problème : "Port already in use"

**Solution :** Trouvez et arrêtez le processus ou utilisez un autre port

```bash
# Trouver le processus sur le port 8000
lsof -ti:8000

# Arrêter le processus
lsof -ti:8000 | xargs kill

# Ou utiliser un autre port
python3 manage.py runserver 8001
```

### Problème : "OperationalError: no such table"

**Solution :** Appliquez les migrations

```bash
python3 manage.py migrate
```

### Problème : Mot de passe oublié

**Solution :** Réinitialisez le mot de passe

```bash
python3 manage.py changepassword admin
```

## 🐍 Vérifier votre environnement

```bash
# Vérifier la version de Python
python3 --version

# Vérifier si le venv est activé
which python3

# Devrait afficher: /Users/manu/.../venv/bin/python3

# Vérifier les versions Django et Wagtail
python3 -c "import django, wagtail; print(f'Django {django.get_version()}'); print(f'Wagtail {wagtail.__version__}')"
```

## 📦 Gestion des dépendances

```bash
# Installer une nouvelle dépendance
pip install nom-du-package

# Mettre à jour requirements.txt
pip freeze > requirements.txt

# Installer toutes les dépendances
pip install -r requirements.txt

# Mettre à jour pip
pip install --upgrade pip
```

## 🔄 Workflow typique

### Démarrage quotidien

```bash
cd victimes-pesticides-quebec
source venv/bin/activate
python3 manage.py runserver
```

### Après modification des modèles

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

### Avant de committer

```bash
# Vérifier les problèmes
python3 manage.py check

# Créer une sauvegarde
python3 manage.py dumpdata > backup.json

# Mettre à jour requirements.txt si nécessaire
pip freeze > requirements.txt
```

## 🚀 Raccourcis utiles

Créez des alias dans votre `~/.zshrc` ou `~/.bashrc` :

```bash
# Ajouter ces lignes à ~/.zshrc
alias vpq='cd ~/src/github.com/victimes-pesticides-quebec && source venv/bin/activate'
alias vpq-server='vpq && python3 manage.py runserver'
alias vpq-shell='vpq && python3 manage.py shell'

# Recharger le shell
source ~/.zshrc
```

Ensuite vous pouvez simplement taper :
- `vpq-server` pour démarrer le serveur
- `vpq-shell` pour ouvrir le shell Django

## 📚 Aide

Pour plus d'informations sur une commande :

```bash
python3 manage.py help
python3 manage.py help commande_specifique
```

Exemple :
```bash
python3 manage.py help migrate
```
