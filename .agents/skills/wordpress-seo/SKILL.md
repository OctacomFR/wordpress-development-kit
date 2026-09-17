---
name: wordpress-seo
description: "Vérifier ou configurer la structure HTML, les titres, métadonnées, canonical, Yoast, indexabilité, liens crawlables et Schema d'un site WordPress/Oxygen."
---

# SEO WordPress

Le SEO part du contenu métier validé et du HTML réel. Ne jamais inventer une promesse, une localisation, un service, un avis ou une donnée structurée.

## Référence à lire

Lire [references/technical-seo.md](references/technical-seo.md) avant toute modification SEO ou revue de balisage.

## Workflow

1. Inspecter le DOM et l'état Yoast existant avant d'écrire.
2. Vérifier un H1 principal, une hiérarchie Hn cohérente, les landmarks et les vrais liens crawlables.
3. Vérifier title, meta description, canonical, robots, OpenGraph, image sociale et indexabilité.
4. Utiliser le connecteur Yoast disponible plutôt que des métas privées ou un second balisage dans le `<head>`.
5. Préserver et compléter le graphe Schema Yoast ; ne créer que des données vérifiées.
6. Contrôler la sortie réelle pour l'URL finale.

Ne jamais fabriquer `review` ou `aggregateRating`. Ne pas choisir un niveau de titre pour sa taille visuelle. Le texte SEO important doit exister dans le DOM, pas seulement dans CSS ou une image.

## Sous-agents

Déléguer en lecture seule des audits séparés : structure DOM/Hn, métadonnées/canonical, liens internes, Schema/Yoast et images/alt. Le propriétaire SEO consolide les conflits et applique les écritures de métadonnées de façon sérialisée.
