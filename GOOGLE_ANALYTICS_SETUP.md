# Configuration Google Analytics pour VPQ

## ✅ Ce qui a été implémenté

### 1. Google Analytics 4 avec Consentement RGPD

**Fichiers modifiés:**
- `victimes_pesticides/templates/base.html` - Script GA4 avec consentement
- `victimes_pesticides/templates/includes/cookie_banner.html` - Bandeau de cookies
- `victimes_pesticides/static/css/victimes_pesticides.css` - Styles du bandeau

### 2. Fonctionnalités

✅ **Consentement requis** - GA ne se charge pas avant acceptation
✅ **Anonymisation IP** - Respect de la vie privée
✅ **localStorage** - Mémorisation du choix de l'utilisateur
✅ **Bandeau responsive** - Mobile et desktop
✅ **Animation fluide** - Slide up depuis le bas
✅ **Deux options** - Accepter ou Refuser

### 3. Comportement

1. **Première visite:**
   - Le bandeau apparaît en bas de page
   - GA4 n'est **pas chargé** par défaut
   - L'utilisateur doit choisir

2. **Si acceptation:**
   - GA4 se charge immédiatement
   - Le choix est sauvegardé dans localStorage
   - Le bandeau disparaît
   - Les pages futures ne montrent plus le bandeau

3. **Si refus:**
   - GA4 n'est **jamais chargé**
   - Le choix est sauvegardé
   - Le bandeau disparaît
   - Aucun tracking n'a lieu

4. **Visites suivantes:**
   - Le bandeau ne s'affiche plus
   - Le choix précédent est respecté

---

## 🔧 Configuration nécessaire

### Étape 1: Obtenir votre ID Google Analytics

1. Allez sur https://analytics.google.com/
2. Créez une propriété GA4 (si pas déjà fait)
3. Copiez votre **ID de mesure** (format: `G-XXXXXXXXXX`)

### Étape 2: Remplacer le placeholder

Dans le fichier `victimes_pesticides/templates/base.html`, remplacez **les 2 occurrences** de `G-XXXXXXXXXX`:

**Ligne ~48:**
```javascript
script.src = 'https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX';
```

**Ligne ~53:**
```javascript
gtag('config', 'G-XXXXXXXXXX', {
```

### Étape 3: Créer une page de politique de confidentialité

**Via l'admin Wagtail:**

1. Connectez-vous à `/admin/`
2. Créez une nouvelle **StandardPage**
3. **Titre:** "Politique de confidentialité"
4. **Slug:** `politique-de-confidentialite`
5. **Contenu suggéré:**

```markdown
# Politique de confidentialité

## Collecte de données

Nous utilisons Google Analytics pour comprendre comment les visiteurs utilisent notre site.

### Données collectées
- Pages visitées
- Durée de visite
- Source du trafic (Google, réseaux sociaux, etc.)
- Type d'appareil (mobile, desktop)
- Localisation approximative (ville/région)

### Données NON collectées
- Nom ou identité personnelle
- Adresse email
- Adresse IP complète (anonymisée)
- Informations sensibles

## Utilisation des cookies

Nous utilisons uniquement des cookies analytiques après votre consentement explicite.

**Type:** Cookies Google Analytics
**Durée:** 2 ans
**But:** Améliorer l'expérience utilisateur

## Vos droits

Vous pouvez à tout moment:
- Refuser les cookies lors de votre première visite
- Effacer les cookies de votre navigateur
- Contacter info@victimespesticidesquebec.ca pour toute question

## Partage de données

Vos données analytiques ne sont **jamais** partagées avec des tiers commerciaux.
Seule l'équipe de VPQ y a accès pour améliorer le site.

## Modifications

Cette politique peut être mise à jour. Dernière modification: [DATE]
```

6. Publiez la page

---

## 📊 Événements trackés automatiquement

Une fois GA4 activé, ces événements seront automatiquement suivis:

### Événements standards GA4:
- `page_view` - Chaque page visitée
- `session_start` - Début de session
- `first_visit` - Première visite
- `scroll` - Scroll de 90%
- `click` - Clics sur liens externes

### Événements personnalisés:
- `cookie_consent` - Acceptation/refus des cookies
  - Label: `accepted` ou `refused`

---

## 🧪 Tester l'implémentation

### Test 1: Vérifier que GA ne charge pas par défaut

1. Ouvrez le site en navigation privée
2. Ouvrez DevTools (F12) → Onglet "Network"
3. Rechargez la page
4. **Vérifiez:** Aucune requête vers `googletagmanager.com` ou `google-analytics.com`
5. Le bandeau de cookies doit apparaître

### Test 2: Vérifier l'acceptation

1. Cliquez sur "Accepter"
2. Le bandeau disparaît
3. Dans "Network", vous devez voir des requêtes vers `googletagmanager.com`
4. Rechargez la page
5. **Vérifiez:** Le bandeau ne réapparaît pas, GA se charge automatiquement

### Test 3: Vérifier le refus

1. Effacez le localStorage (DevTools → Application → Local Storage)
2. Rechargez la page
3. Cliquez sur "Refuser"
4. **Vérifiez:** Aucune requête GA, le bandeau disparaît
5. Rechargez la page
6. **Vérifiez:** Le bandeau ne réapparaît pas, pas de requête GA

### Test 4: Vérifier dans GA4

1. Allez sur https://analytics.google.com/
2. Sélectionnez votre propriété
3. Allez dans **Temps réel**
4. Visitez votre site (après avoir accepté les cookies)
5. **Vérifiez:** Vous apparaissez dans les visiteurs en temps réel

---

## 🔒 Conformité RGPD/Loi 25 (Québec)

Cette implémentation est conforme car:

✅ **Consentement explicite** - L'utilisateur doit cliquer pour accepter
✅ **Opt-in par défaut** - GA ne se charge pas automatiquement
✅ **Anonymisation IP** - `anonymize_ip: true`
✅ **Transparence** - Lien vers politique de confidentialité
✅ **Révocable** - L'utilisateur peut effacer ses cookies
✅ **Pas de cookies tiers** - Seulement GA4 first-party

---

## 🎯 Prochaines étapes (optionnel)

### 1. Événements personnalisés avancés

Ajoutez du tracking pour des actions spécifiques:

```javascript
// Dans vos templates, ajoutez:

// Track donation button clicks
<button onclick="gtag('event', 'click', {
    'event_category': 'donation',
    'event_label': 'zeffy_form'
});">
    Faire un don
</button>

// Track PDF downloads
<a href="/document.pdf" onclick="gtag('event', 'download', {
    'event_category': 'engagement',
    'event_label': 'rapport_pesticides.pdf'
});">
    Télécharger le rapport
</a>

// Track external links
<a href="https://example.com" onclick="gtag('event', 'click', {
    'event_category': 'outbound',
    'event_label': 'aspq_website'
});">
    Visiter ASPQ
</a>
```

### 2. Objectifs de conversion

Dans GA4, créez des objectifs pour mesurer:
- Soumission du formulaire de contact
- Clics sur le formulaire de don
- Temps passé > 3 minutes
- Lecture d'articles de nouvelles

### 3. Rapports personnalisés

Créez des rapports pour:
- Pages les plus visitées
- Taux de rebond par page
- Conversion donation
- Sources de trafic performantes

---

## 📞 Support

Si vous avez des questions:
- Consultez la documentation GA4: https://support.google.com/analytics/
- Contactez votre développeur
- Documentation Wagtail: https://docs.wagtail.org/

---

**Dernière mise à jour:** 2026-01-25
