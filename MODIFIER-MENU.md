# Comment modifier le menu principal depuis l'admin Wagtail

Le menu principal du site est dynamique et géré directement depuis l'interface Wagtail. Aucune modification de code n'est nécessaire!

## Comment ça fonctionne

Le menu affiche automatiquement toutes les pages qui ont l'option **"Afficher dans les menus"** activée, dans l'ordre de l'arborescence des pages.

## Ajouter une page au menu

1. **Allez dans l'admin**: https://victimespesticidesquebec.pythonanywhere.com/admin (ou http://127.0.0.1:8000/admin en local)
2. **Cliquez sur "Pages"** dans la barre latérale
3. **Trouvez la page** que vous voulez ajouter au menu
4. **Cliquez sur la page** pour l'éditer
5. **Allez dans l'onglet "Promouvoir"** (en haut)
6. **Cochez "Afficher dans les menus"**
7. **Cliquez sur "Publier"** (ou "Enregistrer le brouillon" si pas encore prêt)

✅ La page apparaîtra immédiatement dans le menu!

## Retirer une page du menu

1. **Éditez la page** concernée
2. **Allez dans l'onglet "Promouvoir"**
3. **Décochez "Afficher dans les menus"**
4. **Cliquez sur "Publier"**

❌ La page disparaîtra du menu (mais restera accessible via son URL directe).

## Changer l'ordre des éléments du menu

L'ordre du menu suit l'ordre des pages dans l'arborescence Wagtail.

### Méthode 1: Glisser-déposer (Recommandé)

1. **Allez dans "Pages"**
2. **Dans l'arborescence**, vous verrez toutes les pages sous "Home"
3. **Cliquez et maintenez** sur l'icône de poignée (⋮⋮) à gauche du nom de la page
4. **Glissez la page** vers le haut ou le bas
5. **Relâchez** pour positionner

L'ordre du menu sera mis à jour automatiquement!

### Méthode 2: Via le menu contextuel

1. **Cliquez sur les trois points (⋮)** à droite du nom de la page
2. **Sélectionnez "Déplacer"**
3. **Choisissez la nouvelle position**:
   - "Déplacer vers le haut"
   - "Déplacer vers le bas"
   - Ou choisissez une position spécifique dans la liste
4. **Confirmez**

## Exemple pratique

### Situation actuelle
```
Home
├── À propos (show_in_menus: ✓)
├── Quels risques? (show_in_menus: ✓)
├── Malades, que faire? (show_in_menus: ✓)
├── Alternatives (show_in_menus: ✓)
└── Soutenez VPQ (show_in_menus: ✓)
```

**Menu affiché**: À propos | Quels risques? | Malades, que faire? | Alternatives | Soutenez VPQ

### Pour mettre "Soutenez VPQ" en premier

1. Dans Pages, glissez "Soutenez VPQ" tout en haut (juste après "Home")
2. L'ordre devient:

```
Home
├── Soutenez VPQ (show_in_menus: ✓)
├── À propos (show_in_menus: ✓)
├── Quels risques? (show_in_menus: ✓)
├── Malades, que faire? (show_in_menus: ✓)
└── Alternatives (show_in_menus: ✓)
```

**Nouveau menu**: Soutenez VPQ | À propos | Quels risques? | Malades, que faire? | Alternatives

## Changer le texte d'un lien dans le menu

Le texte du menu est le **titre de la page** (champ "Titre" dans l'éditeur).

1. **Éditez la page**
2. **Modifiez le champ "Titre"**
3. **Publiez**

Le nouveau titre apparaîtra dans le menu.

**Note**: Si vous changez le titre, l'URL (slug) ne changera pas automatiquement pour préserver les liens existants.

## Ajouter une nouvelle page au menu

### Créer une nouvelle page

1. **Allez dans "Pages"**
2. **Cliquez sur les trois points (⋮)** à côté de "Home"
3. **Sélectionnez "Ajouter une page enfant"**
4. **Choisissez le type** (Page standard, Page de contact, etc.)
5. **Remplissez les informations**:
   - Titre (titre de la page et du menu)
   - Identifiant (URL de la page)
   - Contenu
6. **Onglet "Promouvoir"**: Cochez **"Afficher dans les menus"**
7. **Publiez**

### Positionner la nouvelle page

1. Glissez-déposez la page à la position désirée
2. Le menu sera mis à jour automatiquement

## Pages spéciales

### Page "Actualités"

Si vous avez une page d'actualités et que vous voulez qu'elle apparaisse dans le menu:

1. **Trouvez "Actualités"** dans Pages
2. **Éditez-la**
3. **Onglet "Promouvoir"**: Cochez **"Afficher dans les menus"**
4. **Positionnez-la** dans l'arborescence (généralement à la fin)

### Pages enfants (sous-menus)

**Note**: Le système actuel ne supporte pas les sous-menus déroulants. Seules les pages **directement sous "Home"** apparaissent dans le menu principal.

Si vous créez une page sous une autre page (ex: "Home > À propos > Notre équipe"), elle n'apparaîtra pas dans le menu principal, même avec "Afficher dans les menus" activé.

## Style spécial: "Soutenez VPQ"

La page "Soutenez VPQ" a un style spécial (bouton orange) dans le menu. C'est automatique si le slug de la page est `soutenez-vpq`.

Pour appliquer ce style à une autre page:
1. La page doit avoir le slug `soutenez-vpq`
2. Ou modifier le template `header.html` pour utiliser un autre slug

## Vérifications

Après avoir modifié le menu, vérifiez:

- ✅ Le menu s'affiche correctement sur **desktop**
- ✅ Le menu **mobile** fonctionne (cliquez sur l'icône hamburger ☰)
- ✅ L'ordre est correct
- ✅ Tous les liens fonctionnent (pas de 404)
- ✅ Le texte est correct
- ✅ La page "Soutenez VPQ" a bien son style orange (si applicable)

## Troubleshooting

### La page n'apparaît pas dans le menu

- ✅ Vérifiez que "Afficher dans les menus" est coché (onglet Promouvoir)
- ✅ Vérifiez que la page est **publiée** (pas en brouillon)
- ✅ Vérifiez que la page est **directement sous "Home"** (pas sous une autre page)
- ✅ Videz le cache du navigateur (Cmd+Shift+R / Ctrl+Shift+R)

### L'ordre ne change pas

- Assurez-vous de glisser-déposer au bon endroit
- Rafraîchissez la page admin après avoir déplacé
- Videz le cache du navigateur

### Le menu mobile ne s'affiche pas

- Cliquez sur l'icône hamburger (☰) en haut à droite
- Vérifiez que JavaScript est activé dans votre navigateur

## Limites actuelles

❌ **Pas de sous-menus déroulants**: Seules les pages de premier niveau (sous "Home") apparaissent
❌ **Pas de liens externes**: Le menu ne peut contenir que des pages Wagtail internes
❌ **Pas de séparateurs**: Impossible d'ajouter des séparateurs visuels entre les éléments

Si vous avez besoin de ces fonctionnalités, il faudra installer `wagtailmenus` ou créer un système de snippets personnalisé.

## Recommandations

### Pour un menu efficace

1. **Maximum 5-7 éléments** dans le menu principal
2. **Titres courts** et clairs (2-3 mots maximum)
3. **Ordre logique**: Du général au spécifique, ou par importance
4. **CTA visible**: Mettre "Soutenez VPQ" ou "Contact" en position stratégique (début ou fin)

### Ordre recommandé actuel

```
1. Soutenez VPQ (CTA principal - orange)
2. À propos
3. Quels risques?
4. Malades, que faire?
5. Alternatives
6. Contact (si activé)
```

Ou:

```
1. À propos
2. Quels risques?
3. Malades, que faire?
4. Alternatives
5. Soutenez VPQ (CTA principal - orange)
```

## Résumé rapide

**Pour ajouter au menu**: Page > Promouvoir > ☑ Afficher dans les menus > Publier

**Pour changer l'ordre**: Pages > Glisser-déposer les pages

**Pour retirer du menu**: Page > Promouvoir > ☐ Afficher dans les menus > Publier

**Pour changer le texte**: Page > Modifier "Titre" > Publier

---

**C'est tout!** Aucune modification de code nécessaire. 🎉
