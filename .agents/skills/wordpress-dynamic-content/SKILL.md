---
name: wordpress-dynamic-content
description: "Construire des actualités, listes, loops, archives et templates WordPress/Oxygen avec les données réelles, les bonnes requêtes et des états limites explicites."
---

# Contenus WordPress dynamiques

Les données WordPress restent dans WordPress. Ne jamais remplacer des articles, dates, images, permaliens, catégories ou contenus récurrents par des cartes copiées à la main.

## Référence à lire

Lire [references/news-and-posts.md](references/news-and-posts.md) pour les règles détaillées de Post Loop Builder, Component de carte, query, premier item, cas limites et template article.

## Workflow

1. Résoudre les post types, catégories, slugs, IDs et contenus réels.
2. Créer ou réutiliser un Component unique pour chaque motif de résultat.
3. Utiliser Dynamic Data et Post Loop Builder/Query Builder.
4. Réserver Array Query puis PHP/WP_Query aux besoins non exprimables nativement.
5. Tester zéro, un et plusieurs résultats, contenus longs et image absente.
6. Vérifier ordre, statut, nombre demandé, sticky posts, permaliens et template single dans le périmètre.

Le nombre d'éléments vient du brief. « Deux dernières actualités » n'est la valeur par défaut que si le projet le demande explicitement.

Ne pas créer archive, single ou 404 hors périmètre pendant une mission limitée à l'accueil. Lorsqu'un système d'articles est dans le périmètre, les permaliens de l'accueil doivent être compatibles avec le template single prévu.

## Sous-agents

Déléguer en lecture seule l'inventaire des catégories/posts, la spécification de query, la vérification des états limites et la QA des permaliens. Un propriétaire exclusif modifie le loop, son Component et ses Templates.
