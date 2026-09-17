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

Avant d'implémenter, établir mentalement ou dans une note temporaire :

```text
Typography
- polices
- poids réellement utilisés
- tailles / line-height

Colors
- fonds
- textes
- accents
- gradients

Geometry
- max-width
- rayons
- bordures
- ombres

Spacing
- padding sections
- gaps
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

S'il n'y a pas de variables Figma, ne pas considérer chaque valeur isolée comme un token. Regrouper seulement les valeurs réellement répétées.
