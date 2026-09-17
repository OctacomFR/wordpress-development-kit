# SEO technique, métadonnées et Schema

Référence extraite sans réécriture du snapshot `docs/AGENTS.pre-skills-snapshot.md`.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 972-1079 -->

## 13. SEO technique et balisage

Le design ne doit jamais dégrader le HTML sémantique.

### 13.1. Structure HTML

Une page standard :

```text
<header>
<nav>
<main>
  <section>
    <h1>...</h1>
  </section>
  <section>
    <h2>...</h2>
    <h3>...</h3>
  </section>
</main>
<footer>
```

Règles :

- un H1 principal par page sauf cas exceptionnel justifié ;
- niveaux Hn cohérents ;
- ne jamais choisir H2/H3 uniquement pour la taille visuelle ;
- les titres décoratifs peuvent être des `div`, `span` ou paragraphes ;
- le contenu textuel important doit exister dans le DOM ;
- ne pas mettre du contenu SEO important uniquement dans `content:` CSS ;
- utiliser `<nav>` pour les navigations ;
- utiliser `<address>` avec discernement : uniquement pour les coordonnées réellement liées à l'auteur/propriétaire du document/section, sinon un bloc sémantique classique est acceptable.

### 13.2. Liens crawlables

Les liens internes importants doivent être de vrais liens :

```html
<a href="/page/">Texte descriptif</a>
```

Éviter :

```html
<span onclick="...">...</span>
<a onclick="...">...</a>
```

Le texte d'ancrage doit être descriptif lorsque cela reste compatible avec la maquette.

### 13.3. Yoast SEO

Si un connecteur Yoast est disponible :

- l'utiliser plutôt que d'écrire directement des métas privées en base ;
- lire l'état actuel avant modification ;
- préserver les valeurs éditoriales déjà définies ;
- vérifier title ;
- meta description ;
- canonical ;
- robots ;
- OpenGraph ;
- image sociale lorsque pertinente ;
- Schema généré.

Après modification, contrôler le rendu ou les données Yoast retournées pour l'URL.

Ne pas dupliquer manuellement dans le `<head>` ce que Yoast génère déjà.

### 13.4. Métadonnées

Chaque page importante doit avoir :

- `<title>` descriptif et propre à la page ;
- meta description utile et propre à la page ;
- canonical cohérente ;
- URL finale cohérente ;
- indexabilité vérifiée avant mise en production.

On peut rédiger un title/description à partir du contenu métier validé, mais on ne doit jamais ajouter une promesse ou information commerciale absente des sources.

### 13.5. Schema.org

Quand Yoast est présent, privilégier son graphe Schema et ses APIs/extensions plutôt que d'ajouter un second JSON-LD indépendant.

Pour un établissement local, utiliser le type le plus spécifique pertinent si le projet et les outils le permettent :

```text
LocalBusiness
Restaurant
Store
ProfessionalService
...
```

Ne renseigner que des informations vérifiées :

- nom ;
- URL ;
- adresse ;
- téléphone ;
- horaires ;
- logo ;
- image ;
- type de cuisine/menu lorsque pertinent et vérifié.

**Ne jamais fabriquer de `review` ou `aggregateRating` Schema à partir d'un widget d'avis du propre établissement.** Respecter les règles Google et le graphe Yoast existant.
