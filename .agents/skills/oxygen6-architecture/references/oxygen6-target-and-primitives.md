# Cible Oxygen 6 et primitives

Référence extraite sans réécriture du snapshot `docs/AGENTS.pre-skills-snapshot.md`.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 114-181 -->

## 3. Cible technique : Oxygen 6.x

Ce guide cible **le nouvel Oxygen 6.x**, et **jamais Oxygen Classic**, sauf consigne explicite contraire du projet.

Oxygen 6 est une réécriture complète du builder. Ne pas transposer automatiquement les concepts ou recettes d'Oxygen Classic. En particulier :

- `Reusable Parts` Classic -> utiliser les **Components** Oxygen 6 ;
- `Inner Content` Classic -> utiliser **Template Content Area** ;
- `Repeater / Easy Posts` Classic -> utiliser en priorité **Post Loop Builder** + **Component** pour les listes de contenus WordPress ;
- les anciens patterns centrés sur styles par ID -> privilégier le système **Classes / Selectors / Variables** d'Oxygen 6 ;
- header/footer génériques dans un ancien Main Template -> utiliser en priorité les objets **Headers** et **Footers** natifs d'Oxygen 6 avec Location, Conditions et Priority ;
- les interactions custom JS -> utiliser d'abord les **States**, **Nested Selectors** et l'**Interactions Engine** natif lorsque cela couvre le besoin.

### 3.1. Toujours détecter la version exacte

Avant de construire :

1. lire la version exacte d'Oxygen installée ;
2. inspecter les abilities/outils MCP réellement exposés ;
3. utiliser uniquement les fonctionnalités disponibles sur cette installation ;
4. ne jamais supposer qu'une fonction apparue en 6.2 Beta est disponible sur une installation 6.0/6.1.

Au moment de la rédaction de ce guide, Oxygen 6.2 ajoute un support MCP/agent beaucoup plus poussé, mais certaines versions 6.2 peuvent être des bêtas. Le guide reste donc **version-gated** : si l'ability n'existe pas, ne pas l'inventer.

### 3.2. Design system Oxygen 6

Le design system doit être construit avec les primitives natives :

- **Variables** organisées en collections : couleurs, spacing, typographie, dimensions/radius lorsque pertinent ;
- **Classes** pour les styles réutilisables ;
- **Selectors** et Nested Selectors pour les sélecteurs avancés ;
- **States** (`&:hover`, `&:focus-visible`, `&:active`, etc.) pour les états simples ;
- **Components** pour les patterns réutilisables ;
- **Component Properties** pour rendre certaines valeurs modifiables par instance sans casser le composant ;
- **Component child visibility** lorsque certaines variantes doivent afficher/masquer un sous-élément ;
- **Dynamic Data** pour les données WordPress ;
- **Post Loop Builder / Term Loop Builder / Repeater Field** selon le type de données répétées ;
- **Template Content Area** dans les templates qui doivent afficher le contenu propre à chaque page/post.

Avant de créer un comportement ou un bloc à la main, inventorier dans cet ordre :

1. élément Oxygen natif disponible dans la version installée ;
2. Component existant du projet ;
3. pattern réalisable avec Containers, liens, Images, Dynamic Data, States, Nested Selectors ou Interactions ;
4. code custom ciblé en dernier recours.

Pour une implémentation manuelle interactive, suivre les patterns WAI-ARIA applicables sans remplacer la sémantique HTML native par des rôles ARIA inutiles. Tester le clavier, le focus, les noms accessibles et les états annoncés.

### 3.3. MCP Oxygen / Agent Connector

Si Oxygen expose ses abilities via MCP, les utiliser en priorité au lieu de bricoler les données internes du builder.

Selon la version réellement installée, l'agent peut notamment être capable de lire/créer/modifier :

- pages ;
- templates ;
- headers ;
- footers ;
- Components et propriétés de Components ;
- classes/selectors ;
- variables CSS ;
- dynamic data ;
- loops et leurs queries ;
- conditions ;
- interactions/animations ;
- réglages Oxygen.

Quand des outils de preview Oxygen sont exposés (`preview-post`, `preview-element` ou équivalent), les utiliser pendant la QA. Ne jamais les appeler s'ils ne sont pas présents dans les abilities du serveur.
