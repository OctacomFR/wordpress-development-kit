---
name: oxygen6-architecture
description: "Créer ou modifier le socle partagé Oxygen 6 : Variables, Classes, Selectors, Components, Templates, Header, Footer, éditabilité, mutations MCP et code custom de dernier recours."
---

# Architecture Oxygen 6

Construire avec les primitives réellement disponibles dans la version installée. Ne jamais transposer automatiquement une recette Oxygen Classic.

## Références à lire selon la tâche

- Cible, version et primitives : [references/oxygen6-target-and-primitives.md](references/oxygen6-target-and-primitives.md).
- Ordre de construction : [references/implementation-order.md](references/implementation-order.md).
- Header, Footer, Templates, Components, Variables et Classes : [references/reusable-architecture.md](references/reusable-architecture.md).
- Éditabilité, lecture/écriture MCP, erreurs et code custom : [references/editability-mcp-custom-code.md](references/editability-mcp-custom-code.md).

Pour une création de socle complète, lire les quatre références. Pour une correction ciblée, lire la référence concernée et toute référence qui décrit un objet partagé touché.

## Décision native d'abord

Chercher dans cet ordre : élément Oxygen natif disponible, Component existant, composition avec Containers/Dynamic Data/States/Nested Selectors/Interactions, puis code custom ciblé. Documenter pourquoi le natif ne suffit pas avant le dernier recours.

## Objets globaux

- Un seul propriétaire d'écriture pour le Header, le Footer, les Templates, Components, Variables, Classes, Selectors et menus globaux.
- Lire l'objet complet et ses usages avant modification.
- Une importation de règle peut remplacer la règle entière au breakpoint : réécrire toutes les propriétés nécessaires et lire les avertissements.
- Après une mutation externe, recharger l'éditeur Oxygen avant de sauvegarder.
- Tester les consommateurs de tout objet partagé modifié.

## Invariants du shell

- Le Header Oxygen est dédié, utilise le menu WordPress réel et reste sticky sur toutes les pages et tous les breakpoints. Compenser sa hauteur réelle et vérifier `top`, `z-index`, ancêtres `overflow`, ancres et contenu masqué.
- Le Footer Oxygen est unique, utilise les coordonnées et réseaux réels, le menu WordPress réel pour les pages légales, une année dynamique si disponible et le crédit Octacom prévu dans la référence.
- Les Templates qui affichent le contenu propre aux pages/posts utilisent `Template Content Area`.
- Les données répétées utilisent Dynamic Data et les loops Oxygen appropriés.

## Éditabilité

Le front et le builder doivent rester cohérents. Rejeter les gros blobs HTML/PHP, les styles dépendant de sélecteurs DOM fragiles, les contenus essentiels en pseudo-éléments et les layouts restaurés seulement par JavaScript.

## Sous-agents

Utiliser `octacom-parallel-delivery`. Pendant l'écriture mono-propriétaire du socle, déléguer en lecture seule l'inventaire des usages, le contrôle des conditions/priorités, la vérification builder et la régression des pages consommatrices. Ne jamais donner simultanément les mêmes objets globaux à plusieurs écrivains.
