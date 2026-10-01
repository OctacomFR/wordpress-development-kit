---
name: oxygen6-homepage
description: "Construire ou refondre une page d'accueil Oxygen 6 à partir de Figma, en calibrant la direction visuelle, les fondations partagées, les parcours et les contenus dynamiques du site."
---

# Page d'accueil Oxygen 6

L'accueil est la page de calibration du site. Il révèle les patterns réutilisables et possède un rayon d'impact supérieur à celui d'une page interne. Un seul agent possède son arbre Oxygen.

## Prérequis

1. Terminer `octacom-project-start` et `figma-to-oxygen`, avec la barrière `FIGMA_ANNOTATIONS_REVIEWED` franchie pour tout le périmètre de l'accueil.
2. Vérifier la sauvegarde et la bonne cible WordPress.
3. Charger `oxygen6-architecture` pour les fondations globales.
4. Distinguer ce qui est global, réutilisable et propre à l'accueil.
5. Confirmer contenus, médias, CTA, destinations et sources dynamiques.
6. Lire la [procédure de fidélité visuelle](../../references/figma-visual-fidelity.md) et préparer les références de toute la page, Header et Footer compris.

## Rôle de l'accueil

L'accueil doit :

- établir le langage visuel, les largeurs, espacements et rythmes ;
- intégrer et valider le Header sticky et le Footer ;
- définir uniquement les vrais Components et variantes réutilisables ;
- présenter les parcours et CTA principaux ;
- afficher les aperçus dynamiques utiles ;
- fonctionner sans JavaScript ;
- rester entièrement éditable dans Oxygen.

Il ne doit pas créer à l'avance les autres pages internes ou archives hors périmètre. Il doit toutefois créer ou vérifier les Templates Oxygen 6 obligatoires Single Article et 404 avant livraison du site.

## Global ou local

Promouvoir un motif vers le socle seulement s'il apparaît à plusieurs endroits, doit être maintenu globalement, sert de template à un loop ou possède des variantes propres exprimables avec des Component Properties.

Conserver dans la home les compositions uniques, décorations propres au hero et sections sans consommateur connu. Ne pas sur-abstraire.

## Ordre de construction

1. Fondations globales validées.
2. Header et compensation du sticky.
3. Hero.
4. Sections propres à l'accueil.
5. Components dont la répétition est confirmée.
6. Contenus dynamiques.
7. Interactions et états.
8. Comparaison obligatoire des captures Figma et front de la page entière puis de chaque section desktop à la largeur exacte de la frame, avec côte à côte, superposition et différence. Corriger et recapturer jusqu'à zéro écart visuel non autorisé. Contrôler aussi 1920 px et comparer directement si une frame Figma existe à cette largeur.
9. Après validation du desktop, responsive et rendu sans JavaScript. Reproduire et comparer chaque frame mobile et tablette fournie à sa largeur exacte.
10. SEO, builder et QA visuelle/fonctionnelle.

Après chaque gros bloc, sauvegarder, ouvrir le front, capturer et comparer au Figma avant de poursuivre. Après toute correction finale, refaire les captures et comparaisons affectées.

## Sous-agents

Pendant que le propriétaire unique écrit, utiliser intensivement des spécialistes en lecture seule : vérification de la matrice d'annotations et de ses effets indirects, cartographie textes/médias/sections, comparaison Figma, contrôle des assets, spécification des loops, accessibilité/no-JS, responsive, SEO et régression des objets partagés. Toute évolution globale passe par le coordinateur ou le propriétaire du socle.

## Critère de stabilité

La barrière `HOME_STABLE` exige `FIGMA_VISUAL_MATCH_VERIFIED` pour l'accueil et ses objets partagés référencés. Toutes les annotations et leurs effets indirects sont vérifiés, le relevé couvre la frame entière, les captures finales de la page et de chaque section sont comparées à toutes les frames fournies, et le registre contient zéro écart visuel non autorisé. Le rendu à 1920 px, les contenus, Header/Footer, le responsive, le sans-JS et le builder sont contrôlés. Les patterns locaux et globaux sont séparés et les fondations peuvent être consommées sans refonte immédiate. Tout écart restant, même minime, ou toute preuve manquante bloque cette barrière et la livraison.
