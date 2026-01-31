# Carrousel de témoignages

Ce document explique comment utiliser le nouveau bloc "Carrousel de témoignages" dans les pages standard.

## Qu'est-ce que c'est?

Le carrousel de témoignages est un bloc de contenu qui permet d'afficher plusieurs témoignages avec photos de manière élégante et interactive. Les témoignages défilent automatiquement (optionnel) et les visiteurs peuvent naviguer manuellement entre eux.

## Fonctionnalités

✅ **Photos circulaires** - Photos des témoins affichées en format circulaire professionnel
✅ **Défilement automatique** - Option pour faire défiler automatiquement les témoignages toutes les 5 secondes
✅ **Navigation manuelle** - Boutons précédent/suivant et indicateurs à points
✅ **Navigation clavier** - Utiliser les flèches gauche/droite du clavier
✅ **Pause au survol** - Le défilement automatique se met en pause quand on survole le carrousel
✅ **Responsive** - S'adapte parfaitement aux mobiles et tablettes
✅ **Animations fluides** - Transitions douces et élégantes entre les témoignages

## Comment l'utiliser

### 1. Créer ou modifier une page standard

1. Allez dans l'admin Wagtail: http://127.0.0.1:8000/admin
2. Créez une nouvelle "Page standard" ou modifiez-en une existante
3. Dans le champ "Corps de la page", cliquez sur "+ Ajouter"
4. Sélectionnez "Carrousel de témoignages"

### 2. Configurer le carrousel

**Titre de la section** (optionnel)
- Ajoutez un titre pour la section des témoignages
- Exemple: "Ce qu'ils disent de nous", "Témoignages de victimes"

**Défilement automatique** (optionnel)
- Cochez cette case pour activer le défilement automatique
- Les témoignages changeront toutes les 5 secondes
- Le défilement se met en pause au survol ou lors de la navigation manuelle

### 3. Ajouter des témoignages

Pour chaque témoignage, vous devez fournir:

**Photo** (requis)
- Photo du témoin
- Format recommandé: carré (ex: 400x400px minimum)
- Sera affichée en cercle

**Témoignage** (requis)
- Le texte du témoignage
- Peut faire plusieurs lignes
- Sera affiché avec des guillemets stylisés

**Nom** (requis)
- Nom complet du témoin
- Exemple: "Marie Tremblay", "Jean-François Dubois"

**Rôle/Titre** (optionnel)
- Fonction, profession ou titre du témoin
- Exemple: "Agricultrice", "Apiculteur", "Chercheur en santé publique"
- Affiché en vert

**Localisation** (optionnel)
- Ville, région ou information géographique
- Exemple: "Montérégie", "Québec", "Laurentides"
- Affiché en gris clair

### 4. Exemple concret

Voici un exemple de configuration:

```
Titre: Témoignages de victimes

Témoignage 1:
- Photo: [photo de Marie]
- Témoignage: "Les pesticides ont gravement affecté ma santé et celle de ma famille. Grâce à VPQ, j'ai trouvé du soutien et de l'information pour faire valoir mes droits."
- Nom: Marie Tremblay
- Rôle: Résidente près de champs agricoles
- Localisation: Montérégie

Témoignage 2:
- Photo: [photo de Jean]
- Témoignage: "En tant qu'agriculteur, j'ai été exposé pendant des années. VPQ m'a aidé à comprendre mes droits et à obtenir compensation."
- Nom: Jean Dubois
- Rôle: Agriculteur
- Localisation: Centre-du-Québec

Témoignage 3:
- Photo: [photo de Sophie]
- Témoignage: "L'association fait un travail essentiel pour sensibiliser le public aux dangers des pesticides."
- Nom: Dr. Sophie Martin
- Rôle: Chercheuse en santé environnementale
- Localisation: Université Laval

Défilement automatique: ✓ Activé
```

## Apparence visuelle

### Desktop (grands écrans)
```
┌─────────────────────────────────────────────────┐
│       Témoignages de victimes                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  [Photo]    "Les pesticides ont gravement      │
│  circulaire  affecté ma santé..."              │
│             ────────────────                    │
│             Marie Tremblay                      │
│             Résidente près de champs            │
│             Montérégie                          │
│                                                 │
│         ◀  ● ○ ○  ▶                            │
└─────────────────────────────────────────────────┘
```

### Mobile (petits écrans)
```
┌─────────────────────────┐
│  Témoignages de victimes│
├─────────────────────────┤
│                         │
│      [Photo]            │
│     circulaire          │
│                         │
│  "Les pesticides ont    │
│   gravement affecté..." │
│  ──────────────         │
│  Marie Tremblay         │
│  Résidente              │
│  Montérégie             │
│                         │
│     ◀  ● ○ ○  ▶        │
└─────────────────────────┘
```

## Conseils d'utilisation

### Nombre de témoignages
- **Recommandé**: 3-5 témoignages
- **Minimum**: 1 témoignage (mais le carrousel n'apparaît pas vraiment utile)
- **Maximum**: Pas de limite technique, mais évitez d'en avoir trop (10 max conseillé)

### Longueur des témoignages
- **Idéal**: 2-4 phrases (50-150 mots)
- **Court**: Plus impactant et facile à lire
- **Long**: Peut être difficile à lire dans le carrousel

### Photos
- **Format**: Carré de préférence (1:1)
- **Taille**: 400x400px minimum, 800x800px recommandé
- **Qualité**: Bonne qualité, bien éclairée
- **Style**: Photos de visages en gros plan fonctionnent mieux

### Ordre des témoignages
Les témoignages s'affichent dans l'ordre où vous les ajoutez. Vous pouvez:
- Les réorganiser en glissant-déposant dans l'admin
- Mettre les témoignages les plus impactants en premier

## Navigation

Les visiteurs peuvent naviguer de 4 façons:

1. **Automatique**: Les témoignages défilent seuls si activé (5 secondes)
2. **Boutons**: Flèches gauche/droite de chaque côté
3. **Indicateurs**: Points en bas (cliquer pour aller directement)
4. **Clavier**: Touches flèche gauche/droite

## Accessibilité

Le carrousel est conçu pour être accessible:

- ✅ Labels ARIA pour les boutons
- ✅ Navigation au clavier complète
- ✅ Pause automatique au survol
- ✅ Indicateurs visuels clairs
- ✅ Texte alternatif pour les images

## Exemples de cas d'usage

### 1. Page "À propos"
Montrer les témoignages de personnes touchées par les pesticides, pour humaniser la cause.

### 2. Page "Impact"
Témoignages de personnes qui ont obtenu justice ou compensation grâce à VPQ.

### 3. Page d'accueil
Section de témoignages pour établir la crédibilité et la confiance.

### 4. Page "Rejoignez-nous"
Témoignages de membres actifs ou bénévoles pour encourager l'engagement.

## Dépannage

### Le carrousel ne s'affiche pas
- Vérifiez que vous avez ajouté au moins 1 témoignage
- Assurez-vous que la migration a été appliquée: `python manage.py migrate`
- Collectez les fichiers statiques: `python manage.py collectstatic`

### Le défilement automatique ne fonctionne pas
- Vérifiez que l'option "Défilement automatique" est cochée
- Testez dans un navigateur privé (peut être bloqué par des extensions)

### Les photos ne s'affichent pas
- Vérifiez que les images sont bien uploadées dans l'admin
- Confirmez que les images existent dans la collection Wagtail

### Le style n'est pas correct
- Videz le cache du navigateur (Cmd+Shift+R sur Mac, Ctrl+Shift+R sur Windows)
- Re-collectez les fichiers statiques: `python manage.py collectstatic --clear`

## Prochaines améliorations possibles

Fonctionnalités qui pourraient être ajoutées plus tard:

- [ ] Vitesse de défilement configurable
- [ ] Effet de transition configurable (fade, slide, etc.)
- [ ] Support vidéo au lieu de photo
- [ ] Lien vers page détaillée du témoignage
- [ ] Note/étoiles pour chaque témoignage
- [ ] Export des témoignages en PDF

## Support technique

Si vous rencontrez des problèmes avec le carrousel de témoignages, consultez:

1. Ce document en premier
2. La documentation Wagtail: https://docs.wagtail.org/
3. Les logs d'erreur dans l'admin Wagtail

---

**Bon usage du carrousel de témoignages!** ✨

