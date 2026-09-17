---
name: figma-to-oxygen
description: "Lire une maquette Figma et traduire ses frames, annotations, assets, variables et interactions en structure Oxygen 6 fidèle, durable et éditable, sans copier le code généré brut."
---

# Traduire Figma vers Oxygen

La maquette définit l'intention visuelle. Oxygen, HTML et CSS définissent l'implémentation de production.

## Références à lire

- Lire [references/figma-reading-and-inventory.md](references/figma-reading-and-inventory.md) pour l'acquisition du contexte et l'inventaire.
- Lire [references/translation-and-assets.md](references/translation-and-assets.md) avant toute implémentation issue de Figma.
- Lire [references/anti-slop.md](references/anti-slop.md) avant une décision esthétique non explicitement visible dans la maquette.

## Workflow

1. Ouvrir le node exact et récupérer contexte, capture, variables, composants, annotations, interactions et variantes desktop/mobile accessibles.
2. Ne jamais prétendre avoir lu un commentaire que le connecteur n'expose pas.
3. Construire l'inventaire typographie, couleurs, géométrie, espacements, composants, assets et états.
4. Distinguer les valeurs répétées des valeurs ponctuelles avant de créer des tokens.
5. Traduire les compositions en Sections/Containers, flexbox ou Grid, largeur fluide et structure sémantique.
6. Réserver l'absolu aux superpositions et décorations réellement présentes.
7. Importer les assets exacts dans un emplacement durable ; aucune URL temporaire Figma ne reste en production.
8. Comparer régulièrement le front à la capture de référence, à la largeur correspondante.

Ne pas coller du React, Tailwind ou un arbre rempli de coordonnées fixes dans Oxygen. Ne pas recréer approximativement logos, icônes, SVG ou favicon disponibles.

## Sous-agents

Pour une maquette riche, déléguer en parallèle et en lecture seule : inventaire des frames et annotations, inventaire des tokens, manifeste des assets, matrice desktop/mobile, et comparaison visuelle. Un seul propriétaire transforme ensuite ces constats en objets Oxygen partagés.

## Garde-fous

- La dernière correction visuelle explicite de l'utilisateur prime, puis Figma.
- Les documents métier priment sur Figma pour le contenu lorsqu'ils sont la source validée.
- Ne pas ajouter d'effets, sections, CTA, textes ou animations pour « améliorer » la charte.
- Signaler un contraste manifestement insuffisant et proposer une correction minimale au lieu de modifier silencieusement la charte.
