# Structure des Pages - Victimes des Pesticides du Québec

Ce document définit la structure recommandée des pages pour le site web VPQ.

## Hiérarchie des Pages

```
Root (Wagtail system page)
└── Home (HomePage)
    ├── À propos (StandardPage)
    ├── Quels risques? (StandardPage)
    ├── Malades, que faire? (StandardPage)
    ├── Alternatives (StandardPage)
    ├── Soutenez VPQ (StandardPage)
    ├── Contact (ContactPage)
    └── Actualités (ActualiteIndexPage)
        ├── Article 1 (ActualitePage)
        ├── Article 2 (ActualitePage)
        └── Article 3 (ActualitePage)
```

## Types de Pages Disponibles

### 1. HomePage (Page d'accueil)
- **Localisation:** `home/models.py`
- **URL:** `/`
- **Utilisation:** Page d'accueil principale avec des blocs riches
- **Blocs disponibles:**
  - Bloc héro pleine largeur (avec image de fond, titre, sous-titre, bouton)
  - Actions rapides (grille de 3 actions avec icônes SVG)
  - Statistiques (grille de 4 statistiques)
  - Bloc problématique (image + texte sur deux colonnes)
  - Cartes de mission (grille de 3 cartes avec icônes)
  - Appel à l'action final (avec dégradé de couleurs)
  - Paragraphe (texte enrichi)
  - Titre de section
  - Image
  - Citation
- **Note:** Il ne peut y avoir qu'une seule HomePage - c'est la racine du site

### 2. StandardPage (Page standard)
- **Localisation:** `pages_app/models.py`
- **URL:** `/slug-de-la-page/`
- **Utilisation:** Pages d'information générales
- **Blocs disponibles:**
  - Paragraphe (texte enrichi avec gras, italique, listes, titres h2-h4)
  - Titre de section
  - Image
  - Image avec légende
  - Citation
  - Tableau (avec lignes et colonnes)
  - Témoignage (simple, avec photo optionnelle)
  - **Carrousel de témoignages** (nouveau - plusieurs témoignages avec défilement automatique)
  - Deux colonnes (layout en 2 colonnes)
  - Carte de personne (équipe/membres)
  - Grille de cartes (avec icônes SVG)
  - Statistiques (affichage de chiffres clés)
  - Alerte/Notice (info, succès, attention, danger)
  - Accordéon/FAQ (sections pliables)
  - Appel à l'action (avec titre, texte, lien, bouton)
  - Formulaire de don Zeffy (intégration iframe)
  - Inscription infolettre Mailchimp
  - HTML brut (utiliser avec précaution)
- **Champs additionnels:**
  - Introduction (texte simple)
- **Documentation détaillée:**
  - Voir [CARROUSEL-TEMOIGNAGES.md](CARROUSEL-TEMOIGNAGES.md) pour le bloc carrousel

### 3. ContactPage (Page de contact)
- **Localisation:** `pages_app/models.py`
- **URL:** `/contact/` (ou autre slug)
- **Utilisation:** Page avec formulaire de contact
- **Fonctionnalités:**
  - Formulaire configurable avec champs personnalisés
  - Envoi d'email automatique
  - Message de remerciement personnalisable
  - Panneau de suivi des soumissions dans l'admin
- **Champs configurables:**
  - Introduction (texte enrichi)
  - Champs du formulaire (ajout/suppression via InlinePanel)
  - Adresse email de destination
  - Adresse email d'expédition
  - Sujet de l'email

### 4. ActualiteIndexPage (Page d'index des actualités)
- **Localisation:** `actualites/models.py`
- **URL:** `/actualites/` (ou autre slug)
- **Utilisation:** Page qui liste toutes les actualités/articles de blog
- **Fonctionnalités:**
  - Affichage automatique de toutes les ActualitePage enfants
  - Tri par date de publication (plus récent en premier)
  - Introduction personnalisable
- **Restrictions:** Accepte uniquement des ActualitePage comme pages enfants

### 5. ActualitePage (Page d'actualité/article)
- **Localisation:** `actualites/models.py`
- **URL:** `/actualites/slug-de-larticle/`
- **Utilisation:** Articles de blog, communiqués de presse, actualités
- **Champs:**
  - Date de publication
  - Auteur
  - Catégories (tags)
  - Image à la une
  - Introduction (résumé)
  - Corps (StreamField avec blocs flexibles)
- **Blocs disponibles:**
  - Paragraphe
  - Titre de section
  - Image
  - Citation
  - Appel à l'action
  - HTML brut
- **Note:** Doit être créée comme enfant d'une ActualiteIndexPage

## Menu Principal

Le menu de navigation (défini dans `victimes_pesticides/templates/includes/header.html`) correspond à cette structure:

1. **À propos** → StandardPage (`/a-propos/`)
2. **Quels risques?** → StandardPage (`/quels-risques/`)
3. **Malades, que faire ?** → StandardPage (`/malades-que-faire/`)
4. **Alternatives** → StandardPage (`/alternatives/`)
5. **Soutenez VPQ** → StandardPage (`/soutenez-vpq/`)

**Note:** Les liens dans le menu doivent être mis à jour pour pointer vers les vraies pages une fois créées.

## Création d'une Nouvelle Page

### Via l'Admin Wagtail

1. Connectez-vous à `/admin/`
2. Cliquez sur **"Pages"** dans la barre latérale
3. Naviguez vers la page parent (généralement **"Home"**)
4. Cliquez sur le menu **"⋮"** (trois points) à côté de la page parent
5. Sélectionnez **"Add child page"**
6. Choisissez le type de page approprié
7. Remplissez les champs requis
8. **Important:** Définissez le **slug** de l'URL (généré automatiquement depuis le titre, mais modifiable)
9. Cliquez sur **"Publish"** pour publier immédiatement, ou **"Save draft"** pour sauvegarder en brouillon

### Ordre Recommandé de Création

1. **HomePage** (déjà créée lors de l'installation initiale)
2. **ActualiteIndexPage** (`/actualites/`)
   - Slug: `actualites`
   - Titre: "Actualités"
3. **StandardPages** pour chaque section du menu:
   - `/a-propos/`
   - `/quels-risques/`
   - `/malades-que-faire/`
   - `/alternatives/`
   - `/soutenez-vpq/`
4. **ContactPage** (`/contact/`)
5. **ActualitePage** (sous ActualiteIndexPage) au fur et à mesure

## Visualisation et Prévisualisation

### Voir une Page Publiée
- Dans l'éditeur de page, cliquez sur le bouton **"Live"** (icône d'œil, vert) en haut à droite
- Ou visitez directement l'URL de la page dans votre navigateur

### Prévisualiser un Brouillon
- Dans l'éditeur de page, cliquez sur le bouton **"Preview"** en haut
- Choisissez le mode de prévisualisation (Desktop, Mobile, Tablet)

### Accès Direct aux URLs
- **Homepage:** `http://127.0.0.1:8000/` (développement) ou `https://yourusername.pythonanywhere.com/` (production)
- **Pages standards:** `http://127.0.0.1:8000/slug-de-la-page/`
- **Actualités index:** `http://127.0.0.1:8000/actualites/`
- **Actualité individuelle:** `http://127.0.0.1:8000/actualites/slug-de-larticle/`

## URLs et Slugs

### Génération Automatique
- Le slug est généré automatiquement à partir du titre
- Exemple: "À propos" → `a-propos`
- Vous pouvez modifier le slug dans l'onglet **"Promote"** de l'éditeur de page

### Bonnes Pratiques pour les Slugs
- Utiliser uniquement des lettres minuscules, chiffres et tirets
- Éviter les caractères spéciaux et accents (convertis automatiquement)
- Garder les slugs courts et descriptifs
- Ne pas changer les slugs après publication (brise les liens existants)

## Configuration du Site

### Paramètres Wagtail

**Site par défaut:**
- Hostname: `localhost` (développement) ou votre domaine (production)
- Port: `80` (ou vide)
- Root page: **Home** (HomePage)

**Base URL pour l'admin:**
- Développement: `WAGTAILADMIN_BASE_URL = "http://127.0.0.1:8000"`
- PythonAnywhere: `WAGTAILADMIN_BASE_URL = "https://yourusername.pythonanywhere.com"`

### Modifier la Page Racine du Site

Si vous avez besoin de changer quelle page est la racine du site:

1. Allez dans **Settings → Sites** dans l'admin Wagtail
2. Cliquez sur le site (généralement "localhost")
3. Changez **"Root page"** pour pointer vers la page désirée
4. Cliquez sur **"Save"**

## Dépannage

### "Page not found" après publication
- Vérifiez que la page est **publiée** (pas en brouillon)
- Vérifiez que la page est bien enfant de **Home** ou d'une autre page publiée
- Vérifiez le slug dans l'onglet **"Promote"**

### Impossible de créer une ActualitePage sous Home
- Les ActualitePage doivent être créées sous une **ActualiteIndexPage**
- Créez d'abord l'ActualiteIndexPage, puis ajoutez les articles comme enfants

### URLs qui ne correspondent pas au menu
- Mettez à jour les liens dans `victimes_pesticides/templates/includes/header.html`
- Les URLs doivent correspondre aux slugs des pages réelles

### Bouton "Live" non visible
- Le bouton n'apparaît que pour les pages **publiées**
- Les brouillons n'ont que le bouton **"Preview"**

## Maintenance

### Réorganiser les Pages
- Dans l'admin, allez dans **"Pages"**
- Glissez-déposez les pages pour les réorganiser
- L'ordre affecte l'URL des pages enfants

### Supprimer une Page
- Cliquez sur le menu **"⋮"** à côté de la page
- Sélectionnez **"Delete"**
- **Attention:** La suppression d'une page parent supprime aussi tous ses enfants

### Dupliquer une Page
- Cliquez sur le menu **"⋮"** à côté de la page
- Sélectionnez **"Copy"**
- Choisissez où copier la page
- Modifiez le titre et le slug de la copie

## Ressources

- **Documentation Wagtail:** https://docs.wagtail.org/
- **Guide de démarrage du projet:** `DEMARRAGE-RAPIDE.md`
- **Guide de déploiement:** `DEPLOYMENT.md`
- **Modèles de pages:**
  - `home/models.py`
  - `pages_app/models.py`
  - `actualites/models.py`

---

*Document créé le 2025-11-07*
