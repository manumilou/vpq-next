# 🚀 Premiers pas - Guide ultra-rapide

## 1. Démarrer le site (3 minutes)

### Option A : Mot de passe simple pour tester

```bash
# Activer l'environnement
source venv/bin/activate

# Définir le mot de passe de l'admin (username: admin)
python manage.py changepassword admin
# Entrez un mot de passe simple pour tester (ex: admin123)

# Démarrer le serveur
python manage.py runserver
```

### Option B : Créer votre propre compte

```bash
# Activer l'environnement
source venv/bin/activate

# Créer votre compte
python manage.py createsuperuser
# Suivez les instructions

# Démarrer le serveur
python manage.py runserver
```

## 2. Accéder au site

Ouvrez votre navigateur :

- **Admin** : http://127.0.0.1:8000/admin
- **Site public** : http://127.0.0.1:8000

Connectez-vous avec :
- Username : `admin` (ou celui que vous avez créé)
- Password : celui que vous venez de définir

## 3. Créer votre premier contenu (10 minutes)

### Étape 1 : Créer des catégories

1. Dans le menu de gauche, cliquez sur **"Snippets"**
2. Cliquez sur **"Catégories"** → **"Ajouter une catégorie"**
3. Créez 2-3 catégories :
   - Nom : "Nouvelles", Slug : "nouvelles"
   - Nom : "Événements", Slug : "evenements"
   - Nom : "Études", Slug : "etudes"
4. Sauvegardez

### Étape 2 : Créer un auteur

1. Dans **"Snippets"**, cliquez sur **"Auteurs"**
2. **"Ajouter un auteur"**
3. Remplissez :
   - Prénom : Votre prénom
   - Nom : Votre nom
   - Biographie : Quelques mots sur vous
4. Sauvegardez

### Étape 3 : Créer la page d'actualités

1. Dans le menu, cliquez sur **"Pages"**
2. Vous verrez la page "Home"
3. Cliquez sur les **trois points** à droite de "Home"
4. Choisissez **"Ajouter une page enfant"**
5. Sélectionnez **"Page d'index des actualités"**
6. Remplissez :
   - Titre : "Actualités"
   - Introduction : "Découvrez nos dernières nouvelles"
7. Cliquez **"Publier"**

### Étape 4 : Créer votre première actualité

1. Sur la page "Actualités" que vous venez de créer
2. Cliquez sur les **trois points** → **"Ajouter une page enfant"**
3. Choisissez **"Actualité"**
4. Remplissez :
   - **Titre** : "Première actualité de test"
   - **Date de publication** : Aujourd'hui
   - **Auteur** : Choisissez l'auteur créé
   - **Catégories** : Sélectionnez "Nouvelles"
   - **Introduction** : "Ceci est une actualité de test pour découvrir le système"
   - **Corps** : Cliquez sur **"+ Paragraphe"** et écrivez quelques lignes
5. Cochez **"Mise en vedette"** (pour l'afficher sur l'accueil)
6. Cliquez **"Publier"**

### Étape 5 : Voir le résultat

1. Allez sur http://127.0.0.1:8000
2. Vous devriez voir votre actualité sur la page d'accueil !
3. Cliquez dessus pour voir la page complète

## 4. Personnaliser la page d'accueil (5 minutes)

1. Dans **"Pages"**, cliquez sur **"Home"**
2. Cliquez sur **"Modifier"** (en haut)
3. Dans **"Introduction"**, écrivez :
   ```
   Bienvenue sur le site de Victimes des Pesticides du Québec.
   Nous informons et aidons les personnes dont la santé a pu être
   affectée par l'usage de pesticides.
   ```
4. Dans **"Corps"**, ajoutez :
   - Un bloc **"Titre"** : "Notre mission"
   - Un bloc **"Paragraphe"** : Décrivez votre mission
   - Un bloc **"Appel à l'action"** :
     - Titre : "Besoin d'aide ?"
     - Texte : "Contactez-nous pour obtenir du soutien"
     - Lien : /contact (on créera cette page plus tard)
     - Texte du bouton : "Nous contacter"
5. Cliquez **"Publier"**
6. Allez voir le résultat sur http://127.0.0.1:8000

## 5. Astuces pour continuer

### Explorer l'interface
- Survolez les icônes pour voir les tooltips
- Le bouton **"Preview"** vous montre le résultat sans publier
- **"Save draft"** sauvegarde sans publier
- Les **trois points (...)** donnent plus d'options

### Raccourcis clavier utiles
- `Ctrl+S` (ou `Cmd+S`) : Sauvegarder
- `Ctrl+P` (ou `Cmd+P`) : Prévisualiser

### Gestion des images
1. Allez dans **"Images"** dans le menu
2. Cliquez **"Ajouter une image"**
3. Téléversez une photo
4. Vous pourrez ensuite l'utiliser dans vos actualités

### StreamField - Construire du contenu
Le "Corps" des pages utilise des **blocs** :
- **Paragraphe** : Pour le texte normal
- **Titre** : Pour structurer en sections
- **Image** : Pour ajouter des photos
- **Citation** : Pour mettre en valeur une phrase
- **Appel à l'action** : Pour des boutons/liens importants

Cliquez sur **"+ Ajouter [type]"** pour ajouter un bloc.
Utilisez les flèches ⬆️⬇️ pour réorganiser.

## 6. Créer d'autres pages

### Page "À propos"
1. Créez une page enfant de "Home"
2. Choisissez **"Page standard"**
3. Titre : "À propos"
4. Utilisez le StreamField pour construire votre contenu

### Page de contact
1. Créez une page enfant de "Home"
2. Choisissez **"Page de contact"**
3. Titre : "Contact"
4. Ajoutez les champs du formulaire :
   - Nom (Single line text) - Required
   - Courriel (Email) - Required
   - Message (Multi-line text) - Required
5. Configurez l'email de réception
6. Publiez

## 7. Prochaines étapes

Maintenant que vous maîtrisez les bases :

- [ ] Créez 5-10 actualités
- [ ] Créez vos pages d'information
- [ ] Téléversez des images
- [ ] Testez le formulaire de contact
- [ ] Explorez les options dans "Settings"

## 📚 Besoin d'aide ?

Consultez :
- [DEMARRAGE-RAPIDE.md](DEMARRAGE-RAPIDE.md) - Guide complet
- [README.md](README.md) - Documentation technique
- [SUMMARY.md](SUMMARY.md) - Vue d'ensemble du projet

## 🎉 C'est parti !

Vous êtes prêt à créer du contenu. Le système est simple et intuitif.

**N'ayez pas peur d'expérimenter** - vous pouvez toujours :
- Prévisualiser avant de publier
- Sauvegarder en brouillon
- Revenir en arrière
- Dépublier si nécessaire

Bon travail ! 🚀
