# Éditabilité, mutations MCP et code custom

Référence extraite sans réécriture du snapshot `docs/AGENTS.pre-skills-snapshot.md`.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 646-673 -->

## 7. Exigence critique : la page doit rester éditable dans Oxygen

Une implémentation est refusée si :

- sélectionner une section dans Oxygen fait disparaître le design ;
- le builder ne charge pas les styles essentiels ;
- tout le layout dépend d'un JS exécuté seulement côté front ;
- le contenu visible n'existe que dans des pseudo-éléments CSS ;
- une grosse section est reconstruite dans un unique bloc HTML/PHP alors qu'elle doit être modifiable visuellement ;
- la structure Oxygen est remplacée par un énorme blob HTML/import HTML alors que des éléments natifs suffisent ;
- les styles dépendent de sélecteurs DOM hyper fragiles produits par Oxygen.

Exemples attendus : une galerie simple utilise des Containers, liens et Images éditables ; une FAQ utilise un vrai Accordion si cet élément existe ; une liste d'articles utilise Dynamic Data et un loop ; un carrousel utilise l'élément natif disponible seulement si le besoin justifie un carrousel.

### 7.1. Test « Builder Editability » obligatoire

Pour chaque section majeure :

1. ouvrir la page dans Oxygen ;
2. sélectionner la section ;
3. sélectionner ses enfants importants ;
4. vérifier que le rendu reste visible ;
5. modifier temporairement une propriété simple puis l'annuler ;
6. vérifier qu'aucun JS ne doit être déclenché pour « restaurer » le design ;
7. après toute modification faite hors de l'éditeur ouvert, recharger Oxygen avant de sauvegarder ;
8. sauvegarder uniquement après validation.

Le front ET le builder doivent être cohérents.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 1401-1475 -->

## 19. Règles MCP WordPress + Oxygen 6

### Lecture

Avant toute mutation, inspecter les abilities du serveur MCP puis lire l'objet actuel :

- page ;
- Template ;
- Header ;
- Footer ;
- Component et ses propriétés éditables ;
- Classes / Selectors ;
- Variables ;
- loop/query ;
- menu ;
- post ;
- catégorie ;
- média ;
- métadonnée SEO.

Si des abilities Oxygen natives existent, les préférer à l'écriture directe de post meta, JSON interne ou HTML importé.

Lors d'une mutation externe à Oxygen, noter quels objets ont changé. Considérer tout éditeur déjà ouvert comme périmé jusqu'à son rechargement.

### Écriture

- utiliser les abilities Oxygen natives les plus spécifiques disponibles ;
- modifier l'objet existant lorsqu'il correspond au besoin ;
- créer uniquement quand il n'existe pas ;
- préserver slug et statut lorsque la demande ne nécessite pas leur changement ;
- ne pas publier automatiquement un brouillon si l'utilisateur n'a pas demandé de publication ;
- ne pas supprimer un Template, Header, Footer, Component, Selector ou Variable partagé sans analyse des usages ;
- faire des modifications aussi atomiques que l'API le permet.

### Échec

En cas d'erreur :

1. lire l'erreur ;
2. relire l'état si l'écriture a pu être partiellement appliquée ;
3. ne pas répéter une requête destructive à l'identique ;
4. corriger la cause ;
5. vérifier l'état après succès ;
6. si un outil de preview Oxygen est exposé, rendre/inspecter l'élément ou la page modifiée.

---

## 20. Quand utiliser du code custom

Du code custom est acceptable pour :

- query WordPress impossible à exprimer proprement avec Post Loop Builder / Query Builder / Array Query ;
- interaction spécifique non disponible avec States, Nested Selectors ou Interactions Engine ;
- petite amélioration progressive ;
- SVG décoratif exporté / composant technique ;
- logique dynamique réellement nécessaire.

Avant d'en écrire, documenter quel élément ou mécanisme Oxygen a été recherché et pourquoi il ne couvre pas le besoin. Pour un widget interactif custom, appliquer le pattern WAI-ARIA correspondant, conserver les éléments HTML natifs possibles et tester clavier, tactile, focus et annonce des états.

Il n'est pas acceptable de :

- reconstruire toute une page en HTML dans un Code Block ;
- contourner les Components, Variables, Selectors ou loops Oxygen parce que c'est plus rapide ;
- injecter toutes les sections via JS ;
- écrire un mini page-builder maison ;
- dupliquer une fonction WordPress/Oxygen existante.

Le code custom doit être :

- scoped ;
- commenté lorsque sa raison n'est pas évidente ;
- stable dans le builder ;
- compatible responsive ;
- accessible ;
- sans dépendance inutile.
