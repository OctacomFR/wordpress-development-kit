---
name: figma-to-oxygen
description: "Lire une maquette Figma et traduire ses frames, annotations, assets, variables et interactions en structure Oxygen 6 fidèle, durable et éditable, sans copier le code généré brut."
---

# Traduire Figma vers Oxygen

La maquette définit l'intention visuelle. Oxygen, HTML et CSS définissent l'implémentation de production.

## Références à lire

- Lire obligatoirement [references/annotation-workflow.md](references/annotation-workflow.md) avant toute implémentation fondée sur Figma.
- Lire [references/figma-reading-and-inventory.md](references/figma-reading-and-inventory.md) pour l'acquisition du contexte et l'inventaire.
- Lire [references/translation-and-assets.md](references/translation-and-assets.md) avant toute implémentation issue de Figma.
- Lire [../../references/media-tooling.md](../../references/media-tooling.md) avant de transformer, convertir, redimensionner, recadrer, compresser ou extraire un asset image ou vidéo.
- Lire [references/anti-slop.md](references/anti-slop.md) avant une décision esthétique non explicitement visible dans la maquette.

## Workflow

1. Ouvrir le node exact et récupérer contexte, capture, variables, composants, annotations, interactions et variantes desktop/mobile accessibles.
2. Recenser et lire intégralement toutes les annotations du périmètre, identifier leur cible exacte et construire la matrice obligatoire.
3. Analyser pour chaque annotation ses effets directs, ses effets indirects, ses occurrences liées, ses breakpoints, ses états et ses contraintes.
4. Appliquer l'ordre de priorité Figma. Si une annotation inaccessible, ambiguë, techniquement impossible ou contradictoire laisse une décision requise non résolue, demander une instruction explicite à l'utilisateur. Ne commencer aucune implémentation avant `FIGMA_ANNOTATIONS_REVIEWED`.
5. Construire l'inventaire typographie, couleurs, géométrie, espacements, composants, assets et états.
6. Distinguer les valeurs répétées des valeurs ponctuelles avant de créer des tokens.
7. Traduire les compositions en Sections/Containers, flexbox ou Grid, largeur fluide et structure sémantique.
8. Réserver l'absolu aux superpositions et décorations réellement présentes.
9. Préparer les assets exacts avant import : utiliser ImageMagick pour transformer et convertir tous les rasters maîtrisés en WebP, FFmpeg pour transformer les vidéos et FFprobe pour les inspecter, puis conserver/exporter en SVG les logos, icônes, pictogrammes, formes et illustrations vectorielles. Importer ensuite les fichiers optimisés dans un emplacement durable ; aucune URL temporaire Figma ne reste en production.
10. Comparer régulièrement le front à la capture de référence et vérifier la matrice d'annotations à chaque bloc concerné.

Ne pas coller du React, Tailwind ou un arbre rempli de coordonnées fixes dans Oxygen. Ne pas recréer approximativement logos, icônes, SVG ou favicon disponibles.

## Sous-agents

Pour une maquette riche, déléguer en parallèle et en lecture seule : inventaire exhaustif des annotations, vérification des effets indirects, inventaire des frames et tokens, manifeste des assets, matrice desktop/mobile et comparaison visuelle. Un seul coordinateur consolide la matrice ; un seul propriétaire transforme ensuite ces constats en objets Oxygen partagés.

## Garde-fous

- Dans l'analyse Figma : instruction explicite de la tâche, annotations, structure/propriétés réelles, rendu visuel, puis interprétation personnelle.
- Les documents métier priment sur Figma pour le contenu lorsqu'ils sont la source validée.
- Une annotation fait partie des spécifications. Ne jamais l'écarter parce que le rendu visuel paraît différent.
- Ne pas ajouter d'effets, sections, CTA ou textes pour « améliorer » la charte. Les animations d'apparition restent obligatoires, même si la charte ou la maquette n'en prévoit aucune. Reprendre celles de Figma ou définir un système sobre si la maquette ne les précise pas.
- Signaler un contraste manifestement insuffisant et proposer une correction minimale au lieu de modifier silencieusement la charte.
