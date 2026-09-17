# AGENTS.md — Développement WordPress + Oxygen 6.x depuis Figma avec Codex

Guide générique pour développer des sites WordPress avec Codex à partir d'une maquette Figma, en utilisant un MCP WordPress, le MCP Figma et, lorsqu'il est disponible, le connecteur Yoast SEO.

Objectif : produire des pages fidèles à la charte, réellement éditables dans Oxygen 6.x, réutilisables, responsive, performantes, accessibles et propres pour le SEO — sans inventer de contenu ni transformer la maquette Figma en soupe de `position:absolute`.

---

## 0. Paramètres projet

Ne jamais hard-coder un client ou un domaine dans ce fichier générique.

Les informations suivantes doivent être fournies dans le prompt projet ou détectées avec les MCP :

```text
SITE_URL=<url du site>
FINAL_DOMAIN=<domaine public final, obligatoire avant Complianz et l'envoi d'emails>
WORDPRESS_MCP=<serveur MCP WordPress du projet>
FIGMA_URL=<url Figma node-specific>
COMPANY_ID=<identifiant entreprise dans la base Octacom>
PROJECT_ID=<identifiant projet dans la base Octacom>
BUILDER=Oxygen 6.x
SEO_CONNECTOR=Yoast SEO si disponible
LANG=fr-FR sauf consigne contraire
```

Règles :

- Toujours utiliser le MCP WordPress correspondant au domaine du projet courant.
- Ne jamais écrire sur un autre WordPress simplement parce qu'un autre connecteur est disponible.
- Toujours résoudre les IDs, slugs, catégories, templates et médias depuis le site avant d'écrire.
- Ne jamais inventer le nom d'un outil MCP ou une capacité que le serveur n'expose pas : inspecter les outils disponibles d'abord.
- Demander ou retrouver dès le début `COMPANY_ID` et `PROJECT_ID`. Utiliser la base Octacom en lecture seule pour consulter le dossier ; ne jamais modifier le projet ou l'entreprise dans l'ERP sans demande explicite.
- Construire les URLs ERP uniquement avec les identifiants confirmés :

```text
https://base.octacom.fr/entreprises/<COMPANY_ID>
https://base.octacom.fr/entreprises/<COMPANY_ID>/projet/<PROJECT_ID>
```

- Demander le domaine public final avant de configurer Complianz, WP Mail SMTP, les URLs absolues, les cookies, les expéditeurs ou les redirections. Ne pas déduire ce domaine de l'URL de préproduction.
- Ne jamais inscrire de mot de passe, clé CAPTCHA, clé SMTP ou licence dans ce fichier, un compte rendu ou un journal de travail.

Documentation interne de référence : [Développement WordPress Octacom](https://app.notion.com/p/octacom/Dev-Wordpress-f6510f445ce44dad95d5c81e5c193540). La consulter lorsqu'elle est accessible pour les procédures Octacom, sans lui faire remplacer les sources métier propres au projet.

---

## 1. Ordre de priorité

### 1.1. Priorité générale

En cas de conflit :

1. Dernière instruction explicite de l'utilisateur.
2. Documents métier et contenus validés du projet pour les textes, horaires, prix, coordonnées et données légales.
3. Données vérifiées dans WordPress ou dans l'ERP Octacom consulté en lecture seule.
4. Figma pour le design et la disposition ; pour le contenu uniquement si le projet le désigne comme source éditoriale.
5. Le présent `AGENTS.md`.
6. Documentation officielle de l'outil concerné.

Si deux sources de même niveau ou deux sources métier se contredisent, signaler le conflit et demander laquelle fait foi avant de publier. Ne pas choisir silencieusement.

### 1.2. Priorité DESIGN

Pour toute décision visuelle :

1. Dernière correction visuelle explicite de l'utilisateur.
2. **Charte / maquette Figma du projet, y compris annotations et commentaires accessibles.**
3. Skill `frontend-design`.
4. Composants et patterns existants du site uniquement s'ils ne contredisent pas la nouvelle charte.
5. Règles génériques de ce document.

La charte Figma est donc la vérité visuelle. Le site existant est une référence technique, pas une excuse pour conserver un ancien design.

### 1.3. Skills obligatoires

Quand les skills sont disponibles dans l'environnement Codex :

- invoquer `caveman` ;
- invoquer `unslop` ;
- invoquer `frontend-design` ;
- les utiliser sur chaque tour qui implique conception, code ou correction visuelle.

Ne jamais prétendre avoir utilisé un skill indisponible. S'il n'est pas exposé par l'environnement, le signaler une fois puis continuer avec les règles de ce guide.

Les instructions propres aux skills priment sur ce document pour leur domaine, sauf pour le design où la charte Figma reste prioritaire conformément à la section précédente.

---

## 2. Principes non négociables

1. **Lire avant d'écrire.** Auditer le site, la maquette et les composants existants avant toute modification.
2. **Ne rien inventer.** Pas de téléphone, email, horaire, prix, adresse, certification, témoignage, URL, image, texte métier ou donnée SEO factuelle inventée.
3. **Figma décrit le design, pas l'implémentation.** Le React/Tailwind éventuellement retourné par Figma MCP est une référence de structure et de style, jamais du code à coller tel quel dans WordPress/Oxygen.
4. **Oxygen 6.x doit rester éditable.** Une page qui ressemble à Figma sur le front mais se casse dans le builder est considérée comme ratée.
5. **Réutiliser avant de dupliquer.** Components, Classes, Selectors, Variables, Templates, Headers, Footers, menus et composants de boucle doivent être factorisés.
6. **Pas de contenu statique pour des données WordPress dynamiques.** Articles, titres, dates, images à la une, permaliens, catégories et contenus récurrents doivent venir de WordPress.
7. **Pas de lien factice en production.** Aucun bouton `#`, `javascript:void(0)` ou URL dev si une vraie destination existe ou doit être résolue.
8. **Navigation = lien HTML réel.** Un élément qui navigue doit produire un `<a href="...">`; un `<button>` est réservé à une action applicative.
9. **Tester réellement.** Ne jamais écrire « pixel perfect », « responsive » ou « SEO OK » sans avoir fait les contrôles correspondants.
10. **Pas d'installation inutile.** Priorité à WordPress, Oxygen 6.x et aux plugins déjà présents. Pas de dépendance ou plugin supplémentaire sans besoin réel.
11. **Pas de JavaScript pour résoudre un problème que CSS/HTML/Oxygen savent déjà résoudre proprement.**
12. **Pas de CSS ou JS global destructif.** Toujours scoper les sélecteurs aux composants concernés.
13. **Ne pas modifier hors périmètre.** Une demande de home ne donne pas carte blanche pour refaire toutes les pages.
14. **Sauvegarder ou lire l'état existant avant une écriture importante.** En cas d'échec MCP, ne pas relancer aveuglément une mutation destructive.
15. **Une correction locale reste locale.** Une page ne doit pas changer les médias, carrousels, vidéos ou espacements d'autres pages par effet de bord.
16. **Préserver le contenu validé.** Ne pas reformuler les textes métier, avis, horaires, tarifs ou mentions légales sans demande explicite.
17. **Oxygen natif d'abord.** Chercher un élément, un Component ou une capacité Oxygen compatible avant tout code custom. Construire manuellement seulement en dernier recours, avec HTML sémantique, clavier, focus et WAI-ARIA lorsque nécessaire.
18. **Un seul état d'édition fait foi.** Après une modification externe ou MCP, recharger l'éditeur Oxygen avant toute nouvelle sauvegarde pour éviter qu'un onglet ancien réinjecte une version obsolète.
19. **Contenu visible sans JavaScript.** Le HTML et le CSS initiaux doivent afficher clairement tout le contenu éditorial, la navigation et les actions essentielles. JavaScript peut enrichir l'expérience, mais son absence ou son échec ne doit jamais laisser une page vide, un texte masqué ou une navigation inutilisable.

---

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

---

## 4. Workflow obligatoire

### Phase A0 — Cadrage, ERP et sources

Avant de construire, obtenir ou retrouver :

- l'URL de préproduction et le domaine public final prévu ;
- `COMPANY_ID` et `PROJECT_ID`, puis consulter les deux fiches ERP en lecture seule ;
- le node Figma exact, les captures de référence et le dossier des captures de retours ;
- les documents qui associent les textes et médias à chaque page ou section ;
- les textes validés, coordonnées légales, horaires, tarifs et informations d'hébergement ;
- les URLs officielles des réseaux sociaux, de la fiche d'établissement et des destinations externes ;
- l'adresse de réception des formulaires et les paramètres d'expéditeur attendus ;
- les pages légales existantes et l'URL de la politique de protection des données ;
- les cartes, vidéos, PDF, téléchargements et codes d'intégration nécessaires ;
- la disponibilité des clés CAPTCHA, accès SMTP et licences, sans les recopier dans les comptes rendus ;
- les pages hors périmètre et les contraintes intangibles, par exemple les polices à conserver ;
- les dates de recette interne et de validation client lorsqu'elles existent.

Classer chaque donnée par source. Ne jamais compléter une donnée manquante par une supposition. Chercher d'abord dans WordPress, l'ERP consulté en lecture seule, les documents du projet et les sources fournies.

### Phase A1 — Audit du WordPress

Avant toute écriture via le MCP WordPress :

1. identifier la version WordPress si elle est exposée ;
2. confirmer la présence et la version exacte d'Oxygen 6.x ;
3. lister les pages importantes ;
4. identifier la page d'accueil ;
5. identifier les Templates Oxygen existants, leurs Locations, Conditions et Priority ;
6. identifier les Headers Oxygen existants et leurs règles d'application ;
7. identifier les Footers Oxygen existants et leurs règles d'application ;
8. identifier les Components existants et leurs Component Properties ;
9. identifier les menus WordPress et leurs items ;
10. identifier les classes/selectors et collections de Variables déjà utilisées ;
11. identifier les catégories d'articles et leur **slug réel** ;
12. identifier les articles récents utiles au développement ;
13. identifier les images/médias existants ;
14. vérifier Yoast SEO et les métadonnées existantes ;
15. relever les URLs réelles de contact, actualités, mentions légales, politique de confidentialité, réservation, etc. ;
16. lister les éléments Oxygen réellement disponibles, sans supposer qu'un élément Gallery, Accordion, Form ou Slider existe ;
17. vérifier les plugins actifs, leur rôle, leur licence si elle conditionne le fonctionnement, et les erreurs JavaScript existantes ;
18. ouvrir l'éditeur dans Chrome lorsqu'un problème semble propre au navigateur embarqué, avant de conclure que les données Oxygen sont cassées.

Ne pas créer un doublon d'une page, d'un menu ou d'un template qui existe déjà.

### Phase A2 — Sauvegarde proportionnée au risque

Avant une refonte, suppression, import global, modification de styles partagés ou opération difficile à annuler :

1. sauvegarder la base de données ;
2. sauvegarder les fichiers si l'intervention touche les médias, plugins, thèmes ou fichiers ;
3. exclure le répertoire de sauvegarde de sa propre archive ;
4. stocker la copie hors des répertoires publics du site ;
5. calculer une somme SHA-256 ;
6. noter le périmètre, la date, le chemin, la taille et la somme de contrôle ;
7. vérifier que les fichiers existent et ont une taille cohérente avant de commencer.

Une sauvegarde de base peut suffire pour une modification limitée aux structures Oxygen stockées en base. Toute modification de fichiers ou médias exige une sauvegarde complète. Sauvegarder aussi les arbres JSON, Components, Header, Footer, Templates, Selectors, Variables et réglages concernés lorsque les outils le permettent.

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

### Phase D — Plan d'architecture Oxygen

Avant de construire la home, décider :

- ce qui appartient à un Template ;
- ce qui appartient à un Header ou Footer dédié ;
- ce qui devient Component ;
- quelles valeurs deviennent Component Properties ;
- ce qui devient classe/selector réutilisable ;
- ce qui devient Variable globale ;
- ce qui est propre à la home ;
- ce qui doit devenir dynamique avec WordPress ;
- ce qui peut servir aux futures pages internes.

### Phase E — Implémentation par blocs

Construire dans cet ordre recommandé :

1. Variables globales nécessaires ;
2. Classes / Selectors réutilisables ;
3. Components génériques ;
4. Header Oxygen ;
5. Footer Oxygen ;
6. Templates + Template Content Area si nécessaires ;
7. Component Hero ;
8. sections propres à la home ;
9. contenus dynamiques / Post Loop Builder ;
10. interactions ;
11. responsive ;
12. SEO ;
13. formulaires, Complianz et WP Mail SMTP ;
14. pages légales et menus associés ;
15. performance ;
16. QA finale.

Après chaque gros bloc : sauvegarder, ouvrir le front, contrôler le rendu avant de continuer.

---

## 5. Traduire Figma vers Oxygen proprement

### 5.1. Ne pas copier le code Figma brut

Le code design-to-code peut contenir beaucoup de :

```text
position:absolute
left/top fixes
width/height 1920px
React
Tailwind
wrappers purement visuels
```

Ce n'est pas la structure de production attendue.

Convertir l'intention en :

- Sections / Divs Oxygen ;
- flexbox ;
- CSS Grid lorsqu'il s'agit vraiment d'une grille ;
- colonnes structurées pour les compositions texte/image ;
- `max-width` + largeur fluide ;
- paddings/gaps ;
- pseudo-éléments uniquement pour décoratif léger ;
- assets SVG/images exacts pour les formes complexes.

### 5.2. Absolute positioning

Autorisé pour :

- décoration ;
- éléments volontairement flottants ;
- badge superposé ;
- formes graphiques ;
- rail social fixed ;
- éléments dont l'overlap est réellement visible dans Figma.

Interdit comme technique principale pour reconstruire toute une page desktop.

### 5.3. Assets Figma

- Utiliser les images et SVG réels exportés par Figma lorsqu'ils font partie du design.
- Ne jamais recréer « à peu près » un logo, une icône ou un SVG complexe.
- Les URLs d'assets retournées par Figma MCP sont temporaires : **ne jamais les laisser en production**.
- Télécharger/importer les assets durables dans WordPress Media ou dans l'emplacement prévu par le projet.
- Optimiser les rasters avant ou pendant l'import lorsque le workflow le permet.
- Conserver le ratio/cadrage Figma via `object-fit`, `object-position` ou l'outil Oxygen adapté.
- Si Figma ou le dossier projet fournit un favicon, exporter le node exact, générer les formats requis par WordPress et vérifier le rendu dans l'onglet du navigateur. Ne pas fabriquer une icône approchante.

### 5.4. Variables Oxygen 6

Utiliser en priorité le système **Oxygen > Variables** au lieu d'ajouter un deuxième design system en CSS brut.

Si aucun système existant ne couvre la nouvelle charte, créer des collections limitées, par exemple :

```text
Brand Colors
- color-primary
- color-secondary
- color-text
- color-surface

Typography
- font-heading
- font-body

Spacing
- space-xs
- space-sm
- space-md
- space-lg
- space-section

Layout
- container-max
- radius-sm
- radius-md
- radius-lg
```

Règles :

- réutiliser une Variable existante lorsque son rôle correspond ;
- ne pas dupliquer une Variable avec un nom différent pour la même valeur/rôle ;
- utiliser les types Oxygen adaptés : Color, Number, Unit, Font Family, Image URL ;
- préférer les Variables dans les contrôles Oxygen plutôt que `var(...)` injecté partout à la main ;
- les overrides de Variables servent aux variantes ponctuelles, pas à contourner un Component mal conçu ;
- CSS custom `:root` uniquement si une contrainte technique ne peut pas être couverte nativement et après vérification de l'existant ;
- ne pas créer 50 variables pour des valeurs utilisées une seule fois.

---

## 6. Architecture réutilisable Oxygen 6.x

### 6.1. Architecture globale recommandée

Oxygen 6 possède des objets dédiés. Ne pas recréer artificiellement l'architecture Classic.

Architecture générique recommandée :

```text
Oxygen
├── Header "Global"              -> Location/Conditions adaptées
├── Footer "Global"              -> Location/Conditions adaptées
├── Templates
│   ├── Page / contenu si nécessaire
│   │   └── Template Content Area
│   ├── Single Article si dans le scope
│   └── Archives si dans le scope
├── Components
│   ├── Hero
│   ├── Button / CTA variant si utile
│   ├── News Card
│   ├── Social Rail
│   └── autres patterns réellement répétés
├── Variables
│   ├── Colors
│   ├── Typography
│   ├── Spacing
│   └── Layout / Radius si pertinent
└── Classes / Selectors
```

Un Header/Footer global n'a pas besoin d'être dupliqué dans chaque Template. Utiliser les types **Headers** et **Footers** d'Oxygen 6, avec `Everywhere` ou des conditions plus fines selon le projet.

### 6.2. Template Content Area

Lorsqu'un Template doit afficher le contenu propre à chaque page/post :

- insérer **Template Content Area** à l'emplacement prévu ;
- ne jamais utiliser l'ancien concept `Inner Content` ;
- vérifier qu'un template MCP créé possède bien son Template Content Area lorsqu'il doit afficher du contenu spécifique ;
- ne pas mettre le contenu unique d'une page directement dans le Template générique.

### 6.3. Header

Créer/modifier un objet **Header Oxygen 6** dédié.

Le header doit :

- respecter strictement Figma ;
- utiliser le menu WordPress réel si un menu existe ;
- avoir des liens réels ;
- gérer l'état courant ;
- rester sticky sur toutes les pages et à tous les breakpoints ;
- être responsive ;
- être navigable au clavier ;
- conserver un comportement utilisable sans hover ;
- ne pas dépendre d'un JS lourd pour une simple navigation.

Le sticky est obligatoire. Utiliser en priorité le réglage natif Oxygen ou `position: sticky` avec un `top` et un `z-index` maîtrisés. Mesurer la hauteur réelle du header à chaque breakpoint et réserver l'espace nécessaire au premier hero ou au contenu suivant. Vérifier qu'aucun parent avec `overflow` incompatible ne désactive le sticky. Aucun titre, ancre ou contrôle ne doit passer sous le header.

Configuration :

- `Location: Everywhere` pour un header global, sauf besoin contraire ;
- Conditions uniquement si nécessaires ;
- vérifier Priority lorsqu'il existe plusieurs headers applicables.

Si un menu mobile est nécessaire :

- utiliser un bouton réel ;
- `aria-expanded` doit refléter l'état ;
- ouverture/fermeture clavier ;
- fermeture Escape lorsque possible ;
- focus visible ;
- préférer les interactions/éléments natifs Oxygen 6 quand ils couvrent proprement le besoin.

### 6.4. Footer

Créer/modifier un objet **Footer Oxygen 6** dédié.

Le footer doit :

- être défini une seule fois pour les zones concernées ;
- reprendre les coordonnées réelles ;
- utiliser `mailto:` pour les emails ;
- utiliser `tel:` pour les numéros ;
- avoir de vrais liens pour mentions légales / confidentialité ;
- réutiliser les réseaux sociaux réels ;
- ne pas hard-coder l'année si une valeur dynamique propre existe déjà ;
- utiliser le menu WordPress réel du footer pour afficher **Politique de protection des données**, **Mentions légales** et, lorsqu'elles existent ou sont applicables, les **Conditions générales de vente** ;
- afficher le crédit de réalisation Octacom sur tous les sites, même si Figma ne le montre pas. Cette règle de livraison explicite prime sur l'absence du crédit dans la maquette.

Markup du crédit :

```html
<span>Réalisation</span><span id="copyright-logo"></span>
```

Style de base :

```css
#copyright-logo {
  display: inline-block;
  background: url('https://www.octacom.fr/images/logo.png') no-repeat center;
  /* Variante sur fond sombre : https://www.octacom.fr/images/logo-blanc.png */
  background-size: contain;
  height: 17px;
  width: 80px;
}
```

Choisir le logo rouge/classique ou blanc selon le contraste du fond. Conserver le markup demandé. Scoper les règles complémentaires au Footer pour éviter qu'un ancien style global ou le rail social ne les écrase.

Vérifier Location, Conditions et Priority comme pour le Header.

### 6.5. Hero réutilisable = Component

Si plusieurs pages partagent le même squelette de hero, créer un **Component Hero**.

Utiliser des **Component Properties** pour les valeurs qui changent par instance, par exemple :

```text
hero.title
hero.text
hero.image
hero.cta_label
hero.cta_url
hero.variant
```

Ne créer que les propriétés réellement nécessaires.

Règles :

- styles/layout dans le Component ;
- contenu variable via Component Properties ou Dynamic Data selon le contexte ;
- variantes limitées et explicites ;
- utiliser le child visibility toggle si un CTA ou média est optionnel et que la version installée le supporte ;
- ne pas créer un Component qui nécessite ensuite 40 overrides locaux.

### 6.6. Components : règle de factorisation

Créer un Component quand au moins un de ces cas est vrai :

- le pattern apparaît à plusieurs endroits ;
- il doit être maintenu globalement ;
- il sert de template à un Post Loop Builder ;
- il a des variations maîtrisées exprimables via Component Properties.

Ne pas convertir chaque petit `div` en Component. Un Component doit représenter une vraie unité de design ou fonctionnelle.

### 6.7. Variables

Avant d'ajouter des valeurs brutes répétées, inspecter les Variables existantes.

Collections conseillées si le projet n'en a pas :

```text
Brand Colors
Typography
Spacing
Layout
```

Préférer les Variables Oxygen aux valeurs CSS dupliquées quand elles représentent un token global. Utiliser les overrides de Variables uniquement pour une vraie variante locale.

### 6.8. Classes et Selectors

Toujours réutiliser les classes/selectors existants adaptés avant d'en créer de nouveaux.

Si aucune convention projet n'existe, utiliser une convention claire :

```text
l-section
l-container
c-button
c-button--primary
c-button--secondary
c-hero
c-news-card
c-social-rail
u-sr-only
```

Dans Oxygen 6, le styling est centré sur les classes. Éviter de dupliquer des styles élément par élément.

Utiliser :

- States pour `:hover`, `:active`, `:focus-visible`, etc. ;
- Nested Selectors pour les sous-éléments et sélecteurs relationnels simples ;
- Selectors manuels pour les cas avancés réellement nécessaires.

Avant de modifier une classe partagée, lire toutes ses propriétés et rechercher ses usages. Avec les imports de règles Oxygen/MCP qui remplacent la règle du breakpoint au lieu de fusionner les propriétés, réécrire la règle complète. Lire les avertissements retournés après chaque import. Pour un besoin local, préférer une classe ciblée à une surcharge globale. Contrôler le front et les pages consommatrices après chaque modification globale.

Éviter les noms visuels fragiles : `blue-box-2`, `rectangle-54`, `left-thing`.

---

## 7. Exigence critique : la page doit rester éditable dans Oxygen

Une implémentation est refusée si :

- sélectionner une section dans Oxygen fait disparaître le design ;
- le builder ne charge pas les styles essentiels ;
- tout le layout dépend d'un JS exécuté seulement côté front ;
- le contenu visible n'existe que dans des pseudo-éléments CSS ;
- une grosse section est reconstruite dans un unique bloc HTML/PHP alors qu'elle doit être modifiable visuellement ;
- la structure Oxygen est remplacée par un énorme blob HTML/import HTML alors que des éléments natifs suffisent ;
- les styles dépendent de sélecteurs DOM hyper fragiles produits par Oxygen.

Exemples attendus : une galerie simple utilise des Containers, liens et Images éditables ; une FAQ utilise un vrai Accordion si cet élément existe ; une liste d'articles utilise Dynamic Data et un loop ; un carrousel utilise l'élément natif disponible seulement si le besoin justifie un carrousel.

### 7.1. Test « Builder Editability » obligatoire

Pour chaque section majeure :

1. ouvrir la page dans Oxygen ;
2. sélectionner la section ;
3. sélectionner ses enfants importants ;
4. vérifier que le rendu reste visible ;
5. modifier temporairement une propriété simple puis l'annuler ;
6. vérifier qu'aucun JS ne doit être déclenché pour « restaurer » le design ;
7. après toute modification faite hors de l'éditeur ouvert, recharger Oxygen avant de sauvegarder ;
8. sauvegarder uniquement après validation.

Le front ET le builder doivent être cohérents.

---

## 8. Responsive : règles obligatoires

Le desktop Figma n'est pas une page à réduire proportionnellement.

Le responsive doit respecter l'intention du design avec :

- largeur fluide ;
- `max-width` ;
- flex/grid ;
- images responsives ;
- typographie fluide lorsque pertinent ;
- gaps adaptatifs ;
- réorganisation sémantique des colonnes ;
- aucune barre horizontale parasite.

### 8.1. Breakpoints

Utiliser les breakpoints configurés dans le projet Oxygen 6.x. Ne pas inventer une seconde stratégie concurrente si le site possède déjà ses breakpoints.

Tester au minimum autour de :

```text
320
360
390
480
768
1024
1280
1440
1920 px
```

Tester également **entre** les breakpoints : le bug qui apparaît à 930 px compte autant que celui qui apparaît exactement à 1024 px.

### 8.2. Règles de layout

- pas de largeur de contenu fixe égale au canvas Figma ;
- `width: 100%` + `max-width` pour les conteneurs ;
- une vraie grille de cards peut devenir 3 -> 2 -> 1 colonnes ;
- une section texte/image peut passer en colonne ;
- préserver l'ordre de lecture logique en mobile ;
- ne pas utiliser `order` pour produire un ordre visuel qui contredit fortement l'ordre DOM accessible ;
- adapter les tableaux à leur contenu et au viewport : colonnes compactes, défilement horizontal annoncé ou présentation alternative accessible lorsque nécessaire ;
- les textes ne doivent pas être coupés par des hauteurs fixes ;
- limiter les `height` fixes aux éléments réellement dimensionnés par le design ;
- préférer `min-height`, ratio ou contenu naturel pour les sections.

Pour une section texte/média, la quantité de contenu et le format du média déterminent les proportions, pas une grille 50/50 automatique :

- étendre le texte sur toute la largeur si aucun média n'est prévu ;
- placer un média panoramique au-dessus du texte lorsque la colonne latérale créerait de grands vides ;
- limiter la hauteur visible d'un portrait sans le déformer ;
- déplacer la suite d'un texte sous le média si une colonne devient nettement plus longue ;
- vérifier séparément les variantes média à gauche et média à droite ;
- garder un rythme vertical régulier, souvent 12 à 18 px entre paragraphes liés, puis ajuster à la typographie réelle ;
- réduire les paddings ou CTA trop hauts sans supprimer l'espace qui marque un changement de sujet.

### 8.3. Hover et tactile

Aucune information essentielle ne doit exister uniquement au hover.

Tout état hover important doit disposer d'un équivalent :

- `:focus-visible` / `:focus-within` au clavier ;
- comportement utilisable au tactile ;
- contenu toujours accessible dans le DOM.

### 8.4. Motion

Pour les animations non essentielles :

```css
@media (prefers-reduced-motion: reduce) {
  /* réduire/supprimer les transitions et animations non indispensables */
}
```

Utiliser d'abord l'Interactions Engine Oxygen. Le style par défaut de tout élément animé doit être son état final visible. Appliquer l'état initial masqué ou décalé uniquement après l'initialisation réussie du mécanisme d'animation. Ne jamais enregistrer dans Oxygen un contenu essentiel durablement en `opacity: 0`, `visibility: hidden`, `display: none` ou hors écran dans l'attente d'un script.

Une animation d'apparition ne doit jamais laisser le contenu invisible si JavaScript est désactivé, bloqué, en erreur ou si son observer ne se déclenche pas. Tester le chargement direct, le retour arrière, le mobile, `prefers-reduced-motion` et la page avec JavaScript désactivé.

Ne pas ajouter des animations décoratives qui n'existent pas dans Figma juste pour « faire premium ».

### 8.5. Sticky ciblé

Réserver `position: sticky` aux médias latéraux qui accompagnent un texte long :

- desktop seulement, sauf preuve contraire dans la maquette ;
- `top` calculé avec la hauteur réelle du header sticky et une marge visible ;
- désactivation sous 1024 px par défaut ;
- exclusion des vidéos, carrousels et médias panoramiques placés au-dessus du texte ;
- hauteur maximale d'un portrait limitée à la fenêtre sans déformation ;
- arrêt naturel à la fin de la section par le bon conteneur parent.

Ne jamais appliquer un sticky global à tous les médias.

---

## 9. Réseaux sociaux fixed avec libellé au hover

Lorsqu'un design prévoit des réseaux sociaux en position fixe :

- créer un seul composant rail social réutilisable ;
- `position: fixed` uniquement si la maquette ou le brief le demande ;
- chaque réseau est un vrai `<a>` ;
- icône exacte ;
- `aria-label` explicite ;
- libellé du réseau présent dans le DOM ;
- expansion au `:hover` ;
- même expansion ou équivalent au `:focus-visible` ;
- transition courte et légère ;
- ne pas masquer le contenu principal ;
- respecter les safe areas et petits écrans ;
- vérifier le z-index contre menu, cookies et modales.

Exemple de logique, à adapter aux classes réelles :

```css
.c-social-link {
  display: inline-flex;
  align-items: center;
  overflow: hidden;
}

.c-social-link__label {
  max-width: 0;
  opacity: 0;
  white-space: nowrap;
  overflow: hidden;
}

.c-social-link:hover .c-social-link__label,
.c-social-link:focus-visible .c-social-link__label {
  max-width: 10rem;
  opacity: 1;
}
```

Ne jamais faire dépendre le nom du réseau d'un `::after` uniquement : le texte doit exister dans le DOM.

---

## 10. Téléphone, email, adresse et boutons

### Téléphone

Affichage lisible, lien normalisé :

```html
<a href="tel:+33XXXXXXXXX">04 XX XX XX XX</a>
```

Ne pas inventer l'indicatif ou normaliser une donnée dont la valeur source n'est pas connue.

### Email

```html
<a href="mailto:contact@example.fr">contact@example.fr</a>
```

Pas besoin de `target="_blank"` sur `mailto:`.

### Adresse

Si une URL Maps réelle est fournie ou déjà utilisée par le site, rendre l'adresse cliquable.

Tous les liens HTTP externes s'ouvrent dans un nouvel onglet avec `rel="noopener noreferrer"`. Les liens internes restent dans le même onglet. `mailto:` et `tel:` ne reçoivent pas de `target="_blank"`.

```html
<a href="..." target="_blank" rel="noopener noreferrer">...</a>
```

### Boutons

Chaque bouton doit avoir :

- une action claire ;
- une destination réelle ;
- un libellé descriptif ;
- un état hover ;
- un état focus visible ;
- un contraste suffisant ;
- une zone tactile correcte.

Un bouton qui navigue doit être un lien, pas un faux bouton JavaScript.

---

## 11. Actualités dynamiques WordPress

Une section actualités ne doit pas contenir deux cards copiées manuellement si le site possède de vrais articles.

### 11.1. Oxygen 6.x

Priorité :

1. créer un **Component `News Card`** unique pour le rendu d'un article ;
2. utiliser **Post Loop Builder** ;
3. sélectionner le Component `News Card` comme template de chaque résultat ;
4. configurer la query du Post Loop Builder avec le Query Builder visuel ;
5. utiliser une **Array Query** uniquement lorsqu'une query avancée ne peut pas être exprimée proprement autrement ;
6. PHP/WP_Query custom uniquement en dernier recours.

Ne pas utiliser les concepts Classic `Easy Posts` ou `Reusable Part` dans un nouveau projet Oxygen 6.

Le Component de card doit lier ses éléments à la **Dynamic Data** du post : titre, permalink, date, image à la une, extrait si demandé.

### 11.2. Query « deux dernières actualités »

Toujours résoudre le slug réel de la catégorie avec WordPress avant de configurer la query.

Configurer nativement l'équivalent suivant dans le Post Loop Builder. L'exemple PHP ci-dessous est une **spécification logique**, pas une obligation d'implémentation :

```php
$args = [
    'post_type'           => 'post',
    'post_status'         => 'publish',
    'posts_per_page'      => 2,
    'category_name'       => $actualites_category_slug,
    'orderby'             => 'date',
    'order'               => 'DESC',
    'ignore_sticky_posts' => true,
    'no_found_rows'       => true,
];
```

Règles :

- x articles maximum précisé par le user ou lui demander ;
- plus récent en premier ;
- date WordPress réelle ;
- image à la une réelle ;
- titre réel ;
- permalink réel ;
- pas de duplication d'une seconde query juste pour styler différemment le premier élément.

### 11.3. Premier article affiché dans l'état « hover »

Quand le brief demande :

```text
article 1 = apparence hover par défaut
article 2 = état normal
```

Le composant card doit rester unique.

Approche recommandée :

- construire un état normal ;
- construire un état hover/focus ;
- appliquer le même style hover au premier item au repos via une classe/modificateur ou un sélecteur de premier item ;
- conserver le vrai hover/focus sur tous les items.

Concept :

```css
.c-news-card:hover,
.c-news-card:focus-within,
/* sélecteur exact du premier item vérifié dans le DOM */
...:first-child .c-news-card {
  /* état hover */
}
```

Ne pas utiliser `:first-child` au hasard. Inspecter le DOM réellement généré par Post Loop Builder et vérifier que le sélecteur cible bien le premier résultat. Si la version 6.2 installée expose `Raw Mode`, il peut être utilisé pour supprimer les wrappers du loop lorsque cela simplifie le HTML sans casser le layout.

### 11.4. Cas limites

- 0 article : section vide propre ou message prévu par le projet, jamais faux contenu.
- 1 article : afficher un item sans casser la grille.
- image à la une absente : utiliser uniquement le fallback défini par le projet ; ne pas inventer une photo.
- contenu très long : utiliser titre/date/extrait selon la maquette, sans couper avec une hauteur rigide qui déborde sur mobile.

---

## 12. Avis via iframe

Si le brief précise que les avis seront intégrés plus tard via iframe et demande uniquement le titre :

- créer uniquement la section et le titre demandés ;
- ne pas recopier les faux avis de la maquette ;
- ne pas fabriquer un iframe ;
- prévoir une structure qui pourra accueillir le widget sans devoir casser toute la section.

Lorsqu'un iframe réel est ajouté plus tard :

- `title` accessible obligatoire ;
- réserver la hauteur ou le ratio pour éviter le CLS ;
- lazy-load s'il est sous la ligne de flottaison et que le widget le supporte ;
- ne pas ajouter un `sandbox` susceptible de casser le widget sans vérifier sa documentation.

---

## 13. SEO technique et balisage

Le design ne doit jamais dégrader le HTML sémantique.

### 13.1. Structure HTML

Une page standard :

```text
<header>
<nav>
<main>
  <section>
    <h1>...</h1>
  </section>
  <section>
    <h2>...</h2>
    <h3>...</h3>
  </section>
</main>
<footer>
```

Règles :

- un H1 principal par page sauf cas exceptionnel justifié ;
- niveaux Hn cohérents ;
- ne jamais choisir H2/H3 uniquement pour la taille visuelle ;
- les titres décoratifs peuvent être des `div`, `span` ou paragraphes ;
- le contenu textuel important doit exister dans le DOM ;
- ne pas mettre du contenu SEO important uniquement dans `content:` CSS ;
- utiliser `<nav>` pour les navigations ;
- utiliser `<address>` avec discernement : uniquement pour les coordonnées réellement liées à l'auteur/propriétaire du document/section, sinon un bloc sémantique classique est acceptable.

### 13.2. Liens crawlables

Les liens internes importants doivent être de vrais liens :

```html
<a href="/page/">Texte descriptif</a>
```

Éviter :

```html
<span onclick="...">...</span>
<a onclick="...">...</a>
```

Le texte d'ancrage doit être descriptif lorsque cela reste compatible avec la maquette.

### 13.3. Yoast SEO

Si un connecteur Yoast est disponible :

- l'utiliser plutôt que d'écrire directement des métas privées en base ;
- lire l'état actuel avant modification ;
- préserver les valeurs éditoriales déjà définies ;
- vérifier title ;
- meta description ;
- canonical ;
- robots ;
- OpenGraph ;
- image sociale lorsque pertinente ;
- Schema généré.

Après modification, contrôler le rendu ou les données Yoast retournées pour l'URL.

Ne pas dupliquer manuellement dans le `<head>` ce que Yoast génère déjà.

### 13.4. Métadonnées

Chaque page importante doit avoir :

- `<title>` descriptif et propre à la page ;
- meta description utile et propre à la page ;
- canonical cohérente ;
- URL finale cohérente ;
- indexabilité vérifiée avant mise en production.

On peut rédiger un title/description à partir du contenu métier validé, mais on ne doit jamais ajouter une promesse ou information commerciale absente des sources.

### 13.5. Schema.org

Quand Yoast est présent, privilégier son graphe Schema et ses APIs/extensions plutôt que d'ajouter un second JSON-LD indépendant.

Pour un établissement local, utiliser le type le plus spécifique pertinent si le projet et les outils le permettent :

```text
LocalBusiness
Restaurant
Store
ProfessionalService
...
```

Ne renseigner que des informations vérifiées :

- nom ;
- URL ;
- adresse ;
- téléphone ;
- horaires ;
- logo ;
- image ;
- type de cuisine/menu lorsque pertinent et vérifié.

**Ne jamais fabriquer de `review` ou `aggregateRating` Schema à partir d'un widget d'avis du propre établissement.** Respecter les règles Google et le graphe Yoast existant.

### 13.6. Articles

Lorsque le site possède des articles :

- page article / template single cohérent ;
- titre visible ;
- date réelle ;
- image à la une ;
- contenu ;
- canonical ;
- données Article gérées par Yoast quand applicable ;
- liens vers les articles générés dynamiquement.

Toujours créer le template single ; La home doit utiliser des permaliens compatibles avec ces templates.

### 13.7. Pages légales, Complianz et consentement

- Créer ou compléter les mentions légales à partir de [`templates/mentions-legales.html.tpl`](templates/mentions-legales.html.tpl). Remplacer chaque variable par une donnée confirmée. Ne jamais publier un placeholder.
- Demander en amont la raison sociale, la forme juridique, le capital si applicable, l'adresse postale complète, les téléphones et emails publiables, les numéros d'immatriculation, le responsable de publication, les coordonnées du responsable de traitement, le DPO si applicable, l'hébergeur et le propriétaire du site.
- Faire valider le contenu juridique par le client ou son conseil. Le template structure la collecte et la rédaction ; il ne constitue pas une validation juridique.
- La page de confidentialité porte strictement le titre **Politique de protection des données**.
- Générer cette page avec Complianz et conserver son contenu/shortcode géré par le plugin au lieu de recopier une politique statique parallèle.
- Ajouter **Politique de protection des données** et **Mentions légales** au menu WordPress du footer. Ajouter aussi les **Conditions générales de vente** lorsqu'une page validée existe ou que l'activité les exige. Rendre ce menu dans le Footer Oxygen et ne pas maintenir une seconde liste de liens légaux codée à la main. Ne jamais inventer des CGV ni publier une page CGV vide.
- Configurer Complianz pour le domaine public final, les services réellement présents, la zone juridique du projet et les scripts/iframes observés. Tester avant consentement, après acceptation, après refus et après retrait du consentement.
- Vérifier les wrappers ajoutés par Complianz autour des cartes, vidéos et autres iframes. Ils doivent respecter la largeur prévue et réserver leur hauteur.
- Une page légale vide, un shortcode brut non rendu ou un lien de footer cassé bloque la livraison.

---

## 14. Images

### 14.1. Alt

- Image informative : `alt` descriptif.
- Image décorative : `alt=""`.
- Logo : alt correspondant au nom de l'entité lorsqu'il apporte cette information.
- Ne pas bourrer les `alt` de mots-clés.
- Ne pas importer ou afficher deux fois le même média pour résoudre un problème de mise en page.

### 14.2. Responsive images

Laisser WordPress produire/utiliser `srcset` et `sizes` lorsque possible.

Respecter le rôle du média :

- `object-fit: contain` pour un logo, pictogramme, portrait ou document qui ne doit pas être coupé ;
- `object-fit: cover` seulement pour une vignette volontairement recadrée ;
- miniature optimisée dans une grille, liée à l'original si un agrandissement est demandé ;
- ratio d'origine conservé sauf recadrage explicitement prévu par la maquette.

Toujours éviter qu'une image dépasse son conteneur :

```css
img {
  max-width: 100%;
  height: auto;
}
```

### 14.3. Dimensions et CLS

Chaque image doit avoir des dimensions intrinsèques ou un ratio réservé.

Préférer :

```html
<img src="..." width="1200" height="800" alt="...">
```

ou un conteneur avec `aspect-ratio` si le layout l'exige.

### 14.4. LCP

L'image principale visible immédiatement :

- ne doit pas être `loading="lazy"` ;
- doit être découvrable tôt ;
- peut recevoir `fetchpriority="high"` si elle est très probablement l'élément LCP et si l'implémentation le permet proprement ;
- ne doit pas dépendre d'un JS tardif ;
- éviter de la cacher dans un background CSS si une vraie balise image permet la même fidélité et une meilleure découverte de ressource.

### 14.5. Images sous la ligne de flottaison

- `loading="lazy"` lorsque pertinent ;
- `decoding="async"` lorsque le système le gère correctement ;
- formats et tailles adaptés ;
- ne pas charger une image 4000 px pour une card de 400 px.

### 14.6. Galerie ou carrousel

Utiliser une galerie quand la personne doit parcourir un album. Utiliser un carrousel quand le nombre d'éléments visibles doit rester faible, que l'ordre raconte une séquence ou que le besoin produit le demande.

Galerie classique :

- grille native et éditable, avec vignettes cohérentes ;
- cible par défaut de 4 colonnes desktop, 3 tablette et 2 mobile, adaptée si Figma indique autre chose ;
- lien vers l'original si agrandissement demandé ;
- focus clavier visible et chargement différé sous la ligne de flottaison ;
- même traitement pour les albums d'une même page.

Vrai carrousel :

- élément Oxygen/Swiper existant avant toute implémentation custom ;
- glissement tactile, flèches, pagination et clavier si ces commandes sont présentes ;
- nombre de cartes adapté à chaque largeur ;
- hauteur compatible avec les contenus longs ;
- aucune couleur bleue par défaut héritée du navigateur ou de Swiper ;
- autoplay seulement s'il sert le contenu, avec arrêt ou contrôle accessible lorsque requis.

Une simple rangée à défilement horizontal ne doit pas être présentée comme un carrousel si le brief demande de vraies commandes.

---

## 15. Performance

Objectifs Core Web Vitals recommandés :

```text
LCP <= 2,5 s
INP <= 200 ms
CLS <= 0,1
```

à viser au 75e percentile mobile et desktop.

### 15.1. CSS

- mutualiser les styles dans les classes ;
- ne pas dupliquer la même déclaration sur 30 IDs Oxygen ;
- éviter les sélecteurs très profonds ;
- ne pas importer une librairie CSS complète pour une animation ou une grille simple ;
- pas de CSS bloquant externe inutile.

### 15.2. JavaScript

- appliquer l'amélioration progressive : contenu, navigation et actions essentielles disponibles avant l'exécution du script ;
- JavaScript minimal ;
- vanilla JS si aucun besoin d'une dépendance supplémentaire ;
- ne pas ajouter jQuery si le composant peut fonctionner sans et que jQuery n'est pas nécessaire ;
- listeners légers ;
- pas de boucle ou observer permanent inutile ;
- limiter le travail main-thread ;
- différer les scripts non critiques lorsque possible ;
- éviter les animations JS pour des transitions réalisables en CSS.

Prévoir un rendu sans JavaScript pour les composants enrichis : navigation mobile accessible, accordéons lisibles ou ouverts, carrousels présentés comme une liste statique, coordonnées et liens de carte visibles, médias accompagnés d'un lien direct lorsque pertinent. Un message `<noscript>` peut expliquer la perte d'une fonction secondaire, mais ne remplace jamais le contenu masqué.

### 15.3. Fonts

- utiliser les polices exactes de Figma ;
- ne pas substituer silencieusement une police ;
- limiter les poids réellement chargés ;
- privilégier un hébergement performant/self-host si la licence et le projet le permettent ;
- ne jamais importer plusieurs fois la même font ;
- utiliser un fallback cohérent ;
- surveiller les layout shifts causés par le chargement des polices.

### 15.4. Iframes / widgets tiers

- charger sous le fold lorsque possible ;
- réserver l'espace avant chargement ;
- n'ajouter que les widgets réellement nécessaires ;
- mesurer leur impact avant d'empiler 5 scripts marketing.

---

## 16. Accessibilité

Le minimum attendu :

- navigation clavier ;
- focus visible ;
- liens et boutons correctement typés ;
- `aria-label` sur les liens icône seuls ;
- menu mobile accessible ;
- textes alternatifs ;
- pas de texte important uniquement en image ;
- pas d'information uniquement par couleur ;
- hover doublé d'un focus ;
- animations réduites si préférence utilisateur ;
- ordre DOM logique ;
- labels de formulaire réels lorsque des formulaires sont dans le scope.

Si la charte Figma contient un contraste manifestement insuffisant :

- ne pas modifier silencieusement la charte ;
- relever la paire couleur/fond problématique ;
- proposer la correction minimale conforme ;
- appliquer la décision utilisateur.

### 16.1. États globaux

Définir et vérifier dès le début : liens normaux, hover, `:focus-visible`, état actif du menu, boutons primaires/secondaires, liens sur fond sombre, téléphone et email. L'état courant doit fonctionner sur chaque page, en desktop et dans le menu mobile. Aucun bleu navigateur, WordPress ou Swiper ne doit apparaître par défaut sauf choix explicite de la charte.

### 16.2. Formulaire de contact et délivrabilité

Utiliser l'élément Form Oxygen ou le composant déjà validé du projet lorsqu'il répond au besoin. Une implémentation manuelle vient en dernier recours et respecte HTML sémantique, WAI-ARIA applicable, sécurité serveur et amélioration progressive.

Le formulaire doit avoir :

- labels visibles et associés aux champs ;
- champs et bouton cohérents avec le design system ;
- case de consentement obligatoire quand le traitement l'exige, avec lien vers **Politique de protection des données** ;
- CAPTCHA réellement configuré, honeypot et protection CSRF/nonce ;
- adresse de destination et adresse d'expéditeur vérifiées ;
- messages de succès et d'erreur explicites ;
- focus visible, erreurs associées aux champs et affichage mobile pleine largeur.

Configurer WP Mail SMTP avec le fournisseur, le domaine public final, l'expéditeur et les identifiants validés. Ne pas inventer de serveur, port, chiffrement ou adresse. Tester séparément : connexion SMTP, envoi réel, réception, Reply-To, échec contrôlé et journaux disponibles. La présence du plugin ou d'un message de succès côté navigateur ne prouve pas la réception.

Tester aussi le CAPTCHA avec Complianz actif. Vérifier la présence du widget ou du jeton, la validité des clés pour le domaine final, le consentement requis, l'absence de double initialisation et l'absence de boucle de rechargement.

---

## 17. Anti-slop design

La fidélité à Figma interdit les « améliorations IA » gratuites.

Ne pas ajouter sans preuve dans la charte :

- glassmorphism ;
- gradients supplémentaires ;
- grosses ombres génériques ;
- pills partout ;
- cards supplémentaires ;
- icônes aléatoires ;
- halos ;
- animations d'entrée systématiques ;
- blobs décoratifs ;
- sections inventées ;
- textes marketing inventés ;
- CTA supplémentaires ;
- changement de rayon pour « moderniser » ;
- redesign du footer/menu parce que l'agent préfère autre chose.

Le rôle de l'agent est de traduire la direction artistique, pas d'en créer une seconde par-dessus.

---

## 18. QA visuelle obligatoire avec navigateur

Lorsque l'environnement fournit un navigateur ou outil de preview, il doit être utilisé.

### 18.1. Workflow de comparaison

Pour chaque section :

1. ouvrir la page front ;
2. régler le viewport sur la largeur Figma de référence ;
3. comparer à la capture Figma ;
4. contrôler :
   - dimensions globales ;
   - max-width ;
   - alignements ;
   - gaps ;
   - padding ;
   - typo ;
   - line-height ;
   - couleurs ;
   - rayons ;
   - crops images ;
   - overlays ;
   - décorations ;
   - états hover ;
5. corriger ;
6. recharger et comparer à nouveau.

Ne pas tout juger « à l'œil » depuis le code.

### 18.2. Responsive QA

Tester au minimum 1440, 1280, 1024, 768, 390, 360 et 320 px, puis une largeur intermédiaire proche de chaque changement de layout.

Vérifier :

- overflow horizontal ;
- textes coupés ;
- éléments fixed qui masquent le contenu ;
- menu ;
- boutons ;
- images ;
- colonnes ;
- carrousels ;
- footer ;
- rail social ;
- hover/focus ;
- zone tactile.
- formulaires et cartes utilisant toute la largeur disponible ;
- sticky désactivé ou sûr aux largeurs prévues ;
- aucun rechargement en boucle.

### 18.3. QA technique

Avant de déclarer terminé :

- page testée avec JavaScript désactivé : tout le contenu, la navigation et les actions essentielles restent clairs et visibles ;
- animations testées sans JavaScript et en cas d'échec de déclenchement : aucun élément ne reste masqué ;
- aucune erreur JS console liée aux modifications ;
- aucun 404 de ressource ;
- liens CTA testés ;
- téléphone/email testés ;
- permaliens actualités testés ;
- H1/H2 inspectés ;
- meta title/description inspectés ;
- canonical inspectée ;
- images alt inspectées ;
- pas de Figma asset temporaire dans le HTML final ;
- pas de contenu placeholder involontaire ;
- pas de lien `#` involontaire ;
- pas de style détruit dans le builder Oxygen ;
- front vérifié dans Chrome lorsque disponible ;
- formulaires reçus à l'adresse prévue via WP Mail SMTP ;
- CAPTCHA fonctionnel sans boucle de rechargement ;
- Complianz testé avant/après consentement et wrappers de carte/vidéo contrôlés ;
- pages **Politique de protection des données** et **Mentions légales** accessibles par le menu du footer, ainsi que les **Conditions générales de vente** lorsqu'elles existent ou sont applicables ;
- crédit Octacom présent, contrasté et non cassé ;
- éditeur Oxygen rechargé après la dernière mutation externe avant toute sauvegarde finale.

---

## 19. Règles MCP WordPress + Oxygen 6

### Lecture

Avant toute mutation, inspecter les abilities du serveur MCP puis lire l'objet actuel :

- page ;
- Template ;
- Header ;
- Footer ;
- Component et ses propriétés éditables ;
- Classes / Selectors ;
- Variables ;
- loop/query ;
- menu ;
- post ;
- catégorie ;
- média ;
- métadonnée SEO.

Si des abilities Oxygen natives existent, les préférer à l'écriture directe de post meta, JSON interne ou HTML importé.

Lors d'une mutation externe à Oxygen, noter quels objets ont changé. Considérer tout éditeur déjà ouvert comme périmé jusqu'à son rechargement.

### Écriture

- utiliser les abilities Oxygen natives les plus spécifiques disponibles ;
- modifier l'objet existant lorsqu'il correspond au besoin ;
- créer uniquement quand il n'existe pas ;
- préserver slug et statut lorsque la demande ne nécessite pas leur changement ;
- ne pas publier automatiquement un brouillon si l'utilisateur n'a pas demandé de publication ;
- ne pas supprimer un Template, Header, Footer, Component, Selector ou Variable partagé sans analyse des usages ;
- faire des modifications aussi atomiques que l'API le permet.

### Échec

En cas d'erreur :

1. lire l'erreur ;
2. relire l'état si l'écriture a pu être partiellement appliquée ;
3. ne pas répéter une requête destructive à l'identique ;
4. corriger la cause ;
5. vérifier l'état après succès ;
6. si un outil de preview Oxygen est exposé, rendre/inspecter l'élément ou la page modifiée.

---

## 20. Quand utiliser du code custom

Du code custom est acceptable pour :

- query WordPress impossible à exprimer proprement avec Post Loop Builder / Query Builder / Array Query ;
- interaction spécifique non disponible avec States, Nested Selectors ou Interactions Engine ;
- petite amélioration progressive ;
- SVG décoratif exporté / composant technique ;
- logique dynamique réellement nécessaire.

Avant d'en écrire, documenter quel élément ou mécanisme Oxygen a été recherché et pourquoi il ne couvre pas le besoin. Pour un widget interactif custom, appliquer le pattern WAI-ARIA correspondant, conserver les éléments HTML natifs possibles et tester clavier, tactile, focus et annonce des états.

Il n'est pas acceptable de :

- reconstruire toute une page en HTML dans un Code Block ;
- contourner les Components, Variables, Selectors ou loops Oxygen parce que c'est plus rapide ;
- injecter toutes les sections via JS ;
- écrire un mini page-builder maison ;
- dupliquer une fonction WordPress/Oxygen existante.

Le code custom doit être :

- scoped ;
- commenté lorsque sa raison n'est pas évidente ;
- stable dans le builder ;
- compatible responsive ;
- accessible ;
- sans dépendance inutile.

---

## 21. Règles pour les futures pages intérieures

La home doit préparer le terrain sans créer à l'avance des pages hors scope.

À réutiliser ensuite :

- Header Oxygen ;
- Footer Oxygen ;
- Templates nécessaires + Template Content Area ;
- Components ;
- Variables ;
- classes/selectors de boutons ;
- container/section ;
- styles de headings ;
- hero interne si réellement factorisable ;
- card actualité ;
- rail social ;
- décorations communes ;
- tokens de couleur/typo/radius/spacing.

Une page intérieure ne doit pas copier la home entière. Elle doit exploiter les composants communs et ne reprendre que les patterns pertinents.

Quand le site possède des actualités, prévoir lorsque cela entre dans le scope :

- archive/liste actualités ;
- template single article ;
- 404 ;
- mais ne pas les créer sans demande explicite si le travail actuel concerne uniquement la home.

---

## 22. Definition of Done

Le travail n'est terminé que si tous les points applicables sont vrais.

### Design

- [ ] Structure des sections conforme à Figma.
- [ ] Assets réels utilisés.
- [ ] Typographies conformes.
- [ ] Couleurs conformes.
- [ ] Espacements contrôlés.
- [ ] États hover/interactions conformes.
- [ ] Commentaires/annotations Figma appliqués lorsqu'accessibles.

### Oxygen 6.x

- [ ] Version exacte d'Oxygen confirmée.
- [ ] Header Oxygen dédié et règles Location/Conditions vérifiées.
- [ ] Header sticky fonctionnel sur toutes les pages et tous les breakpoints, sans masquer le contenu.
- [ ] Footer Oxygen dédié et règles Location/Conditions vérifiées.
- [ ] Templates utilisant Template Content Area lorsque nécessaire.
- [ ] Components réutilisables créés sans sur-abstraction.
- [ ] Component Properties utilisées pour les variations pertinentes.
- [ ] Variables existantes réutilisées avant création de valeurs parallèles.
- [ ] Classes/Selectors réutilisés.
- [ ] Page éditable dans Oxygen.
- [ ] Aucun gros blob HTML remplaçant le builder.
- [ ] Aucun concept Classic (`Reusable Part`, `Inner Content`, `Easy Posts`) introduit dans un nouveau build.
- [ ] Éditeur rechargé après les mutations externes et dernière version sauvegardée sans écrasement.
- [ ] Toute classe globale modifiée a été relue en entier et ses pages consommatrices ont été contrôlées.

### Responsive

- [ ] 320 px testé.
- [ ] 390 px testé.
- [ ] 768 px testé.
- [ ] 1024 px testé.
- [ ] Desktop testé à la taille de référence Figma.
- [ ] Aucun overflow horizontal.
- [ ] Menu utilisable.
- [ ] Fixed elements non bloquants.

### Contenu dynamique

- [ ] Actualités viennent de WordPress.
- [ ] Catégorie résolue par slug/ID réel.
- [ ] Ordre date DESC.
- [ ] 2 derniers posts si demandé.
- [ ] Permaliens réels.
- [ ] Cas 0/1 article acceptable.

### Liens

- [ ] Tous les CTA ont une destination.
- [ ] `tel:` sur téléphone.
- [ ] `mailto:` sur email.
- [ ] Aucun `#` factice involontaire.
- [ ] Liens externes ouverts dans un nouvel onglet munis de `rel="noopener noreferrer"`.

### SEO

- [ ] H1 unique.
- [ ] Hiérarchie Hn cohérente.
- [ ] Title vérifié.
- [ ] Meta description vérifiée.
- [ ] Canonical vérifiée.
- [ ] Liens crawlables.
- [ ] Alt images vérifiés.
- [ ] Yoast non dupliqué par du markup manuel.
- [ ] Schema cohérent si applicable.

### Performance

- [ ] LCP image non lazy.
- [ ] Images sous fold lazy lorsque pertinent.
- [ ] Dimensions/ratio des images réservés.
- [ ] Pas d'assets Figma temporaires.
- [ ] JS custom minimal.
- [ ] Iframes/widgets ne provoquent pas de CLS évitable.

### QA

- [ ] Front contrôlé avec navigateur si disponible.
- [ ] Builder Oxygen contrôlé.
- [ ] Site contrôlé avec JavaScript désactivé : contenu, navigation et actions essentielles visibles et utilisables.
- [ ] Animations défaillantes ou non initialisées ne masquent aucun contenu.
- [ ] Console sans erreur liée au dev.
- [ ] Aucun asset 404.
- [ ] Aucun placeholder involontaire.
- [ ] Sauvegarde proportionnée au risque créée et vérifiée.
- [ ] Complianz configuré et scénarios de consentement testés.
- [ ] Page **Politique de protection des données** générée par Complianz et présente dans le menu du footer.
- [ ] Page **Mentions légales** présente dans le menu du footer.
- [ ] **Conditions générales de vente** validées et présentes dans le menu du footer lorsqu'elles existent ou sont applicables.
- [ ] WP Mail SMTP configuré pour le domaine final et réception réelle vérifiée.
- [ ] Formulaire, consentement, CAPTCHA, honeypot et messages testés.
- [ ] Mentions légales remplies avec des données validées et sans variable de template restante.
- [ ] Crédit de réalisation Octacom présent dans le footer avec la bonne variante de logo.

---

## 23. Rapport final de l'agent

À la fin, répondre de façon courte et vérifiable :

```text
Implémenté
- ...

Réutilisable
- ...

Dynamique
- ...

QA effectuée
- Figma desktop : ...
- Responsive : ...
- Oxygen builder : ...
- SEO : ...
- Performance : ...

Reste / limites
- uniquement les vrais points non vérifiés
```

Ne pas écrire « tout est bon » si une partie n'a pas été testée.

Si le navigateur n'est pas disponible, écrire explicitement que la comparaison visuelle front n'a pas pu être effectuée.

Si les commentaires Figma ne sont pas exposés, écrire explicitement qu'ils n'ont pas pu être lus.

### Rapport de temps, tokens et coût

À la fin d'un développement complet, ajouter un récapitulatif du type `Récap <nom du site> — <modèle principal>` à partir des journaux réellement disponibles. Ne jamais estimer des tokens ou des coûts sans données.

Inclure, lorsque les journaux les exposent :

- heure de début et de fin, durée totale avec pauses et temps d'exécution actif ;
- détail par modèle utilisé ;
- tokens d'entrée hors cache, tokens d'entrée en cache, tokens de sortie incluant le raisonnement et total ;
- coût unitaire ou source tarifaire, coût par catégorie, coût par modèle et total ;
- part du cache dans les tokens d'entrée ;
- périmètre temporel exact du relevé et éventuelles lacunes des journaux.

Format recommandé :

```text
Récap <site> — <modèle principal>

Période : <début> à <fin>
Durée totale avec pauses : <durée>
Temps d'exécution cumulé : <durée>

Modèle | Entrée hors cache | Entrée en cache | Sortie + raisonnement | Total tokens | Coût
...

Total : <tokens> | <coût>
Part du cache dans les entrées : <pourcentage>
Source des tarifs : <source et date>
Limites du relevé : <aucune ou détails>
```

Si le runtime ne donne pas accès à une métrique, écrire `non disponible dans les journaux accessibles` au lieu de l'inventer. Les coûts doivent utiliser les tarifs applicables aux modèles et à la date du travail, avec la devise explicitée.

---

## 24. Sources officielles à privilégier

En cas de doute, chercher d'abord dans ces sources et citer la documentation utilisée dans le rapport technique lorsque la décision n'est pas évidente.

### Figma MCP

- Figma — *Introducing our Dev Mode MCP server: Bringing Figma into your workflow* (4 juin 2025)
  <https://www.figma.com/blog/introducing-figma-mcp-server/>
- Figma — Design systems + MCP / design context
  <https://www.figma.com/blog/design-systems-ai-mcp/>

Principes retenus : le MCP fournit contexte de design, screenshots, styles/variables/composants ; le code généré doit être adapté au vrai codebase et à ses composants.

### Responsive / performance

- web.dev — Learn Responsive Design
  <https://web.dev/learn/design/>
- web.dev — Responsive Images
  <https://web.dev/learn/design/responsive-images>
- web.dev — Optimize Largest Contentful Paint
  <https://web.dev/articles/optimize-lcp>
- web.dev — Optimize Cumulative Layout Shift
  <https://web.dev/articles/optimize-cls>
- web.dev — Optimize Interaction to Next Paint
  <https://web.dev/articles/optimize-inp>
- web.dev — Web Vitals
  <https://web.dev/articles/vitals>

### Google Search

- Google Search Central — SEO Starter Guide
  <https://developers.google.com/search/docs/fundamentals/seo-starter-guide?hl=fr>
- Google Search Central — SEO Guide for Web Developers
  <https://developers.google.com/search/docs/fundamentals/get-started-developers>
- Google Search Central — Liens crawlables
  <https://developers.google.com/search/docs/crawling-indexing/links-crawlable?hl=fr>
- Google Search Central — Image SEO
  <https://developers.google.com/search/docs/appearance/google-images>
- Google Search Central — LocalBusiness structured data
  <https://developers.google.com/search/docs/appearance/structured-data/local-business?hl=fr>
- Google Search Central — Article structured data
  <https://developers.google.com/search/docs/appearance/structured-data/article>

### WordPress

- WordPress Developer — WP_Query
  <https://developer.wordpress.org/reference/classes/wp_query/>
- WordPress Developer — Template hierarchy
  <https://developer.wordpress.org/themes/classic-themes/basics/template-hierarchy/>

### Oxygen 6.x

- Oxygen — Documentation générale
  <https://oxygenbuilder.com/documentation/>
- Oxygen — Connect Your Agent
  <https://oxygenbuilder.com/documentation/getting-started/connect-your-agent/>
- Oxygen — Components
  <https://oxygenbuilder.com/documentation/design/components/>
- Oxygen — Variables
  <https://oxygenbuilder.com/documentation/design/variables/>
- Oxygen — Classes
  <https://oxygenbuilder.com/documentation/design/classes/>
- Oxygen — Creating Templates
  <https://oxygenbuilder.com/documentation/templating/template-basics/>
- Oxygen — Applying Templates
  <https://oxygenbuilder.com/documentation/templating/applying-templates/>
- Oxygen — Headers
  <https://oxygenbuilder.com/documentation/templating/headers/>
- Oxygen — Footers
  <https://oxygenbuilder.com/documentation/templating/footers/>
- Oxygen — Template Content Area
  <https://oxygenbuilder.com/documentation/reference/elements/dynamic/template-content-area/>
- Oxygen — Post Loop Builder
  <https://oxygenbuilder.com/documentation/reference/elements/dynamic/post-loop-builder/>
- Oxygen — Loop Elements
  <https://oxygenbuilder.com/documentation/dynamic-data/loops/loop-elements/>
- Oxygen — Custom Query
  <https://oxygenbuilder.com/documentation/dynamic-data/loops/queries/custom-query/>
- Oxygen — Responsive Design
  <https://oxygenbuilder.com/documentation/builder/basics/responsive-design/>
- Oxygen — Working With Elements / semantic HTML tags
  <https://oxygenbuilder.com/documentation/builder/basics/working-with-elements/>

Ne jamais utiliser la documentation `classic.oxygenbuilder.com` pour décider d'une implémentation Oxygen 6.x, sauf comparaison/migration explicitement demandée.

Pour les capacités agent/MCP propres aux versions récentes :

- Oxygen — Oxygen 6.2 / MCP Edition
  <https://oxygenbuilder.com/oxygen-6-2-is-now-available/>
- Oxygen — Oxygen 6.2 Beta 6 / Raw Mode loops
  <https://oxygenbuilder.com/oxygen-6-2-beta-6/>

Toujours vérifier les abilities exposées par le serveur avant d'utiliser une capacité mentionnée dans une release 6.2.

### Yoast SEO

- Yoast Developer — REST API
  <https://developer.yoast.com/customization/apis/rest-api/>
- Yoast Developer — API Overview
  <https://developer.yoast.com/customization/apis/overview/>
- Yoast Developer — Schema
  <https://developer.yoast.com/features/schema/>
- Yoast Developer — Schema integration guidelines
  <https://developer.yoast.com/features/schema/integration-guidelines/>

---

## 25. Règle finale anti-bêtise

Avant de modifier le site, se demander :

```text
Est-ce que j'ai lu Figma et le WordPress actuel ?
Est-ce que j'utilise le bon MCP WordPress ?
Est-ce que les identifiants entreprise/projet sont confirmés et l'ERP a été consulté sans mutation ?
Est-ce que le domaine public final est confirmé avant Complianz et WP Mail SMTP ?
Est-ce que je suis bien sur Oxygen 6.x et sur la bonne version exacte ?
Est-ce que j'ai réutilisé l'existant avant de recréer ?
Est-ce qu'un élément Oxygen natif couvre le besoin avant le code custom ?
Est-ce que le rendu respecte Figma plutôt que mes goûts ?
Est-ce que le builder Oxygen restera éditable ?
Est-ce que l'éditeur a été rechargé depuis la dernière mutation externe ?
Est-ce que le contenu dynamique est réellement dynamique ?
Est-ce que tous les liens ont une destination réelle ?
Est-ce que téléphone/email sont cliquables ?
Est-ce que la correction locale a laissé les autres pages intactes ?
Est-ce que la page tient à 320 px sans casser ?
Est-ce que le H1 est unique ?
Est-ce que Yoast n'est pas doublonné ?
Est-ce que l'image LCP n'est pas lazy ?
Est-ce que les iframes/images réservent leur espace ?
Est-ce que Complianz, le formulaire, le CAPTCHA et l'envoi SMTP ont été testés réellement ?
Est-ce que les pages légales et le crédit Octacom sont présents dans le footer ?
Est-ce qu'une sauvegarde vérifiée permet de revenir en arrière ?
Est-ce que j'ai réellement regardé le rendu avant de dire terminé ?
```

Si une réponse importante est non : corriger avant livraison.
