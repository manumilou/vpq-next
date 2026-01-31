# Exemple d'utilisation du Carrousel de témoignages

## Aperçu visuel

Voici à quoi ressemblera le carrousel sur votre site:

### Vue Desktop
```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│                Témoignages de victimes                       │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                                                        │ │
│  │   ┌────────┐                                          │ │
│  │   │        │   "Les pesticides ont gravement          │ │
│  │   │ Photo  │    affecté ma santé et celle de ma       │ │
│  │   │ ronde  │    famille. Grâce à VPQ, j'ai trouvé     │ │
│  │   │        │    du soutien et de l'information        │ │
│  │   └────────┘    pour faire valoir mes droits."        │ │
│  │                                                        │ │
│  │                 ─────────────────────                 │ │
│  │                 Marie Tremblay                         │ │
│  │                 Résidente près de champs               │ │
│  │                 Montérégie                             │ │
│  │                                                        │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│                   ◀    ●  ○  ○    ▶                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Vue Mobile
```
┌───────────────────────┐
│  Témoignages          │
│                       │
│   ┌──────────┐        │
│   │          │        │
│   │  Photo   │        │
│   │  ronde   │        │
│   │          │        │
│   └──────────┘        │
│                       │
│  "Les pesticides ont  │
│   gravement affecté   │
│   ma santé..."        │
│                       │
│  ───────────────      │
│  Marie Tremblay       │
│  Résidente            │
│  Montérégie           │
│                       │
│   ◀   ●  ○  ○   ▶    │
│                       │
└───────────────────────┘
```

## Exemple réel pour VPQ

### Configuration recommandée

**Page**: "À propos" ou "Notre impact"

**Titre de la section**: "Témoignages de victimes"

**Défilement automatique**: ✓ Activé

### Témoignage 1 - Marie Tremblay
```
Photo: [Photo de Marie - femme d'environ 45 ans]

Témoignage:
"Pendant 10 ans, j'ai vécu à proximité de champs agricoles intensivement traités.
Ma famille et moi avons développé de graves problèmes de santé. Grâce à Victimes
des Pesticides du Québec, j'ai trouvé du soutien, de l'information et l'aide
nécessaire pour faire valoir mes droits. Aujourd'hui, je me bats pour que
d'autres familles n'aient pas à vivre ce que nous avons vécu."

Nom: Marie Tremblay

Rôle: Résidente affectée

Localisation: Montérégie
```

### Témoignage 2 - Jean Dubois
```
Photo: [Photo de Jean - homme d'environ 55 ans avec casquette]

Témoignage:
"En tant qu'agriculteur, j'ai manipulé des pesticides pendant 25 ans sans
vraiment connaître les risques. J'ai développé une maladie de Parkinson
précoce. VPQ m'a accompagné dans mes démarches à la CNESST et m'a aidé à
obtenir une reconnaissance et une compensation. L'association fait un travail
essentiel pour les travailleurs agricoles."

Nom: Jean Dubois

Rôle: Agriculteur retraité

Localisation: Centre-du-Québec
```

### Témoignage 3 - Dr. Sophie Martin
```
Photo: [Photo professionnelle de Sophie]

Témoignage:
"Mes recherches sur les impacts sanitaires des pesticides confirment ce que
les victimes témoignent depuis des années. L'association Victimes des Pesticides
du Québec joue un rôle crucial en donnant une voix à ces personnes et en
sensibilisant le public et les décideurs. Leur travail est fondamental pour
protéger la santé publique."

Nom: Dr. Sophie Martin

Rôle: Chercheuse en santé environnementale

Localisation: Université Laval, Québec
```

### Témoignage 4 - Pierre Gagnon
```
Photo: [Photo de Pierre - apiculteur avec ruches]

Témoignage:
"J'ai perdu 60% de mes ruches après l'épandage de néonicotinoïdes dans les
champs voisins. Au-delà de la perte économique, c'est toute une vie de travail
qui a été détruite. VPQ m'a soutenu dans ma bataille juridique et continue de
se battre pour une meilleure réglementation des pesticides."

Nom: Pierre Gagnon

Rôle: Apiculteur

Localisation: Lanaudière
```

## Code pour l'admin Wagtail

Voici exactement ce que vous devez faire dans l'interface admin:

1. Allez sur votre page "À propos" ou créez-en une nouvelle
2. Dans le champ "Corps de la page", cliquez "+ Ajouter"
3. Sélectionnez "Carrousel de témoignages"
4. Remplissez:

```
┌─────────────────────────────────────────┐
│ Titre de la section:                    │
│ [Témoignages de victimes]               │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Témoignages:                            │
│                                         │
│ ┌─ Témoignage ────────────────────────┐ │
│ │ Photo: [Choisir une image]          │ │
│ │ Témoignage: [Texte du témoignage]   │ │
│ │ Nom: [Marie Tremblay]               │ │
│ │ Rôle: [Résidente affectée]          │ │
│ │ Localisation: [Montérégie]          │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ [+ Ajouter témoignage]                  │
└─────────────────────────────────────────┘

☑ Défilement automatique
```

## Conseils de rédaction

### Pour les témoignages

**DO ✓**
- Rester authentique et humain
- Utiliser des phrases courtes et directes
- Mettre l'accent sur l'impact personnel
- Mentionner le rôle de VPQ
- Inclure des détails concrets (durée, lieu, type d'exposition)

**DON'T ✗**
- Utiliser du jargon médical complexe
- Écrire des paragraphes trop longs
- Être trop générique ou vague
- Oublier de mentionner la localisation
- Négliger l'aspect émotionnel

### Longueur idéale

- **Court (50-80 mots)**: Impactant, facile à lire
- **Moyen (80-120 mots)**: Équilibré entre détails et lisibilité ✓ Recommandé
- **Long (120-150 mots)**: Maximum acceptable

### Ton à adopter

- **Empathique**: Montrer la souffrance et l'espoir
- **Factuel**: Inclure des détails concrets
- **Positif**: Mettre en avant le rôle de VPQ
- **Humain**: Parler de personne à personne

## Photos recommandées

### Style
- **Format**: Carré (1:1)
- **Résolution**: 800x800px minimum
- **Qualité**: Haute qualité, bien éclairée
- **Cadrage**: Portrait en buste ou gros plan du visage
- **Fond**: Neutre ou flou (mise au point sur la personne)
- **Expression**: Authentique, ni trop souriant ni trop sérieux

### Types de photos

1. **Victimes**: Photos naturelles, authentiques
2. **Professionnels**: Photos plus formelles
3. **Agriculteurs/Apiculteurs**: Dans leur environnement de travail
4. **Chercheurs**: Photos professionnelles ou en laboratoire

## Variations possibles

### Pour la page d'accueil
- **Titre**: "Ils nous font confiance"
- **3 témoignages courts** (60-80 mots chacun)
- **Défilement automatique**: Oui

### Pour la page "Impact"
- **Titre**: "Nos victoires"
- **4-5 témoignages** sur les succès juridiques
- **Défilement automatique**: Oui

### Pour la page "Rejoignez-nous"
- **Titre**: "Témoignages de bénévoles"
- **3 témoignages** de personnes engagées
- **Défilement automatique**: Non (pour permettre la lecture complète)

## Mise en ligne

Une fois configuré:

1. **Cliquez sur "Publish"** pour publier immédiatement
2. **Ou "Save draft"** pour sauvegarder en brouillon
3. **Testez** sur desktop et mobile
4. **Vérifiez** que les images se chargent correctement
5. **Testez** la navigation (flèches, points, clavier)
6. **Observez** le défilement automatique

---

Bon courage avec vos témoignages! 💚
