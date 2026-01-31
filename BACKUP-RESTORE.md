# Guide de sauvegarde et restauration

Ce guide explique comment sauvegarder la base de données et les fichiers médias depuis PythonAnywhere et les restaurer localement.

## Sauvegarde depuis PythonAnywhere (Production)

### Étape 1: Se connecter à PythonAnywhere

1. Allez sur [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Connectez-vous à votre compte
3. Ouvrez une console Bash

### Étape 2: Sauvegarder la base de données MySQL

```bash
# Naviguer vers votre projet
cd ~/vpq-next

# Activer l'environnement virtuel
workon vpq-env

# Exporter les variables d'environnement
export DJANGO_SETTINGS_MODULE=victimes_pesticides.settings.pythonanywhere

# Créer un répertoire pour les backups
mkdir -p ~/backups

# Créer une sauvegarde au format JSON (recommandé pour Django)
python manage.py dumpdata \
  --natural-foreign \
  --natural-primary \
  --exclude contenttypes \
  --exclude auth.permission \
  --exclude sessions.session \
  --indent 2 \
  > ~/backups/backup-$(date +%Y%m%d-%H%M%S).json

# OU: Sauvegarde MySQL directe (alternative)
mysqldump -u yourusername -h yourusername.mysql.pythonanywhere-services.com -p yourusername\$vpq > ~/backups/mysql-backup-$(date +%Y%m%d-%H%M%S).sql
```

**Note**: Remplacez `yourusername` par votre nom d'utilisateur PythonAnywhere.

### Étape 3: Sauvegarder les fichiers médias (images)

```bash
# Créer une archive tar.gz des fichiers médias
cd ~/vpq-next
tar -czf ~/backups/media-$(date +%Y%m%d-%H%M%S).tar.gz media/

# Vérifier la taille de l'archive
ls -lh ~/backups/media-*.tar.gz
```

### Étape 4: Télécharger les fichiers de sauvegarde

**Option A: Via l'interface web PythonAnywhere**
1. Allez dans l'onglet **Files**
2. Naviguez vers `/home/yourusername/backups/`
3. Cliquez sur chaque fichier pour le télécharger

**Option B: Via scp (depuis votre machine locale)**

```bash
# Télécharger le backup JSON
scp yourusername@ssh.pythonanywhere.com:~/backups/backup-*.json ~/Downloads/

# Télécharger les médias
scp yourusername@ssh.pythonanywhere.com:~/backups/media-*.tar.gz ~/Downloads/
```

**Option C: Via rsync (plus efficace pour les gros fichiers)**

```bash
# Télécharger tous les backups
rsync -avz yourusername@ssh.pythonanywhere.com:~/backups/ ~/backups-vpq/
```

## Restauration en local

### Étape 1: Placer les fichiers de sauvegarde

```bash
# Sur votre machine locale
cd ~/src/github.com/victimes-pesticides-quebec

# Créer un répertoire pour les backups
mkdir -p backups

# Déplacer les fichiers téléchargés
mv ~/Downloads/backup-*.json backups/
mv ~/Downloads/media-*.tar.gz backups/
```

### Étape 2: Restaurer les fichiers médias

```bash
# Extraire l'archive des médias
cd ~/src/github.com/victimes-pesticides-quebec

# Sauvegarder les médias locaux existants (optionnel)
if [ -d "media" ]; then
  mv media media.old-$(date +%Y%m%d-%H%M%S)
fi

# Extraire les médias de production
tar -xzf backups/media-*.tar.gz

# Vérifier que les fichiers sont là
ls -la media/images/
ls -la media/original_images/
```

### Étape 3: Restaurer la base de données

#### Option A: Réinitialiser complètement la base de données (recommandé)

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Sauvegarder la base de données locale existante (optionnel)
cp db.sqlite3 db.sqlite3.backup-$(date +%Y%m%d-%H%M%S)

# Supprimer la base de données locale
rm db.sqlite3

# Recréer la base de données avec les migrations
python manage.py migrate

# Charger les données de production
python manage.py loaddata backups/backup-20250125-*.json
```

#### Option B: Restaurer sans tout supprimer (plus risqué)

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Charger les données (peut causer des conflits)
python manage.py loaddata backups/backup-20250125-*.json
```

### Étape 4: Vérifier la restauration

```bash
# Démarrer le serveur de développement
python manage.py runserver

# Dans un autre terminal, vérifier les données
python manage.py shell
```

Dans le shell Python:
```python
from actualites.models import ActualitePage
from wagtail.images.models import Image

# Vérifier le nombre d'actualités
print(f"Actualités: {ActualitePage.objects.count()}")

# Vérifier le nombre d'images
print(f"Images: {Image.objects.count()}")

# Vérifier quelques actualités
for page in ActualitePage.objects.live()[:5]:
    print(f"- {page.title} ({page.date_publication})")
```

Visitez http://127.0.0.1:8000 et vérifiez que:
- ✅ Les actualités sont visibles
- ✅ Les images s'affichent correctement
- ✅ Le contenu est complet

## Script automatisé de sauvegarde

Pour faciliter les sauvegardes régulières, créez ce script sur PythonAnywhere:

```bash
# Sur PythonAnywhere, créer le fichier
nano ~/backup.sh
```

Contenu du script:

```bash
#!/bin/bash

# Configuration
PROJECT_DIR="$HOME/vpq-next"
BACKUP_DIR="$HOME/backups"
DATE=$(date +%Y%m%d-%H%M%S)
KEEP_BACKUPS=7  # Nombre de backups à conserver

echo "🔄 Sauvegarde VPQ - $DATE"

# Créer le répertoire de backup
mkdir -p "$BACKUP_DIR"

# Activer l'environnement virtuel
cd "$PROJECT_DIR"
source "$HOME/.virtualenvs/vpq-env/bin/activate"
export DJANGO_SETTINGS_MODULE=victimes_pesticides.settings.pythonanywhere

# Sauvegarde de la base de données
echo "📦 Sauvegarde de la base de données..."
python manage.py dumpdata \
  --natural-foreign \
  --natural-primary \
  --exclude contenttypes \
  --exclude auth.permission \
  --exclude sessions.session \
  --indent 2 \
  > "$BACKUP_DIR/backup-$DATE.json"

if [ $? -eq 0 ]; then
  echo "✅ Base de données sauvegardée: backup-$DATE.json"
else
  echo "❌ Erreur lors de la sauvegarde de la base de données"
  exit 1
fi

# Sauvegarde des médias
echo "📸 Sauvegarde des médias..."
tar -czf "$BACKUP_DIR/media-$DATE.tar.gz" -C "$PROJECT_DIR" media/

if [ $? -eq 0 ]; then
  echo "✅ Médias sauvegardés: media-$DATE.tar.gz"
else
  echo "❌ Erreur lors de la sauvegarde des médias"
  exit 1
fi

# Afficher les tailles
echo ""
echo "📊 Taille des sauvegardes:"
ls -lh "$BACKUP_DIR/backup-$DATE.json"
ls -lh "$BACKUP_DIR/media-$DATE.tar.gz"

# Nettoyer les anciennes sauvegardes (garder les $KEEP_BACKUPS plus récentes)
echo ""
echo "🧹 Nettoyage des anciennes sauvegardes..."
cd "$BACKUP_DIR"
ls -t backup-*.json | tail -n +$((KEEP_BACKUPS + 1)) | xargs -r rm
ls -t media-*.tar.gz | tail -n +$((KEEP_BACKUPS + 1)) | xargs -r rm

echo ""
echo "✅ Sauvegarde terminée!"
echo ""
echo "📋 Sauvegardes disponibles:"
ls -lh "$BACKUP_DIR"
```

Rendre le script exécutable:

```bash
chmod +x ~/backup.sh
```

Utilisation:

```bash
# Exécuter une sauvegarde
~/backup.sh
```

## Script automatisé de restauration locale

Créez ce script sur votre machine locale:

```bash
# Sur votre machine locale
cd ~/src/github.com/victimes-pesticides-quebec
nano restore-from-prod.sh
```

Contenu du script:

```bash
#!/bin/bash

# Configuration
PROJECT_DIR="$HOME/src/github.com/victimes-pesticides-quebec"
BACKUP_DIR="$PROJECT_DIR/backups"

echo "🔄 Restauration depuis la production"

# Vérifier qu'on est dans le bon répertoire
cd "$PROJECT_DIR" || exit 1

# Vérifier qu'un backup existe
if [ ! -f "$BACKUP_DIR/backup-"*.json ]; then
  echo "❌ Aucun fichier de backup trouvé dans $BACKUP_DIR"
  echo "   Téléchargez d'abord les backups depuis PythonAnywhere"
  exit 1
fi

# Trouver le backup le plus récent
LATEST_BACKUP=$(ls -t "$BACKUP_DIR/backup-"*.json | head -1)
LATEST_MEDIA=$(ls -t "$BACKUP_DIR/media-"*.tar.gz | head -1)

echo "📦 Backup DB: $LATEST_BACKUP"
echo "📸 Backup médias: $LATEST_MEDIA"
echo ""

# Demander confirmation
read -p "⚠️  Ceci va remplacer votre base de données locale. Continuer? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "❌ Restauration annulée"
  exit 1
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Sauvegarder la DB locale existante
if [ -f "db.sqlite3" ]; then
  echo "💾 Sauvegarde de la DB locale existante..."
  cp db.sqlite3 "db.sqlite3.backup-$(date +%Y%m%d-%H%M%S)"
fi

# Sauvegarder les médias locaux existants
if [ -d "media" ]; then
  echo "💾 Sauvegarde des médias locaux existants..."
  mv media "media.backup-$(date +%Y%m%d-%H%M%S)"
fi

# Supprimer et recréer la base de données
echo "🗑️  Suppression de la base de données locale..."
rm -f db.sqlite3

echo "🔨 Création d'une nouvelle base de données..."
python manage.py migrate --noinput

# Restaurer les données
echo "📥 Restauration des données..."
python manage.py loaddata "$LATEST_BACKUP"

if [ $? -ne 0 ]; then
  echo "❌ Erreur lors de la restauration de la base de données"
  exit 1
fi

# Restaurer les médias
echo "📸 Restauration des médias..."
tar -xzf "$LATEST_MEDIA"

if [ $? -ne 0 ]; then
  echo "❌ Erreur lors de la restauration des médias"
  exit 1
fi

# Vérifications
echo ""
echo "✅ Restauration terminée!"
echo ""
echo "🔍 Vérification..."

# Compter les données
python manage.py shell -c "
from actualites.models import ActualitePage
from wagtail.images.models import Image
print(f'Actualités: {ActualitePage.objects.count()}')
print(f'Images: {Image.objects.count()}')
"

echo ""
echo "🚀 Vous pouvez maintenant démarrer le serveur:"
echo "   python manage.py runserver"
```

Rendre le script exécutable:

```bash
chmod +x restore-from-prod.sh
```

Utilisation:

```bash
# Télécharger les backups depuis PythonAnywhere d'abord
# Puis exécuter:
./restore-from-prod.sh
```

## Fréquence de sauvegarde recommandée

- **Avant chaque déploiement majeur**: Toujours sauvegarder
- **Quotidien**: Si beaucoup de nouveau contenu est ajouté
- **Hebdomadaire**: Pour une utilisation normale
- **Mensuel**: Minimum pour archivage

## Troubleshooting

### Erreur lors du loaddata

```
IntegrityError: duplicate key value violates unique constraint
```

**Solution**: La base de données locale n'était pas vide. Supprimez-la complètement avant de restaurer:

```bash
rm db.sqlite3
python manage.py migrate
python manage.py loaddata backups/backup-*.json
```

### Images manquantes après restauration

**Vérifications**:

```bash
# Vérifier que les fichiers existent
ls -la media/images/
ls -la media/original_images/

# Vérifier les permissions
chmod -R 755 media/
```

### Backup trop volumineux pour télécharger

**Solution**: Compresser davantage ou utiliser rsync:

```bash
# Compression maximale
tar -czf ~/backups/media-compressed.tar.gz --gzip media/

# OU: Utiliser rsync avec compression
rsync -avz --compress-level=9 \
  yourusername@ssh.pythonanywhere.com:~/vpq-next/media/ \
  ./media/
```

### Erreur de connexion MySQL lors du backup

**Solution**: Vérifiez vos identifiants MySQL dans le fichier `.env` sur PythonAnywhere:

```bash
cat ~/.env | grep DATABASE
```

## Sauvegardes automatiques (Cron)

Pour programmer des sauvegardes automatiques sur PythonAnywhere:

1. Allez dans l'onglet **Tasks** sur PythonAnywhere
2. Ajoutez une nouvelle tâche programmée:
   - **Heure**: `03:00` (3h du matin)
   - **Commande**: `/home/yourusername/backup.sh`
3. Cliquez sur "Create"

Les sauvegardes seront créées automatiquement chaque jour à 3h du matin.

## Conclusion

Vous avez maintenant:
- ✅ Un guide complet pour sauvegarder production
- ✅ Un guide pour restaurer localement
- ✅ Des scripts automatisés pour faciliter le processus
- ✅ Des procédures de vérification

**Important**: Testez régulièrement vos sauvegardes pour vous assurer qu'elles fonctionnent correctement!
