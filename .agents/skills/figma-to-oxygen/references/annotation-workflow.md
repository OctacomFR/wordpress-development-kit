# Workflow obligatoire des annotations Figma

Les annotations font partie des spécifications du design. La reproduction visuelle seule ne suffit pas.

## Barrière avant implémentation

Avant toute génération, construction ou modification fondée sur Figma :

1. définir le périmètre Figma concerné, avec les nodes, frames, composants, variantes et sections associés ;
2. récupérer toutes les annotations présentes dans ce périmètre ;
3. lire chaque annotation intégralement ;
4. créer la matrice de suivi décrite ci-dessous ;
5. analyser les effets directs et indirects ;
6. appliquer l'ordre de priorité aux ambiguïtés et contradictions, puis demander une décision à l'utilisateur seulement si elles restent non résolues ; soumettre également les impossibilités techniques et leur impact.

La barrière `FIGMA_ANNOTATIONS_REVIEWED` est franchie seulement lorsque toutes les annotations du périmètre sont recensées, comprises, reliées à leurs cibles et sans blocage non résolu. Aucune implémentation dépendante de Figma ne commence avant cette barrière.

Si le connecteur ne permet pas d'accéder aux annotations ou si leur exhaustivité ne peut pas être vérifiée, signaler précisément la limite et demander à l'utilisateur un accès, un export, des captures ou une copie des annotations. L'implémentation reste bloquée. Ne jamais affirmer que les annotations ont été lues sans preuve.

## Priorité interne à l'analyse Figma

Appliquer cet ordre :

1. instructions explicites de la tâche ;
2. annotations Figma ;
3. structure et propriétés réelles des composants et nodes Figma ;
4. rendu visuel de la maquette ;
5. interprétation personnelle, uniquement lorsqu'aucune source supérieure ne répond.

Une annotation explicite prévaut sur une interprétation fondée uniquement sur l'apparence. Les documents métier validés restent prioritaires pour les données métier selon l'ordre général du projet.

## Matrice obligatoire

Créer une ligne par annotation :

```text
ANNOTATION_ID / repère :
NODE / FRAME / COMPOSANT / SECTION :
TEXTE INTÉGRAL :
IMPACT DIRECT :
IMPACTS INDIRECTS / AUTRES OCCURRENCES :
BREAKPOINTS / ÉTATS / VARIANTES CONCERNÉS :
OBJETS OXYGEN / WORDPRESS CONCERNÉS :
CONFLIT OU BLOCAGE :
DÉCISION UTILISATEUR, SI REQUISE :
STATUT : recensée | comprise | implémentée | vérifiée
PREUVE : URL, node, capture ou test
```

Conserver le texte intégral de l'annotation. Un résumé peut compléter la ligne, jamais remplacer la source.

## Analyse de chaque annotation

Identifier concrètement les effets sur :

- structure du composant ;
- disposition, ordre et groupement des éléments ;
- responsive et changements entre breakpoints ;
- visibilité, masquage et espace résiduel ;
- comportements, interactions, sticky, scroll et navigation ;
- textes, médias, liens et destinations ;
- dimensions, espacements, alignements et ratios ;
- Components, propriétés, variantes et occurrences réutilisées ;
- contraintes techniques et fonctionnelles.

Croiser l'annotation avec le contexte visuel, la structure réelle du node, ses parents, ses enfants, ses variantes et ses consommateurs.

## Effets indirects

Pour chaque ligne, poser explicitement la question : « Qu'est-ce que cette annotation implique pour le reste de la page ou du composant ? »

Contrôler notamment :

- une image déplacée sur mobile implique l'ordre et le responsive du conteneur complet ;
- un élément masqué implique les autres breakpoints et l'espace libéré ;
- un Component à réutiliser implique la recherche de toutes les occurrences similaires ;
- un sticky implique le Header, le conteneur parent, le scroll et les éléments voisins ;
- une destination de bouton implique le vrai lien dans WordPress/Oxygen ;
- un élément toujours visible peut modifier les règles de son parent et de ses variantes.

Une correction reste locale seulement lorsque l'annotation n'impose aucun changement aux autres occurrences ou objets partagés. Sinon, transmettre la modification au propriétaire de l'objet global.

## Ambiguïté, contradiction ou impossibilité

Une annotation ambiguë, techniquement impossible ou contradictoire bloque l'implémentation affectée lorsqu'une décision requise reste non résolue après application de l'ordre de priorité. Si une instruction explicite de la tâche résout déjà la contradiction, documenter cette résolution et ses impacts sans redemander la même décision.

Documenter :

- le texte exact ;
- les nodes et objets concernés ;
- la contradiction ou la limite technique ;
- les conséquences directes et indirectes ;
- la décision précise attendue de l'utilisateur.

Demander ensuite une instruction explicite. Ne pas ignorer l'annotation, choisir silencieusement une interprétation ou publier une solution provisoire fondée sur une hypothèse.

## Validation finale

Avant de déclarer la page terminée :

- vérifier que chaque annotation du périmètre figure dans la matrice ;
- vérifier que chaque ligne a atteint le statut `vérifiée` ou possède un blocage utilisateur explicite ;
- contrôler les effets visuels, responsive, fonctionnels et techniques ;
- contrôler les effets indirects et les autres occurrences ;
- comparer le résultat au contexte visuel du node ;
- conserver une preuve pour chaque annotation appliquée.

Une annotation pertinente oubliée ou non vérifiée bloque la livraison.
