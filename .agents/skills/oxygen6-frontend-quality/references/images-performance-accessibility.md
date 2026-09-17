# Images, performance et accessibilité

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis renforcée avec la politique obligatoire WebP/SVG.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 1110-1273 -->

## 14. Images

### 14.0. Formats obligatoires

- convertir en WebP, avant import ou utilisation, tout raster maîtrisé affiché sur le site ;
- ne livrer aucun JPEG, PNG ou GIF comme image de contenu ;
- conserver les originaux de travail hors des assets chargés en production lorsqu'ils restent utiles ;
- utiliser au maximum le SVG pour les logos, icônes, pictogrammes, formes graphiques et illustrations réellement vectorielles ;
- optimiser et assainir chaque SVG, conserver son `viewBox` et supprimer scripts, références externes et métadonnées inutiles ;
- ne pas autoriser globalement des uploads SVG non fiables dans WordPress ;
- ne pas convertir une photographie ou un raster en faux SVG. Ces médias restent des rasters et doivent être fournis en WebP ;
- respecter uniquement les formats techniques supplémentaires qu'une plateforme impose réellement, par exemple certains fichiers de favicon ou de partage social. Cette contrainte ne permet pas de conserver des rasters non-WebP dans le contenu des pages.

### 14.1. Alt

- Image informative : `alt` descriptif.
- Image décorative : `alt=""`.
- Logo : alt correspondant au nom de l'entité lorsqu'il apporte cette information.
- Ne pas bourrer les `alt` de mots-clés.
- Ne pas importer ou afficher deux fois le même média pour résoudre un problème de mise en page.

### 14.2. Responsive images

Laisser WordPress produire/utiliser `srcset` et `sizes` lorsque possible.

Respecter le rôle du média :

- `object-fit: contain` pour un logo, pictogramme, portrait ou document qui ne doit pas être coupé ;
- `object-fit: cover` seulement pour une vignette volontairement recadrée ;
- miniature optimisée dans une grille, liée à l'original si un agrandissement est demandé ;
- ratio d'origine conservé sauf recadrage explicitement prévu par la maquette.

Toujours éviter qu'une image dépasse son conteneur :

```css
img {
  max-width: 100%;
  height: auto;
}
```

### 14.3. Dimensions et CLS

Chaque image doit avoir des dimensions intrinsèques ou un ratio réservé.

Préférer :

```html
<img src="..." width="1200" height="800" alt="...">
```

ou un conteneur avec `aspect-ratio` si le layout l'exige.

### 14.4. LCP

L'image principale visible immédiatement :

- ne doit pas être `loading="lazy"` ;
- doit être découvrable tôt ;
- peut recevoir `fetchpriority="high"` si elle est très probablement l'élément LCP et si l'implémentation le permet proprement ;
- ne doit pas dépendre d'un JS tardif ;
- éviter de la cacher dans un background CSS si une vraie balise image permet la même fidélité et une meilleure découverte de ressource.

### 14.5. Images sous la ligne de flottaison

- `loading="lazy"` lorsque pertinent ;
- `decoding="async"` lorsque le système le gère correctement ;
- formats et tailles adaptés ;
- ne pas charger une image 4000 px pour une card de 400 px.

### 14.6. Galerie ou carrousel

Utiliser une galerie quand la personne doit parcourir un album. Utiliser un carrousel quand le nombre d'éléments visibles doit rester faible, que l'ordre raconte une séquence ou que le besoin produit le demande.

Galerie classique :

- grille native et éditable, avec vignettes cohérentes ;
- cible par défaut de 4 colonnes desktop, 3 tablette et 2 mobile, adaptée si Figma indique autre chose ;
- lien vers l'original si agrandissement demandé ;
- focus clavier visible et chargement différé sous la ligne de flottaison ;
- même traitement pour les albums d'une même page.

Vrai carrousel :

- élément Oxygen/Swiper existant avant toute implémentation custom ;
- glissement tactile, flèches, pagination et clavier si ces commandes sont présentes ;
- nombre de cartes adapté à chaque largeur ;
- hauteur compatible avec les contenus longs ;
- aucune couleur bleue par défaut héritée du navigateur ou de Swiper ;
- autoplay seulement s'il sert le contenu, avec arrêt ou contrôle accessible lorsque requis.

Une simple rangée à défilement horizontal ne doit pas être présentée comme un carrousel si le brief demande de vraies commandes.

---

## 15. Performance

Objectifs Core Web Vitals recommandés :

```text
LCP <= 2,5 s
INP <= 200 ms
CLS <= 0,1
```

à viser au 75e percentile mobile et desktop.

### 15.1. CSS

- mutualiser les styles dans les classes ;
- ne pas dupliquer la même déclaration sur 30 IDs Oxygen ;
- éviter les sélecteurs très profonds ;
- ne pas importer une librairie CSS complète pour une animation ou une grille simple ;
- pas de CSS bloquant externe inutile.

### 15.2. JavaScript

- appliquer l'amélioration progressive : contenu, navigation et actions essentielles disponibles avant l'exécution du script ;
- JavaScript minimal ;
- vanilla JS si aucun besoin d'une dépendance supplémentaire ;
- ne pas ajouter jQuery si le composant peut fonctionner sans et que jQuery n'est pas nécessaire ;
- listeners légers ;
- pas de boucle ou observer permanent inutile ;
- limiter le travail main-thread ;
- différer les scripts non critiques lorsque possible ;
- éviter les animations JS pour des transitions réalisables en CSS.

Prévoir un rendu sans JavaScript pour les composants enrichis : navigation mobile accessible, accordéons lisibles ou ouverts, carrousels présentés comme une liste statique, coordonnées et liens de carte visibles, médias accompagnés d'un lien direct lorsque pertinent. Un message `<noscript>` peut expliquer la perte d'une fonction secondaire, mais ne remplace jamais le contenu masqué.

### 15.3. Fonts

- utiliser les polices exactes de Figma ;
- ne pas substituer silencieusement une police ;
- limiter les poids réellement chargés ;
- privilégier un hébergement performant/self-host si la licence et le projet le permettent ;
- ne jamais importer plusieurs fois la même font ;
- utiliser un fallback cohérent ;
- surveiller les layout shifts causés par le chargement des polices.

### 15.4. Iframes / widgets tiers

- charger sous le fold lorsque possible ;
- réserver l'espace avant chargement ;
- n'ajouter que les widgets réellement nécessaires ;
- mesurer leur impact avant d'empiler 5 scripts marketing.

---

## 16. Accessibilité

Le minimum attendu :

- navigation clavier ;
- focus visible ;
- liens et boutons correctement typés ;
- `aria-label` sur les liens icône seuls ;
- menu mobile accessible ;
- textes alternatifs ;
- pas de texte important uniquement en image ;
- pas d'information uniquement par couleur ;
- hover doublé d'un focus ;
- animations réduites si préférence utilisateur ;
- ordre DOM logique ;
- labels de formulaire réels lorsque des formulaires sont dans le scope.

Si la charte Figma contient un contraste manifestement insuffisant :

- ne pas modifier silencieusement la charte ;
- relever la paire couleur/fond problématique ;
- proposer la correction minimale conforme ;
- appliquer la décision utilisateur.

### 16.1. États globaux

Définir et vérifier dès le début : liens normaux, hover, `:focus-visible`, état actif du menu, boutons primaires/secondaires, liens sur fond sombre, téléphone et email. L'état courant doit fonctionner sur chaque page, en desktop et dans le menu mobile. Aucun bleu navigateur, WordPress ou Swiper ne doit apparaître par défaut sauf choix explicite de la charte.
