---
name: skill-gate
description: "Évaluer, sélectionner et charger les skills applicables avant toute unité d'exécution observable, puis refaire ce préflight quand l'objectif, la cible, les permissions ou le périmètre changent. Utiliser avant outils, mutations, délégations, actions externes et réponse finale."
---

# Préflight des skills

Exécuter ce skill avant toute unité d'exécution observable. Son rôle est de sélectionner et charger les bonnes procédures. Il ne donne aucune permission et n'élargit jamais la demande de l'utilisateur.

## Définir l'unité d'exécution

Regrouper seulement les actions de bas niveau qui partagent :

- le même objectif concret ;
- les mêmes cibles et le même propriétaire d'écriture ;
- la même classe d'action : lecture, mutation, délégation, action externe ou finalisation ;
- les mêmes permissions et informations requises ;
- le même ensemble de skills applicables.

Plusieurs lectures d'un même audit peuvent former une unité. Une nouvelle page, un autre objet Oxygen, une mutation après une phase de lecture, un changement de destination externe ou une réponse finale après élargissement du périmètre impose un nouveau préflight.

## Exécuter le préflight

1. Reformuler en interne l'objectif exact, la classe d'action, la cible, le périmètre et le résultat attendu.
2. Lire le catalogue de skills réellement disponible dans la session. Ne jamais inventer un skill ou supposer qu'un skill local est chargé.
3. Sélectionner `skill-gate`, puis le minimum de skills métier dont les descriptions couvrent toute l'unité. Un skill explicitement demandé par l'utilisateur est obligatoire.
4. Lire intégralement chaque `SKILL.md` sélectionné. Lire aussi chaque référence que le skill rend obligatoire avant l'action concernée.
5. Vérifier les préconditions : informations requises, autorisation, cible/ID, propriétaire unique, état partagé, capacité du modèle, sauvegarde ou retour arrière et preuves attendues.
6. Si une précondition requise manque, appliquer la règle de blocage du dépôt. Continuer seulement les travaux indépendants autorisés en lecture seule.
7. Annoncer brièvement les skills utilisés et leur utilité dans le canal de suivi avant qu'ils causent une action ou une pause.
8. Agir dans le périmètre. Refaire le préflight dès qu'un élément des étapes 1 à 5 change.

Utiliser mentalement cette fiche courte, sans l'ajouter à un journal contenant des secrets :

```text
UNITÉ : objectif et classe d'action
CIBLE / PROPRIÉTAIRE : objet exact
SKILLS : skill-gate + skills métier
PRÉCONDITIONS : confirmées | blocage précis
PREUVES ATTENDUES : contrôles observables
```

Si aucun skill métier ne s'applique, utiliser `skill-gate` seul. Ne pas charger des skills voisins « au cas où ».

## Sous-agents

Le coordinateur fournit des skills pressentis dans la mission. Le sous-agent doit :

1. exécuter son propre préflight ;
2. vérifier le catalogue disponible dans son contexte ;
3. confirmer ou corriger la sélection ;
4. lire lui-même les instructions ;
5. signaler les skills réellement appliqués dans son retour.

Un sous-agent ne reçoit pas automatiquement les permissions, le contexte complet ni l'état de sélection du parent. Un nouvel agent constitue toujours une nouvelle frontière de préflight.

## Séparer routage et autorisation

Le choix de skills reste un contrôle de procédure. Il ne doit jamais décider seul si une mutation est autorisée. Les permissions viennent de la demande utilisateur, des politiques supérieures et des limites déterministes du système. Les IDs, révisions, propriétaires et verrous d'objets partagés restent contrôlés séparément.

Les hooks locaux injectent ce rappel au modèle, mais ne prouvent pas qu'un skill a été compris ou appliqué. Ne pas construire un faux jeton de capacité à partir d'une simple déclaration du modèle.

Pour modifier les hooks, concevoir un exécuteur strict ou définir des tests de couverture, lire intégralement [references/enforcement-and-tests.md](references/enforcement-and-tests.md) avant toute modification.

## Finaliser

Avant la réponse finale :

- confirmer que le périmètre n'a pas changé depuis le dernier préflight ;
- vérifier que chaque skill sélectionné a été appliqué jusqu'à ses critères de sortie ;
- distinguer les preuves réelles, les limites et les éléments non vérifiés ;
- ne jamais annoncer une garantie fournie uniquement par un prompt ou un hook d'injection.
