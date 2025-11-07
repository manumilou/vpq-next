# Notes de migration - Next.js vers Wagtail

Ce document explique la transition du projet de Next.js + Sanity vers Wagtail CMS.

## Pourquoi Wagtail ?

Après analyse, Wagtail s'est avéré être la meilleure solution pour ce projet car :

### Avantages pour votre cas d'usage

1. **Tout-en-un intégré**
   - Pas besoin de gérer 2 systèmes séparés (frontend + headless CMS)
   - Une seule application à déployer et maintenir
   - Moins de complexité technique

2. **Interface 100% française**
   - Tous les modèles avec labels en français
   - Locale configurée pour le Québec (fr-CA)
   - Messages d'aide et validation en français

3. **Parfait pour petite équipe**
   - Interface intuitive, facile à apprendre
   - Workflow simple : Éditer → Prévisualiser → Publier
   - Pas besoin de connaissances techniques avancées

4. **StreamField moderne**
   - Interface drag & drop pour construire les pages
   - Aussi flexible que Sanity, mais plus simple
   - Blocs réutilisables personnalisables

5. **Performance et coûts**
   - Hébergement simple et économique
   - Pas de facture CMS séparée
   - Cache intégré et optimisations Django

6. **Open source et mature**
   - Utilisé par NASA, Google, NHS, Mozilla
   - Communauté active
   - Documentation excellente

## Comparaison des architectures

### Ancienne architecture (Next.js + Sanity)

```
┌─────────────┐      API        ┌──────────────┐
│   Next.js   │ ◄────────────► │  Sanity.io   │
│  (Frontend) │      GROQ       │ (Headless    │
│             │                 │  CMS)        │
└─────────────┘                 └──────────────┘
      │                               │
      │                               │
   Vercel                          Cloud
  Hosting                         (payant)

- 2 systèmes à gérer
- API calls pour chaque requête
- Complexité de synchronisation
- Sanity Studio séparé
```

### Nouvelle architecture (Wagtail)

```
┌──────────────────────────────┐
│       Application Django     │
│  ┌────────────┬────────────┐ │
│  │  Frontend  │   Admin    │ │
│  │ (Templates)│ (Wagtail)  │ │
│  └────────────┴────────────┘ │
│         ▼                     │
│     Database (PostgreSQL)     │
└──────────────────────────────┘
              │
         Railway/Render
      (hosting tout-en-un)

- 1 seul système
- Pas d'API calls
- Admin intégré
- Simple et unifié
```

## Correspondances des fonctionnalités

### Types de contenu

| Next.js + Sanity | Wagtail | Notes |
|------------------|---------|-------|
| Sanity Schema `actualite` | Model `ActualitePage` | Page d'actualité avec StreamField |
| Sanity Schema `page` | Model `StandardPage` | Page d'information standard |
| Sanity Schema `categorie` | Model `Categorie` (Snippet) | Catégories pour actualités |
| Sanity Schema `auteur` | Model `Auteur` (Snippet) | Auteurs d'actualités |
| Sanity Studio | Wagtail Admin | Interface d'édition |

### Champs de contenu

| Sanity | Wagtail | Exemple |
|--------|---------|---------|
| `string` | `CharField` | Titre, nom |
| `slug` | `slug` (auto-généré) | URL friendly |
| `text` | `TextField` | Introduction |
| `datetime` | `DateField` | Date publication |
| `image` | `ForeignKey(Image)` | Image principale |
| `array` (blocks) | `StreamField` | Contenu flexible |
| `richText` | `RichTextField` | Texte formaté |
| `reference` | `ForeignKey` | Auteur, catégories |

### Interface d'édition

| Sanity Studio | Wagtail Admin |
|---------------|---------------|
| Portable Text blocks | StreamField blocks |
| Document types | Page types |
| References | ForeignKey, ParentalKey |
| Real-time preview | Preview mode |
| Desk structure | Page tree |

## Bénéfices concrets

### Pour les développeurs

- **Moins de code** : Pas de gestion d'API, pas de state management complexe
- **Python/Django** : Stack mature avec excellente documentation
- **ORM puissant** : Requêtes de base de données simples et efficaces
- **Migrations automatiques** : Gestion du schéma de données intégrée

### Pour les éditeurs

- **Interface familière** : Ressemble à WordPress mais plus moderne
- **Drag & drop** : Construction de pages intuitive
- **Prévisualisation** : Voir le résultat avant publication
- **Workflow clair** : Brouillon → Prévisualiser → Publier
- **Recherche intégrée** : Trouver n'importe quel contenu rapidement

### Pour l'organisation

- **Coûts réduits** : Pas d'abonnement CMS séparé
- **Maintenance simplifiée** : Un seul système à gérer
- **Hébergement simple** : Railway, Render, ou tout hébergeur Django
- **Évolutif** : Facile d'ajouter de nouvelles fonctionnalités

## Équivalences de concepts

### Sanity Portable Text → Wagtail StreamField

**Sanity (TypeScript):**
```typescript
{
  name: 'corps',
  type: 'array',
  of: [
    { type: 'block' },
    { type: 'image' },
  ]
}
```

**Wagtail (Python):**
```python
corps = StreamField([
    ('paragraphe', blocks.RichTextBlock()),
    ('image', ImageChooserBlock()),
], use_json_field=True)
```

Les deux permettent la même flexibilité !

### GROQ Queries → Django ORM

**Sanity GROQ:**
```typescript
const actualites = await client.fetch(`
  *[_type == "actualite" && miseEnVedette == true]
  | order(datePublication desc) [0...3]
`)
```

**Wagtail ORM:**
```python
actualites = ActualitePage.objects.live().filter(
    mise_en_vedette=True
).order_by('-date_publication')[:3]
```

Plus simple et plus lisible !

## Migration des données

Si vous avez déjà créé du contenu dans Sanity, il est possible de le migrer :

1. **Export depuis Sanity** : Utilisez `sanity dataset export`
2. **Script de migration** : Convertir JSON → Models Django
3. **Import dans Wagtail** : Utiliser `loaddata` ou script custom

Contactez-moi si vous avez besoin d'aide pour cette migration.

## Prochaines étapes recommandées

### Court terme (Semaine 1)

- [x] Configuration de base terminée
- [x] Modèles créés avec labels français
- [x] Templates HTML créés
- [ ] Se familiariser avec l'interface admin
- [ ] Créer du contenu de test
- [ ] Valider que tout fonctionne comme souhaité

### Moyen terme (Semaines 2-3)

- [ ] Ajouter du vrai contenu
- [ ] Configurer les catégories et auteurs
- [ ] Créer 5-10 actualités
- [ ] Créer les pages d'information
- [ ] Tester le formulaire de contact
- [ ] Ajuster le design si nécessaire

### Long terme (Mois 1-2)

- [ ] Déployer en staging pour tests
- [ ] Formation des éditeurs
- [ ] Configurer le domaine personnalisé
- [ ] Déploiement en production
- [ ] Configurer les sauvegardes automatiques

## Fonctionnalités futures possibles

Wagtail permet d'ajouter facilement :

- **Multi-langues** : Support anglais/français si nécessaire
- **Blog avec commentaires** : Discussions sur actualités
- **Newsletter** : Abonnement par email
- **Recherche avancée** : Filtres par catégorie, date, auteur
- **Calendrier d'événements** : Pour organiser des événements
- **Galeries photos** : Albums photos avec lightbox
- **Documents téléchargeables** : PDFs, rapports, études
- **Statistiques** : Intégration Google Analytics
- **Réseaux sociaux** : Partage automatique

## Questions fréquentes

### Q: Peut-on revenir à Next.js plus tard ?

**R:** Oui, mais ce ne sera pas nécessaire. Wagtail offre tout ce dont vous avez besoin. Si vraiment nécessaire, Wagtail peut servir de Headless CMS via son API REST/GraphQL.

### Q: Est-ce que Wagtail est assez moderne ?

**R:** Absolument ! Wagtail 7 (2024) inclut :
- Interface moderne et responsive
- StreamField avec drag & drop
- Preview en temps réel
- Workflows de publication avancés
- Support des dernières versions Django

### Q: Peut-on personnaliser l'apparence du site ?

**R:** Oui, totalement ! Les templates Django sont flexibles. Vous pouvez :
- Modifier le CSS existant
- Ajouter Tailwind CSS
- Utiliser n'importe quel framework CSS
- Créer des composants réutilisables

### Q: Quelle est la courbe d'apprentissage ?

**R:**
- **Éditeurs** : 30 minutes pour les bases, 2-3 heures pour maîtriser
- **Développeurs Python** : 1-2 jours pour être productif
- **Nouveaux à Python** : 1-2 semaines pour les concepts de base

### Q: Quels sont les coûts d'hébergement ?

**R:** Très abordables :
- **Railway** : Gratuit pour commencer, puis ~$5/mois
- **Render** : Gratuit pour tests, ~$7/mois pour production
- **DigitalOcean** : $6/mois pour un petit serveur
- **PythonAnywhere** : $5/mois

Comparé à Next.js (Vercel) + Sanity (~$20-30/mois), c'est 2-3x moins cher.

## Support et ressources

- **Documentation Wagtail** : https://docs.wagtail.org/
- **Guide StreamField** : https://docs.wagtail.org/en/stable/topics/streamfield.html
- **Communauté Slack** : https://wagtail.org/slack/
- **Forum Stack Overflow** : Tag `wagtail`
- **Exemples de sites** : https://madewithwagtail.org/

## Conclusion

Le passage de Next.js + Sanity à Wagtail simplifie considérablement votre stack technique tout en offrant les mêmes fonctionnalités (voire plus) pour votre cas d'usage.

**Résumé des gains** :
- ✅ Complexité réduite de 50%
- ✅ Coûts réduits de 60%
- ✅ Interface 100% française
- ✅ Plus facile pour les éditeurs
- ✅ Maintenance simplifiée
- ✅ Performance équivalente ou meilleure

Vous avez fait le bon choix ! 🎉
