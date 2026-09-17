---
name: oxygen6-frontend-quality
description: "Concevoir ou corriger le responsive, les médias, animations, états, accessibilité, performance, widgets et rendu sans JavaScript d'une page Oxygen 6."
---

# Qualité front Oxygen 6

Appliquer ces règles pendant la construction, pas seulement à la fin.

## Références ciblées

- Layout, breakpoints, motion et sticky : [references/responsive-motion-sticky.md](references/responsive-motion-sticky.md).
- Rail social, coordonnées, boutons et iframes : [references/social-links-and-iframes.md](references/social-links-and-iframes.md).
- Images, performance, galerie/carrousel et accessibilité : [references/images-performance-accessibility.md](references/images-performance-accessibility.md).

Lire uniquement les références utiles à la tâche ; pour une revue front complète, lire les trois.

## Invariants

- Tester les breakpoints configurés, les largeurs de référence historiques et des largeurs intermédiaires.
- Conserver un ordre DOM logique et éviter les hauteurs fixes sur le texte.
- Toute information disponible au hover l'est aussi au clavier et au tactile.
- Le contenu, la navigation et les actions essentielles sont clairs et utilisables sans JavaScript.
- Une animation part de l'état final visible ; elle ne masque l'élément qu'après initialisation réussie. Respecter `prefers-reduced-motion`.
- L'attribut `alt` est obligatoire sur chaque image : descriptif si informative, vide si décorative, nom pertinent pour un logo informatif.
- Préserver ratios, dimensions/espaces réservés, `srcset`/`sizes`, LCP non lazy et lazy-loading pertinent sous la ligne de flottaison.
- Utiliser une galerie ou un vrai carrousel selon le besoin, avec l'élément Oxygen existant avant du custom.
- Les liens externes HTTP utilisent `target="_blank"` et `rel="noopener noreferrer"`; les liens internes restent dans le même onglet ; `tel:` et `mailto:` restent directs.

## Progressive enhancement

Prévoir un état statique utile pour menu mobile, accordéon, carrousel, coordonnées, cartes et médias. Un `<noscript>` peut expliquer la perte d'une fonction secondaire, jamais remplacer du contenu caché.

## Sous-agents

Sur une page non triviale, déléguer séparément et en lecture seule les audits responsive, accessibilité/clavier, no-JS/motion, images/performance et liens/widgets. Le propriétaire de la page applique les corrections ; les auditeurs ne modifient pas simultanément l'arbre Oxygen.

Pour générer des alts depuis les médias, choisir un modèle compatible vision. Un modèle compact et rapide suffit pour une description factuelle simple si l'image, son rôle informatif ou décoratif et son contexte éditorial sont accessibles. Si l'image ou ce contexte manque, bloquer la génération et demander l'information à l'utilisateur. Ne jamais déduire une identité, un lieu, une certification ou un fait invisible.
