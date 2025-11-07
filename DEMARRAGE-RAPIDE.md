# Démarrage rapide - Victimes des Pesticides du Québec

Guide de démarrage rapide pour commencer à utiliser le site.

## Première utilisation

### 1. Démarrer le serveur

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Démarrer le serveur
python manage.py runserver
```

Le site est maintenant accessible à :
- **Site public** : http://127.0.0.1:8000
- **Admin Wagtail** : http://127.0.0.1:8000/admin

### 2. Se connecter à l'administration

**Important** : Un compte administrateur a déjà été créé avec le nom d'utilisateur `admin`. Vous devez définir un mot de passe :

```bash
python manage.py changepassword admin
```

Ou créez un nouveau superutilisateur :

```bash
python manage.py createsuperuser
```

Connectez-vous ensuite à http://127.0.0.1:8000/admin

### 3. Créer vos premiers contenus

#### A. Créer des catégories et auteurs

1. Dans le menu de gauche, cliquez sur **"Snippets"**
2. Créez quelques **Catégories** (ex: "Nouvelles", "Événements", "Études")
3. Créez des **Auteurs** avec leurs informations

#### B. Créer la page d'actualités

1. Allez dans **"Pages"** dans le menu
2. Vous verrez la page "Home" existante
3. Cliquez sur "**+ Ajouter une page enfant**"
4. Choisissez **"Page d'index des actualités"**
5. Remplissez :
   - Titre : "Actualités"
   - Introduction (optionnel)
6. Cliquez **"Publier"**

#### C. Créer votre première actualité

1. Sur la page "Actualités" que vous venez de créer
2. Cliquez sur "**+ Ajouter une page enfant**"
3. Choisissez **"Actualité"**
4. Remplissez le formulaire :
   - **Titre** : Le titre de votre actualité
   - **Date de publication** : Date de publication
   - **Auteur** : Choisissez un auteur
   - **Catégories** : Sélectionnez une ou plusieurs catégories
   - **Image principale** : Téléversez une image
   - **Introduction** : Court résumé (apparaît dans les listes)
   - **Corps** : Utilisez le StreamField pour construire votre contenu
5. Cochez **"Mise en vedette"** si vous voulez l'afficher sur la page d'accueil
6. Cliquez **"Publier"**

#### D. Personnaliser la page d'accueil

1. Retournez dans **"Pages"**
2. Cliquez sur **"Home"**
3. Cliquez sur **"Modifier"**
4. Ajoutez :
   - **Introduction** : Texte de bienvenue
   - **Corps** : Utilisez les blocs pour construire votre page
     - Paragraphe pour du texte
     - Titre pour des sections
     - Appel à l'action pour des boutons importants
5. **Sauvegarder** ou **Publier**

Les actualités "en vedette" apparaîtront automatiquement en bas de la page d'accueil.

#### E. Créer une page de contact

1. Dans **"Pages"**, ajoutez une page enfant à "Home"
2. Choisissez **"Page de contact"**
3. Remplissez :
   - **Titre** : "Contact" ou "Nous joindre"
   - **Introduction** : Message d'accueil
   - **Champs du formulaire** : Ajoutez les champs nécessaires
     - Nom (Single line text)
     - Courriel (Email)
     - Message (Multi-line text)
   - **Message de remerciement** : "Merci, nous vous répondrons bientôt"
   - **Adresse courriel** : Votre email pour recevoir les messages
4. Publiez la page

## Utiliser le StreamField

Le StreamField est un outil puissant pour créer du contenu flexible.

### Blocs disponibles

1. **Paragraphe** : Texte avec formatage (gras, italique, listes, liens)
2. **Titre** : Pour structurer votre contenu en sections
3. **Image** : Téléversez ou choisissez une image
4. **Citation** : Pour mettre en évidence une citation
5. **Appel à l'action** : Créer un encadré avec un bouton
6. **Code** : Pour afficher du code (si nécessaire)
7. **HTML brut** : Pour du contenu personnalisé avancé

### Ajouter un bloc

1. Cliquez sur **"+ Ajouter [type de bloc]"**
2. Remplissez le contenu
3. Utilisez les flèches ⬆️⬇️ pour réorganiser les blocs
4. Utilisez l'icône 🗑️ pour supprimer un bloc

### Exemple de structure d'actualité

```
1. [Titre] Introduction au sujet
2. [Paragraphe] Explication du contexte...
3. [Image] Photo illustrative
4. [Titre] Les faits principaux
5. [Paragraphe] Détails importants...
6. [Citation] "Citation d'un expert"
7. [Paragraphe] Suite de l'article...
8. [Appel à l'action] En savoir plus → Lien vers ressources
```

## Gestion des images

### Téléverser des images

1. Allez dans **"Images"** dans le menu
2. Cliquez **"Ajouter une image"**
3. Choisissez votre fichier
4. Ajoutez un titre descriptif
5. Ajoutez des tags pour organiser (optionnel)

### Bonnes pratiques images

- **Format** : JPG pour photos, PNG pour graphiques
- **Taille** : Maximum 2MB par image
- **Dimensions recommandées** :
  - Image principale d'actualité : 1200×630 px
  - Images dans le contenu : 800-1000 px de large
- **Nommage** : Utilisez des noms descriptifs

## Workflow de publication

### Brouillon → Révision → Publication

1. **Brouillon** : Créez votre contenu et cliquez "Sauvegarder le brouillon"
2. **Prévisualisation** : Utilisez "Prévisualiser" pour voir le rendu
3. **Publication** : Quand c'est prêt, cliquez "Publier"

### Modifier un contenu publié

1. Trouvez la page dans **"Pages"**
2. Cliquez sur le titre ou l'icône ✏️
3. Faites vos modifications
4. Cliquez **"Publier"** pour mettre en ligne immédiatement

### Dépublier une page

1. Dans l'éditeur de page, cliquez sur le menu **"..."** en haut à droite
2. Choisissez **"Dépublier"**

## Organiser votre contenu

### Structure recommandée

```
Home (Page d'accueil)
├── Actualités (Page d'index)
│   ├── Actualité 1
│   ├── Actualité 2
│   └── ...
├── À propos (Page standard)
├── Ressources (Page standard)
│   ├── Documentation (Page standard)
│   └── Liens utiles (Page standard)
└── Contact (Page de contact)
```

### Navigation

La navigation du site se construit automatiquement à partir de l'arborescence des pages.

## Astuces et conseils

### Pour les actualités

- ✅ Utilisez des images attractives
- ✅ Écrivez une introduction accrocheuse (apparaît dans les aperçus)
- ✅ Structurez avec des titres de section
- ✅ Utilisez "Mise en vedette" pour les actualités importantes
- ✅ Attribuez des catégories pour organiser

### Pour les pages d'information

- ✅ Utilisez le bloc "Appel à l'action" pour les actions importantes
- ✅ Divisez le contenu long avec des titres de section
- ✅ Ajoutez des images pour illustrer
- ✅ Utilisez les citations pour mettre en valeur des points clés

### Optimisation SEO

1. **Titre** : Clair et descriptif (50-60 caractères)
2. **Onglet "Promouvoir"** dans l'éditeur :
   - Ajoutez une "Description de recherche" (150-160 caractères)
   - Personnalisez le "Titre SEO" si nécessaire
3. **URLs** : Wagtail génère automatiquement des URLs propres

## Problèmes courants

### "Cette page n'existe pas"
→ Vérifiez que la page est publiée (icône verte dans la liste des pages)

### "L'image ne s'affiche pas"
→ Vérifiez que le fichier n'est pas trop lourd (max 2MB)

### "Je ne peux pas ajouter ce type de page ici"
→ Certaines pages ont des restrictions (ex: ActualitePage ne peut être que sous ActualiteIndexPage)

### "Le formulaire de contact ne fonctionne pas"
→ Vérifiez que vous avez bien configuré l'adresse email de destination

## Prochaines étapes

Maintenant que vous maîtrisez les bases :

1. 📝 Créez plusieurs actualités
2. 📄 Créez vos pages d'information
3. 🎨 Personnalisez la page d'accueil
4. 📧 Configurez la page de contact
5. 🖼️ Organisez vos images et médias

**Besoin d'aide ?** Consultez le README.md ou la [documentation Wagtail](https://docs.wagtail.org/).
