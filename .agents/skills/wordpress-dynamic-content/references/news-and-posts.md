# Actualités et articles dynamiques

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis renforcée pour rendre le Template Single Article obligatoire sur chaque site.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 866-950 -->

## 11. Actualités dynamiques WordPress

Une section actualités ne doit pas contenir deux cards copiées manuellement si le site possède de vrais articles.

### 11.1. Oxygen 6.x

Priorité :

1. créer un **Component `News Card`** unique pour le rendu d'un article ;
2. utiliser **Post Loop Builder** ;
3. sélectionner le Component `News Card` comme template de chaque résultat ;
4. configurer la query du Post Loop Builder avec le Query Builder visuel ;
5. utiliser une **Array Query** uniquement lorsqu'une query avancée ne peut pas être exprimée proprement autrement ;
6. PHP/WP_Query custom uniquement en dernier recours.

Ne pas utiliser les concepts Classic `Easy Posts` ou `Reusable Part` dans un nouveau projet Oxygen 6.

Le Component de card doit lier ses éléments à la **Dynamic Data** du post : titre, permalink, date, image à la une, extrait si demandé.

### 11.2. Query « deux dernières actualités »

Toujours résoudre le slug réel de la catégorie avec WordPress avant de configurer la query.

Configurer nativement l'équivalent suivant dans le Post Loop Builder. L'exemple PHP ci-dessous est une **spécification logique**, pas une obligation d'implémentation :

```php
$args = [
    'post_type'           => 'post',
    'post_status'         => 'publish',
    'posts_per_page'      => 2,
    'category_name'       => $actualites_category_slug,
    'orderby'             => 'date',
    'order'               => 'DESC',
    'ignore_sticky_posts' => true,
    'no_found_rows'       => true,
];
```

Règles :

- x articles maximum précisé par le user ou lui demander ;
- plus récent en premier ;
- date WordPress réelle ;
- image à la une réelle ;
- titre réel ;
- permalink réel ;
- pas de duplication d'une seconde query juste pour styler différemment le premier élément.

### 11.3. Premier article affiché dans l'état « hover »

Quand le brief demande :

```text
article 1 = apparence hover par défaut
article 2 = état normal
```

Le composant card doit rester unique.

Approche recommandée :

- construire un état normal ;
- construire un état hover/focus ;
- appliquer le même style hover au premier item au repos via une classe/modificateur ou un sélecteur de premier item ;
- conserver le vrai hover/focus sur tous les items.

Concept :

```css
.c-news-card:hover,
.c-news-card:focus-within,
/* sélecteur exact du premier item vérifié dans le DOM */
...:first-child .c-news-card {
  /* état hover */
}
```

Ne pas utiliser `:first-child` au hasard. Inspecter le DOM réellement généré par Post Loop Builder et vérifier que le sélecteur cible bien le premier résultat. Si la version 6.2 installée expose `Raw Mode`, il peut être utilisé pour supprimer les wrappers du loop lorsque cela simplifie le HTML sans casser le layout.

### 11.4. Cas limites

- 0 article : section vide propre ou message prévu par le projet, jamais faux contenu.
- 1 article : afficher un item sans casser la grille.
- image à la une absente : utiliser uniquement le fallback défini par le projet ; ne pas inventer une photo.
- contenu très long : utiliser titre/date/extrait selon la maquette, sans couper avec une hauteur rigide qui déborde sur mobile.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 1081-1094 -->

### 13.6. Articles

Le Template Oxygen 6 Single Article est toujours présent, même si aucun article n'est encore publié.

Lorsqu'un article réel est disponible, vérifier son rendu avec :

- titre visible ;
- date réelle ;
- image à la une ;
- contenu ;
- canonical ;
- données Article gérées par Yoast quand applicable ;
- liens vers les articles générés dynamiquement.

Créer ou réutiliser ce template même si la mission initiale porte sur l'accueil. La home et les loops doivent utiliser des permaliens compatibles avec lui. Relier titre, date, image à la une et contenu aux données dynamiques WordPress ; ne pas créer de faux article destiné à la livraison pour compenser l'absence de contenu réel.
