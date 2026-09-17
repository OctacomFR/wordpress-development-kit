# Architecture réutilisable Oxygen 6

Référence extraite sans réécriture du snapshot `docs/AGENTS.pre-skills-snapshot.md`.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 449-642 -->

## 6. Architecture réutilisable Oxygen 6.x

### 6.1. Architecture globale recommandée

Oxygen 6 possède des objets dédiés. Ne pas recréer artificiellement l'architecture Classic.

Architecture générique recommandée :

```text
Oxygen
├── Header "Global"              -> Location/Conditions adaptées
├── Footer "Global"              -> Location/Conditions adaptées
├── Templates
│   ├── Page / contenu si nécessaire
│   │   └── Template Content Area
│   ├── Single Article si dans le scope
│   └── Archives si dans le scope
├── Components
│   ├── Hero
│   ├── Button / CTA variant si utile
│   ├── News Card
│   ├── Social Rail
│   └── autres patterns réellement répétés
├── Variables
│   ├── Colors
│   ├── Typography
│   ├── Spacing
│   └── Layout / Radius si pertinent
└── Classes / Selectors
```

Un Header/Footer global n'a pas besoin d'être dupliqué dans chaque Template. Utiliser les types **Headers** et **Footers** d'Oxygen 6, avec `Everywhere` ou des conditions plus fines selon le projet.

### 6.2. Template Content Area

Lorsqu'un Template doit afficher le contenu propre à chaque page/post :

- insérer **Template Content Area** à l'emplacement prévu ;
- ne jamais utiliser l'ancien concept `Inner Content` ;
- vérifier qu'un template MCP créé possède bien son Template Content Area lorsqu'il doit afficher du contenu spécifique ;
- ne pas mettre le contenu unique d'une page directement dans le Template générique.

### 6.3. Header

Créer/modifier un objet **Header Oxygen 6** dédié.

Le header doit :

- respecter strictement Figma ;
- utiliser le menu WordPress réel si un menu existe ;
- avoir des liens réels ;
- gérer l'état courant ;
- rester sticky sur toutes les pages et à tous les breakpoints ;
- être responsive ;
- être navigable au clavier ;
- conserver un comportement utilisable sans hover ;
- ne pas dépendre d'un JS lourd pour une simple navigation.

Le sticky est obligatoire. Utiliser en priorité le réglage natif Oxygen ou `position: sticky` avec un `top` et un `z-index` maîtrisés. Mesurer la hauteur réelle du header à chaque breakpoint et réserver l'espace nécessaire au premier hero ou au contenu suivant. Vérifier qu'aucun parent avec `overflow` incompatible ne désactive le sticky. Aucun titre, ancre ou contrôle ne doit passer sous le header.

Configuration :

- `Location: Everywhere` pour un header global, sauf besoin contraire ;
- Conditions uniquement si nécessaires ;
- vérifier Priority lorsqu'il existe plusieurs headers applicables.

Si un menu mobile est nécessaire :

- utiliser un bouton réel ;
- `aria-expanded` doit refléter l'état ;
- ouverture/fermeture clavier ;
- fermeture Escape lorsque possible ;
- focus visible ;
- préférer les interactions/éléments natifs Oxygen 6 quand ils couvrent proprement le besoin.

### 6.4. Footer

Créer/modifier un objet **Footer Oxygen 6** dédié.

Le footer doit :

- être défini une seule fois pour les zones concernées ;
- reprendre les coordonnées réelles ;
- utiliser `mailto:` pour les emails ;
- utiliser `tel:` pour les numéros ;
- avoir de vrais liens pour mentions légales / confidentialité ;
- réutiliser les réseaux sociaux réels ;
- ne pas hard-coder l'année si une valeur dynamique propre existe déjà ;
- utiliser le menu WordPress réel du footer pour afficher **Politique de protection des données**, **Mentions légales** et, lorsqu'elles existent ou sont applicables, les **Conditions générales de vente** ;
- afficher le crédit de réalisation Octacom sur tous les sites, même si Figma ne le montre pas. Cette règle de livraison explicite prime sur l'absence du crédit dans la maquette.

Markup du crédit :

```html
<span>Réalisation</span><span id="copyright-logo"></span>
```

Style de base :

```css
#copyright-logo {
  display: inline-block;
  background: url('https://www.octacom.fr/images/logo.png') no-repeat center;
  /* Variante sur fond sombre : https://www.octacom.fr/images/logo-blanc.png */
  background-size: contain;
  height: 17px;
  width: 80px;
}
```

Choisir le logo rouge/classique ou blanc selon le contraste du fond. Conserver le markup demandé. Scoper les règles complémentaires au Footer pour éviter qu'un ancien style global ou le rail social ne les écrase.

Vérifier Location, Conditions et Priority comme pour le Header.

### 6.5. Hero réutilisable = Component

Si plusieurs pages partagent le même squelette de hero, créer un **Component Hero**.

Utiliser des **Component Properties** pour les valeurs qui changent par instance, par exemple :

```text
hero.title
hero.text
hero.image
hero.cta_label
hero.cta_url
hero.variant
```

Ne créer que les propriétés réellement nécessaires.

Règles :

- styles/layout dans le Component ;
- contenu variable via Component Properties ou Dynamic Data selon le contexte ;
- variantes limitées et explicites ;
- utiliser le child visibility toggle si un CTA ou média est optionnel et que la version installée le supporte ;
- ne pas créer un Component qui nécessite ensuite 40 overrides locaux.

### 6.6. Components : règle de factorisation

Créer un Component quand au moins un de ces cas est vrai :

- le pattern apparaît à plusieurs endroits ;
- il doit être maintenu globalement ;
- il sert de template à un Post Loop Builder ;
- il a des variations maîtrisées exprimables via Component Properties.

Ne pas convertir chaque petit `div` en Component. Un Component doit représenter une vraie unité de design ou fonctionnelle.

### 6.7. Variables

Avant d'ajouter des valeurs brutes répétées, inspecter les Variables existantes.

Collections conseillées si le projet n'en a pas :

```text
Brand Colors
Typography
Spacing
Layout
```

Préférer les Variables Oxygen aux valeurs CSS dupliquées quand elles représentent un token global. Utiliser les overrides de Variables uniquement pour une vraie variante locale.

### 6.8. Classes et Selectors

Toujours réutiliser les classes/selectors existants adaptés avant d'en créer de nouveaux.

Si aucune convention projet n'existe, utiliser une convention claire :

```text
l-section
l-container
c-button
c-button--primary
c-button--secondary
c-hero
c-news-card
c-social-rail
u-sr-only
```

Dans Oxygen 6, le styling est centré sur les classes. Éviter de dupliquer des styles élément par élément.

Utiliser :

- States pour `:hover`, `:active`, `:focus-visible`, etc. ;
- Nested Selectors pour les sous-éléments et sélecteurs relationnels simples ;
- Selectors manuels pour les cas avancés réellement nécessaires.

Avant de modifier une classe partagée, lire toutes ses propriétés et rechercher ses usages. Avec les imports de règles Oxygen/MCP qui remplacent la règle du breakpoint au lieu de fusionner les propriétés, réécrire la règle complète. Lire les avertissements retournés après chaque import. Pour un besoin local, préférer une classe ciblée à une surcharge globale. Contrôler le front et les pages consommatrices après chaque modification globale.

Éviter les noms visuels fragiles : `blue-box-2`, `rectangle-54`, `left-thing`.
