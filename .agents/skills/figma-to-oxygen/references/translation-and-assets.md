# Traduction Figma vers Oxygen

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis renforcée avec la politique obligatoire WebP/SVG.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 355-445 -->

## 5. Traduire Figma vers Oxygen proprement

### 5.1. Ne pas copier le code Figma brut

Le code design-to-code peut contenir beaucoup de :

```text
position:absolute
left/top fixes
width/height 1920px
React
Tailwind
wrappers purement visuels
```

Ce n'est pas la structure de production attendue.

Convertir l'intention en :

- Sections / Divs Oxygen ;
- flexbox ;
- CSS Grid lorsqu'il s'agit vraiment d'une grille ;
- colonnes structurées pour les compositions texte/image ;
- `max-width` + largeur fluide ;
- paddings/gaps ;
- pseudo-éléments uniquement pour décoratif léger ;
- assets SVG/images exacts pour les formes complexes.

### 5.2. Absolute positioning

Autorisé pour :

- décoration ;
- éléments volontairement flottants ;
- badge superposé ;
- formes graphiques ;
- rail social fixed ;
- éléments dont l'overlap est réellement visible dans Figma.

Interdit comme technique principale pour reconstruire toute une page desktop.

### 5.3. Assets Figma

- Utiliser les images et SVG réels exportés par Figma lorsqu'ils font partie du design.
- Ne jamais recréer « à peu près » un logo, une icône ou un SVG complexe.
- Les URLs d'assets retournées par Figma MCP sont temporaires : **ne jamais les laisser en production**.
- Avant tout import ou usage sur le site, convertir obligatoirement chaque raster maîtrisé en WebP. Ne pas importer sa version JPEG, PNG ou GIF comme asset de contenu. Seuls les formats techniques supplémentaires explicitement imposés par une plateforme échappent à cette règle, jamais les images affichées dans les pages.
- Pour les logos, icônes, pictogrammes, formes graphiques et illustrations vectorielles, utiliser au maximum le SVG exact fourni ou exporté depuis Figma. Ne pas les rasteriser sans contrainte technique démontrée.
- Optimiser et assainir les SVG avant usage. Conserver un `viewBox`, supprimer scripts, références externes et métadonnées inutiles, et ne pas ouvrir globalement les uploads SVG non fiables dans WordPress.
- Ne jamais envelopper un raster dans un SVG pour prétendre satisfaire cette règle. Une photographie ou une illustration bitmap reste un raster et doit devenir un WebP.
- Télécharger/importer seulement les assets durables et optimisés dans WordPress Media ou dans l'emplacement prévu par le projet.
- Conserver le ratio/cadrage Figma via `object-fit`, `object-position` ou l'outil Oxygen adapté.
- Si Figma ou le dossier projet fournit un favicon, exporter le node exact, générer les formats requis par WordPress et vérifier le rendu dans l'onglet du navigateur. Ne pas fabriquer une icône approchante.

### 5.4. Variables Oxygen 6

Utiliser en priorité le système **Oxygen > Variables** au lieu d'ajouter un deuxième design system en CSS brut.

Si aucun système existant ne couvre la nouvelle charte, créer des collections limitées, par exemple :

```text
Brand Colors
- color-primary
- color-secondary
- color-text
- color-surface

Typography
- font-heading
- font-body

Spacing
- space-xs
- space-sm
- space-md
- space-lg
- space-section

Layout
- container-max
- radius-sm
- radius-md
- radius-lg
```

Règles :

- réutiliser une Variable existante lorsque son rôle correspond ;
- ne pas dupliquer une Variable avec un nom différent pour la même valeur/rôle ;
- utiliser les types Oxygen adaptés : Color, Number, Unit, Font Family, Image URL ;
- préférer les Variables dans les contrôles Oxygen plutôt que `var(...)` injecté partout à la main ;
- les overrides de Variables servent aux variantes ponctuelles, pas à contourner un Component mal conçu ;
- CSS custom `:root` uniquement si une contrainte technique ne peut pas être couverte nativement et après vérification de l'existant ;
- ne pas créer 50 variables pour des valeurs utilisées une seule fois.
