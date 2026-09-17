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

## Rôle de l'accueil

L'accueil doit :

- établir le langage visuel, les largeurs, espacements et rythmes ;
- intégrer et valider le Header sticky et le Footer ;
- définir uniquement les vrais Components et variantes réutilisables ;
- présenter les parcours et CTA principaux ;
- afficher les aperçus dynamiques utiles ;
- fonctionner sans JavaScript ;
- rester entièrement éditable dans Oxygen.

Il ne doit pas créer à l'avance toutes les pages internes, archives, singles ou 404 hors périmètre.

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
8. Responsive et rendu sans JavaScript.
9. SEO, builder et QA visuelle/fonctionnelle.

Après chaque gros bloc, sauvegarder, ouvrir le front et vérifier avant de poursuivre.

## Sous-agents

Pendant que le propriétaire unique écrit, utiliser intensivement des spécialistes en lecture seule : vérification de la matrice d'annotations et de ses effets indirects, cartographie textes/médias/sections, comparaison Figma, contrôle des assets, spécification des loops, accessibilité/no-JS, responsive, SEO et régression des objets partagés. Toute évolution globale passe par le coordinateur ou le propriétaire du socle.

## Critère de stabilité

La barrière `HOME_STABLE` est franchie lorsque toutes les annotations du périmètre et leurs effets indirects sont appliqués et vérifiés, la conformité Figma et les contenus sont contrôlés, les patterns locaux et globaux sont séparés, Header/Footer fonctionnent, le responsive et le sans-JS sont contrôlés, le builder reste éditable et les fondations peuvent être consommées par des pages internes sans refonte immédiate.
