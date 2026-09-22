# Responsive, motion et sticky

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis mise à jour avec les animations d'apparition obligatoires d'Oxygen 6.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 677-772 -->

## 8. Responsive : règles obligatoires

Le desktop Figma n'est pas une page à réduire proportionnellement.

Le responsive doit respecter l'intention du design avec :

- largeur fluide ;
- `max-width` ;
- flex/grid ;
- images responsives ;
- typographie fluide lorsque pertinent ;
- gaps adaptatifs ;
- réorganisation sémantique des colonnes ;
- aucune barre horizontale parasite.

### 8.1. Breakpoints

Utiliser les breakpoints configurés dans le projet Oxygen 6.x. Ne pas inventer une seconde stratégie concurrente si le site possède déjà ses breakpoints.

Tester au minimum autour de :

```text
320
360
390
480
768
1024
1280
1440
1920 px
```

Tester également **entre** les breakpoints : le bug qui apparaît à 930 px compte autant que celui qui apparaît exactement à 1024 px.

### 8.2. Règles de layout

- pas de largeur de contenu fixe égale au canvas Figma ;
- `width: 100%` + `max-width` pour les conteneurs ;
- une vraie grille de cards peut devenir 3 -> 2 -> 1 colonnes ;
- une section texte/image peut passer en colonne ;
- préserver l'ordre de lecture logique en mobile ;
- ne pas utiliser `order` pour produire un ordre visuel qui contredit fortement l'ordre DOM accessible ;
- adapter les tableaux à leur contenu et au viewport : colonnes compactes, défilement horizontal annoncé ou présentation alternative accessible lorsque nécessaire ;
- les textes ne doivent pas être coupés par des hauteurs fixes ;
- limiter les `height` fixes aux éléments réellement dimensionnés par le design ;
- préférer `min-height`, ratio ou contenu naturel pour les sections.

Pour une section texte/média, la quantité de contenu et le format du média déterminent les proportions, pas une grille 50/50 automatique :

- étendre le texte sur toute la largeur si aucun média n'est prévu ;
- placer un média panoramique au-dessus du texte lorsque la colonne latérale créerait de grands vides ;
- limiter la hauteur visible d'un portrait sans le déformer ;
- déplacer la suite d'un texte sous le média si une colonne devient nettement plus longue ;
- vérifier séparément les variantes média à gauche et média à droite ;
- garder un rythme vertical régulier, souvent 12 à 18 px entre paragraphes liés, puis ajuster à la typographie réelle ;
- réduire les paddings ou CTA trop hauts sans supprimer l'espace qui marque un changement de sujet.

### 8.3. Hover et tactile

Aucune information essentielle ne doit exister uniquement au hover.

Tout état hover important doit disposer d'un équivalent :

- `:focus-visible` / `:focus-within` au clavier ;
- comportement utilisable au tactile ;
- contenu toujours accessible dans le DOM.

### 8.4. Motion

Les animations d'apparition sont un critère de livraison obligatoire. Toute page construite ou refondue en comporte sur ses principaux blocs, notamment le hero, les entrées de section et les groupes de contenu lorsque leur animation sert la hiérarchie visuelle. Cette règle s'applique même lorsque la charte, Figma ou les annotations ne prévoient aucune animation. Leur absence bloque la livraison.

Utiliser d'abord l'onglet Animations natif d'Oxygen 6. Il permet de régler le type d'entrée, la durée, le délai, la distance, l'easing et la répétition. Réserver les Interactions aux déclencheurs ou actions qui dépassent une animation d'entrée native.

Lorsque Figma définit le mouvement, reprendre ses paramètres. Dans le cas contraire, définir un système sobre et cohérent avec la direction artistique. Éviter d'animer chaque élément ou d'introduire des flips, zooms et déplacements marqués sans justification visuelle.

Pour les animations non essentielles :

```css
@media (prefers-reduced-motion: reduce) {
  /* réduire/supprimer les transitions et animations non indispensables */
}
```

Le style par défaut de tout élément animé doit être son état final visible. Appliquer l'état initial masqué ou décalé uniquement après l'initialisation réussie du mécanisme d'animation. Ne jamais enregistrer dans Oxygen un contenu essentiel durablement en `opacity: 0`, `visibility: hidden`, `display: none` ou hors écran dans l'attente d'un script.

Une animation d'apparition ne doit jamais laisser le contenu invisible si JavaScript est désactivé, bloqué, en erreur ou si son observer ne se déclenche pas. Tester le chargement direct, le retour arrière, le mobile, `prefers-reduced-motion` et la page avec JavaScript désactivé.

Avant livraison, vérifier dans le navigateur que les animations d'apparition se déclenchent réellement au chargement et au scroll avec le mouvement normal. Refaire le contrôle avec `prefers-reduced-motion: reduce` et avec JavaScript désactivé. Le contenu doit rester visible dans ces deux derniers cas.

### 8.5. Sticky ciblé

Réserver `position: sticky` aux médias latéraux qui accompagnent un texte long :

- desktop seulement, sauf preuve contraire dans la maquette ;
- `top` calculé avec la hauteur réelle du header sticky et une marge visible ;
- désactivation sous 1024 px par défaut ;
- exclusion des vidéos, carrousels et médias panoramiques placés au-dessus du texte ;
- hauteur maximale d'un portrait limitée à la fenêtre sans déformation ;
- arrêt naturel à la fin de la section par le bon conteneur parent.

Ne jamais appliquer un sticky global à tous les médias.
