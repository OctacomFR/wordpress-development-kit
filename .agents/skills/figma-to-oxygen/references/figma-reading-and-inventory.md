# Lecture Figma et inventaire de design

Référence extraite sans réécriture du snapshot `docs/AGENTS.pre-skills-snapshot.md`.

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

Les commentaires/annotations sont contraignants lorsqu'ils sont accessibles par le MCP.

Si l'utilisateur demande explicitement de prendre en compte des **commentaires Figma** mais que le MCP utilisé ne les expose pas :

- ne jamais dire qu'ils ont été lus ;
- utiliser toutes les annotations retournées par le contexte de design ;
- signaler précisément que les commentaires non exposés ne peuvent pas être vérifiés ;
- demander un export ou une copie uniquement si ces commentaires sont indispensables pour continuer correctement.

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
