# Lecture Figma et inventaire de design

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis harmonisée avec la barrière active des annotations Figma.

> Procédure active complète : [annotation-workflow.md](annotation-workflow.md). Toutes les annotations du périmètre doivent être lues avant implémentation. Une annotation inaccessible bloque l'écriture concernée. Une ambiguïté ou contradiction exige une question à l'utilisateur seulement si elle reste non résolue après application de l'ordre de priorité.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 245-314 -->

### Phase B — Lecture Figma

Pour le node Figma demandé :

1. appeler le contexte de design Figma sur le node exact ;
2. récupérer une capture de référence si nécessaire pour comparer visuellement ;
3. récupérer les variables Figma si elles existent ;
4. exploiter les composants, styles, variables, annotations et informations d'interaction retournés ;
5. identifier les assets exportables exacts ;
6. noter les états interactifs : hover, focus apparent, actif, ouvert/fermé, slider, etc. ;
7. noter les relations entre desktop/mobile lorsque plusieurs frames sont disponibles.

#### Commentaires et annotations Figma

Les annotations du périmètre sont contraignantes. Les commentaires Figma sont inclus lorsqu'ils sont exposés comme annotations ou lorsqu'une instruction explicite les rend requis. Toutes les annotations requises doivent être accessibles, lues intégralement et prises en compte avant implémentation.

Si le MCP utilisé n'expose pas les annotations requises ou si leur exhaustivité ne peut pas être vérifiée :

- ne jamais dire qu'ils ont été lus ;
- utiliser les annotations retournées uniquement pour établir l'état de l'inventaire, sans commencer l'implémentation ;
- signaler précisément ce qui ne peut pas être vérifié ;
- demander un accès, un export, des captures ou une copie ;
- maintenir l'implémentation Figma dépendante bloquée jusqu'à lecture complète.

### Phase C — Inventaire de design

Avant d'implémenter, consigner un relevé vérifiable de la frame desktop entière, section par section. Lire les dimensions et propriétés des nodes Figma, leurs contraintes et leur Auto Layout lorsqu'ils existent. Pour chaque bloc visible, noter sa position et sa taille dans la frame, les alignements, les marges, paddings et gaps, les dimensions et retours à la ligne du texte, les images et leur cadrage, les découpes, masques et superpositions. Inclure le Header et le Footer visibles. Une capture seule ne remplace pas les propriétés mesurables ; signaler toute mesure requise inaccessible au lieu de l'estimer.

Noter la largeur exacte de la frame et la source de chaque mesure. La comparaison se fait à cette largeur et à 1920 px. Si la frame n'est pas à 1920 px et qu'aucune référence Figma n'existe à cette largeur, distinguer le contrôle du rendu à 1920 px de la comparaison fidèle à la frame native. Ne pas attribuer à Figma une géométrie à 1920 px qu'il ne spécifie pas.

Compléter ce relevé avec l'inventaire suivant :

```text
Typography
- polices
- poids réellement utilisés
- tailles / line-height / letter-spacing / largeur des blocs et retours à la ligne

Colors
- fonds
- textes
- accents
- gradients

Geometry
- largeur et hauteur des frames, sections, conteneurs et éléments
- positions et alignements dans la frame
- max-width et contraintes de redimensionnement
- rayons
- bordures
- ombres

Spacing
- marges et paddings des sections et éléments
- gaps horizontaux et verticaux
- rythme vertical

Components
- boutons
- cartes
- header
- footer
- hero
- menu
- card actualité
- rail réseaux sociaux
- séparateurs / vagues / décorations

Interactions
- hover
- focus
- menu mobile
- slider/carrousel
- accordéons
```

Mesurer le résultat, puis reconstruire les rapports de placement avec les contrôles Oxygen adaptés. Les coordonnées Figma servent à vérifier le rendu desktop ; elles ne deviennent pas automatiquement des `left`, `top`, largeurs ou hauteurs fixes dans le CSS.

S'il n'y a pas de variables Figma, ne pas considérer chaque valeur isolée comme un token. Regrouper seulement les valeurs réellement répétées.
