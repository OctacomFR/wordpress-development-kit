# Obtenir le rendu final Figma à l'identique

Cette procédure est obligatoire pour toute construction, refonte ou correction dont Figma définit le rendu. Elle couvre chaque page et objet partagé du périmètre, chaque frame fournie et chaque état spécifié. L'objectif est une reproduction à 100 %, avec zéro écart visuel non autorisé. Un écart minime reste un écart à corriger.

## Fixer la référence avant d'écrire

1. Lire toutes les annotations et franchir `FIGMA_ANNOTATIONS_REVIEWED` selon `figma-to-oxygen`.
2. Inventorier les frames, nodes, variantes, états et largeurs exactes à reproduire. Inclure le Header, le Footer et toutes les sections, jusqu'au bas de la page.
3. Récupérer et conserver une capture ou un export de chaque référence Figma. La capture est obligatoire, même si les propriétés des nodes sont accessibles. Elle complète leur relevé mesuré.
4. Associer chaque référence à sa page ou son objet Oxygen, son URL front et son propriétaire. Noter l'identifiant du node, la version ou date de lecture Figma et les dimensions de l'image.
5. Consigner les corrections explicites de l'utilisateur et les annotations qui modifient le rendu de la frame. Leur cible et leur effet doivent être déterminés avant l'implémentation.

Les effets hover peuvent être interprétés. Ils doivent rester cohérents avec la charte, accessibles au clavier et utilisables au tactile. Cette liberté ne permet aucune modification de la géométrie, de la typographie, des couleurs ou des médias de l'état au repos, ni des autres états spécifiés.

Les sources métier restent prioritaires pour le contenu. Si leur application change le rendu attendu, identifier précisément le conflit et son effet. Une décision explicite déjà fournie fait foi et se conserve dans le registre. Si elle ne fixe pas l'effet visuel requis, demander cette décision avant l'écriture dépendante. Une contrainte Oxygen, un manque de police ou d'asset, l'accessibilité, le SEO, un crédit obligatoire ou l'existant ne constituent pas une autorisation silencieuse de modifier Figma.

Pour les animations d'apparition obligatoires, reproduire exactement l'état final Figma après leur exécution. Tester le mouvement séparément. Si une exigence du kit contredit une spécification explicite, appliquer l'ordre des sources et documenter la résolution ou le blocage.

Une référence, un asset, une police, une annotation ou une capacité de capture requis inaccessible bloque le travail qui en dépend. Chercher dans les sources autorisées, puis demander précisément l'accès ou la décision manquante. Seuls les audits indépendants en lecture seule peuvent continuer.

## Capturer des états comparables

1. Ouvrir le front réel dans un navigateur après sauvegarde et rechargement. Utiliser les polices, textes et médias réels, sans substituer un contenu pour arranger la comparaison.
2. Régler le viewport à la largeur CSS exacte de la frame, avec zoom à 100 %. Consigner hauteur du viewport, rapport de pixels du périphérique, navigateur, URL, état et position de scroll. Capturer ou exporter les deux images à la même échelle, idéalement un pixel image par pixel CSS.
3. Attendre le chargement des polices, des images et des ressources. Faire défiler la page pour déclencher les apparitions, attendre leur état final visible, puis revenir à la position prévue. Fixer les carrousels et autres éléments variables à l'état Figma correspondant.
4. Capturer la page entière, puis des détails de chaque section à taille native. Vérifier aussi les éléments sticky dans leur contexte réel. Une capture complète n'exonère pas de regarder les détails à 100 %.
5. Conserver les images originales. Apparier les régions par leur origine et leur largeur sans étirer, redimensionner ni déplacer une image pour faire disparaître un écart. Une différence de hauteur ou de limite de section est un défaut à examiner, pas une raison de couper le bas de page.

Comparer chaque frame desktop, tablette et mobile fournie à sa largeur native. Contrôler aussi 1920 px et la matrice responsive de `wordpress-oxygen-qa`, avec des largeurs intermédiaires. Si Figma ne fournit pas de frame à une largeur, documenter un contrôle responsive à cette largeur, sans prétendre y avoir prouvé une identité à Figma. Une décision de disposition requise et non spécifiée suit la règle de blocage.

## Comparer et corriger jusqu'à zéro écart

Après chaque bloc majeur, puis sur la version finale gelée :

1. Afficher les captures Figma et front côte à côte, puis examiner leur superposition et leur différence. Inspecter la page entière et chaque section, à taille native.
2. Contrôler les limites des sections, positions, largeurs, hauteurs, alignements, marges, paddings, gaps, polices réellement chargées, graisses, tailles, interlignages, espacements de lettres, largeurs de texte et retours à la ligne. Comparer aussi couleurs, fonds, dégradés, bordures, rayons, ombres, images exactes, cadrages, masques, découpes, overlays, icônes et décorations.
3. Croiser chaque constat avec les propriétés Figma mesurées et la matrice d'annotations. Contrôler les autres occurrences et consommateurs d'un objet partagé.
4. Inscrire chaque différence dans le registre, même si elle paraît mineure. Attribuer sa correction au propriétaire de l'objet. Pendant l'audit, les autres agents restent en lecture seule.
5. Corriger à la couche responsable, sauvegarder, recharger le front et produire de nouvelles captures. Refaire les comparaisons concernées et contrôler les régressions sur les consommateurs touchés.
6. Répéter tant qu'un écart visuel non autorisé subsiste. Après la dernière correction, recapturer la page entière et chaque section affectée. La preuve finale doit correspondre à la dernière version sauvegardée.

Pour produire les supports de comparaison avec ImageMagick, utiliser le helper du kit depuis la racine du workspace :

```powershell
python .agents/skills/wordpress-oxygen-qa/scripts/compare_visuals.py --figma qa/figma/home-desktop.png --front qa/front/home-desktop.png --output-dir qa/comparisons/home-desktop-final
```

Les entrées sont des PNG de preuve, pas des médias de production. Le helper exige les mêmes dimensions et un dossier de sortie nouveau. Il produit `side-by-side.png`, `overlay.png`, `difference.png` et `comparison.json`, avec les empreintes des sources, les dimensions, la version d'ImageMagick et la mesure de différence. Si les dimensions divergent, relever et corriger la cause avant de générer la superposition ; conserver les captures originales et le constat.

Ouvrir réellement les images produites avec un outil de lecture d'images. La réussite du helper prouve la production des supports, jamais la fidélité. Aucun seuil de score, pourcentage de pixels, moyenne sur la page, flou ou masque ne permet de valider un écart. La différence brute peut révéler la rasterisation des fontes ou l'anticrénelage ; vérifier alors les propriétés, les contours et les métriques à taille native. Ce signal seul ne prouve ni un défaut de design ni sa conformité. Toute différence inexpliquée reste ouverte et bloque la validation.

## Conserver les preuves

Créer une ligne de couverture par page ou objet, frame et état à reproduire :

```text
PAGE / OBJET / ID / URL FRONT :
NODE / FRAME FIGMA / VERSION OU DATE :
ÉTAT / LARGEUR CSS / HAUTEUR VIEWPORT / DPR / ZOOM / SCROLL :
VERSION OXYGEN SAUVEGARDÉE / DATE DERNIÈRE MUTATION :
CAPTURE FIGMA / CAPTURE FRONT FINALE / DATE CAPTURE :
SECTIONS COUVERTES / PREUVES DE DÉTAIL :
CÔTE À CÔTE / SUPERPOSITION / DIFFÉRENCE / COMPARISON.JSON :
ANNOTATIONS ET DÉCISIONS EXPLICITES APPLICABLES :
ÉCARTS OUVERTS :
STATUT : à comparer | à corriger | bloqué | vérifié
AUDITEUR / DATE DE DERNIÈRE COMPARAISON :
```

Conserver aussi un registre des écarts. Pour chacun, noter la région, le node, l'attendu mesuré, l'observé, le propriétaire, la correction ou décision explicite et la preuve après correction. Une décision explicite doit désigner exactement la divergence autorisée et sa source. L'agent ne peut pas se l'accorder lui-même. Un écart consigné reste ouvert jusqu'à correction vérifiée ou décision explicite applicable.

## Franchir la barrière de livraison

`FIGMA_VISUAL_MATCH_VERIFIED` est une barrière de workflow fondée sur des preuves consultées. Elle est franchie pour une cible seulement lorsque :

- toutes ses frames et tous ses états spécifiés sont couverts ;
- les captures Figma, les captures front finales, les détails et les comparaisons sont conservés et ont été examinés ;
- le registre contient zéro écart visuel non autorisé et zéro différence inexpliquée ;
- les annotations et leurs effets indirects sont vérifiés ;
- les preuves correspondent à la dernière version de Figma retenue et à la dernière version front sauvegardée ;
- les contrôles builder, responsive, animations, accessibilité et sans JavaScript applicables sont passés.

Une mutation de page invalide ses comparaisons précédentes. Une mutation d'objet partagé invalide celles de ses consommateurs concernés. Une nouvelle référence ou correction Figma invalide les comparaisons qu'elle affecte. Refaire les captures et contrôles avant de rétablir la barrière.

Le coordinateur examine lui-même les preuves finales, même si un sous-agent a comparé les captures. Une simple déclaration d'agent, le code, un relevé de propriétés sans captures, un score ou un marqueur écrit ne suffisent pas. Le kit fournit une procédure et des supports de comparaison, pas un exécuteur capable de certifier automatiquement l'identité visuelle.

Sans navigateur, référence, capture, comparaison complète ou résolution des écarts, remettre un rapport de blocage et demander l'information ou la capacité précise manquante. La page et le site ne peuvent pas être déclarés terminés, conformes à 100 % ou prêts à livrer. Joindre au rapport final les preuves et le registre clos lorsque la barrière est franchie.
