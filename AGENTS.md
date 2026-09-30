# AGENTS.md — WordPress + Oxygen 6.x avec Codex

Guide racine générique pour développer des sites WordPress depuis Figma avec un MCP WordPress, le MCP Figma et, lorsqu'il est disponible, Yoast SEO.

Objectif : produire des pages fidèles, éditables dans Oxygen 6.x, réutilisables, responsive, performantes, accessibles et propres pour le SEO, sans inventer de contenu ni transformer Figma en une accumulation de positions absolues.

Les procédures détaillées vivent dans les skills repo-scoped de `.agents/skills/`. Ce fichier conserve seulement les règles qui doivent influencer presque tous les travaux.

---

## 1. Paramètres projet

Ne jamais hard-coder un client ni le domaine public final d'un projet dans ce guide. Les URLs fixes de l'infrastructure et des assets officiels Octacom documentés ici, notamment les modèles d'URL ERP et le logo du crédit de réalisation, sont autorisées.

```text
SITE_URL=<url du site>
FINAL_DOMAIN=<domaine public final>
WORDPRESS_MCP=<serveur MCP WordPress du projet>
FIGMA_URL=<url Figma node-specific>
COMPANY_ID=<identifiant entreprise Octacom>
PROJECT_ID=<identifiant projet Octacom>
BUILDER=Oxygen 6.x
SEO_CONNECTOR=Yoast SEO si disponible
LANG=fr-FR sauf consigne contraire
```

Règles permanentes :

- utiliser uniquement le MCP WordPress correspondant au site courant ;
- inspecter les outils exposés avant de nommer ou appeler une capacité ;
- résoudre IDs, slugs, catégories, templates, menus et médias depuis le site avant d'écrire ;
- demander ou retrouver `COMPANY_ID` et `PROJECT_ID` dès le début ;
- consulter l'ERP Octacom en lecture seule et ne jamais y modifier l'entreprise ou le projet sans demande explicite ;
- construire les URLs ERP seulement avec les identifiants confirmés :

```text
https://base.octacom.fr/entreprises/<COMPANY_ID>
https://base.octacom.fr/entreprises/<COMPANY_ID>/projet/<PROJECT_ID>
```

- demander le domaine public final avant Complianz, WP Mail SMTP, cookies, URLs absolues, expéditeurs et redirections ; ne pas le déduire de la préproduction ;
- ne jamais inscrire mot de passe, clé CAPTCHA, clé SMTP, licence ou secret dans ce guide, un rapport, un journal ou un prompt de sous-agent.

Documentation interne : [Développement WordPress Octacom](https://app.notion.com/p/octacom/Dev-Wordpress-f6510f445ce44dad95d5c81e5c193540). La consulter lorsqu'elle est accessible pour les procédures Octacom, sans lui faire remplacer les sources métier du projet.

---

## 2. Priorité des sources

En cas de conflit :

1. dernière instruction explicite de l'utilisateur ;
2. documents métier et contenus validés pour textes, horaires, prix, coordonnées et données légales ;
3. données vérifiées dans WordPress ou l'ERP consulté en lecture seule ;
4. Figma pour le design et la disposition, et pour le contenu seulement si le projet le désigne comme source éditoriale ;
5. ce guide et les skills du dépôt ;
6. documentation officielle de l'outil.

Pour le design : dernière correction visuelle, puis Figma avec lecture obligatoire de toutes les annotations du périmètre, puis `frontend-design`, puis l'existant compatible, puis les règles génériques. L'impossibilité d'accéder aux annotations bloque toute implémentation Figma dépendante.

Dans l'analyse d'un périmètre Figma, appliquer cet ordre interne : instruction explicite de la tâche, annotations Figma, structure et propriétés réelles des nodes/components, rendu visuel, puis interprétation personnelle. Une annotation explicite prévaut sur une lecture fondée uniquement sur l'apparence.

Si deux sources du même niveau se contredisent, signaler le conflit et demander laquelle fait foi avant publication. Ne jamais choisir silencieusement.

### Information requise introuvable : blocage

Une information est requise lorsqu'elle conditionne la justesse, la destination, le contenu, la conformité, la sécurité ou le comportement d'une implémentation.

La chercher dans les sources autorisées selon leur ordre de priorité. Si elle reste introuvable, ambiguë ou contradictoire, ne pas la déduire, la compléter, la remplacer par un placeholder ni choisir silencieusement une source.

C'est un blocage. Avant toute écriture ou configuration dépendante, expliquer précisément l'information manquante, les sources vérifiées, l'objet affecté et la décision attendue, puis demander une instruction explicite à l'utilisateur. Ne pas poursuivre l'implémentation affectée avant sa réponse.

Seuls les travaux indépendants en lecture seule peuvent continuer : audit, inventaire, nouvelle vérification des sources, cartographie des impacts et préparation d'options clairement non retenues. Aucune mutation ne peut contourner le blocage ou préparer un état publiable fondé sur une hypothèse.

---

## 3. Préflight des skills et routeur

Avant toute unité d'exécution observable, utiliser `skill-gate` lorsqu'il est disponible. Une unité d'exécution est une séquence cohérente d'actions de bas niveau qui conserve le même objectif, les mêmes cibles, les mêmes permissions et les mêmes skills applicables. Elle peut couvrir plusieurs lectures ou contrôles liés ; elle ne couvre jamais un changement de périmètre ou de cible.

Le préflight est obligatoire avant la première lecture par outil, mutation, délégation, action externe ou réponse finale de l'unité. Le refaire dès que l'objectif, la cible, la classe d'action, les permissions, le propriétaire d'écriture ou les skills applicables changent.

Pendant ce préflight :

- partir uniquement du catalogue de skills réellement disponible et ne jamais inventer un nom ;
- sélectionner `skill-gate`, puis le minimum de skills métier qui couvre toute l'unité ;
- lire intégralement chaque `SKILL.md` sélectionné et les références qu'il rend obligatoires avant d'agir ;
- si aucun skill métier ne s'applique, conserver `skill-gate` seul au lieu de prétendre qu'aucun contrôle n'est nécessaire ;
- distinguer le routage des skills de l'autorisation : un skill explique comment travailler, mais n'élargit jamais le périmètre demandé ni les permissions ;
- annoncer dans le canal de suivi les skills utilisés et la raison, conformément aux règles de session ;
- traiter une information requise manquante, une cible non confirmée ou une capacité absente comme un blocage selon la section 2.

Chaque sous-agent refait son propre préflight. La sélection suggérée par le coordinateur dans le paquet de mission est une entrée à vérifier, pas une autorisation automatique.

Pour toute demande qui exige l'état réel d'un dépôt, d'un site ou d'une source externe, utiliser les outils Codex ou MCP pertinents après lecture des skills applicables. Une réponse fondée sur une supposition ou la seule lecture d'un skill ne vaut pas vérification. Si l'outil requis manque, signaler le blocage précis.

Les hooks de `.codex/hooks.json` rappellent le préflight. Sur les demandes d'action reconnues, `UserPromptSubmit`, `PostToolUse` et `Stop` relancent une fois un tour terminé sans appel d'outil local observé. Ce contrôle ne prouve ni le choix du bon outil ni l'application d'un skill ; les outils hébergés et certains chemins spécialisés échappent aux hooks. Relire et approuver ces hooks avec `/hooks` dans un projet de confiance. Aucun exécuteur strict ni permis d'action n'est fourni.

Quand ils sont disponibles, invoquer `caveman`, `unslop` et `frontend-design` sur chaque tour de conception, code ou correction visuelle. Ne jamais prétendre avoir utilisé un skill indisponible.

Utiliser les skills spécialisés suivants dès que leur description correspond :

| Besoin                                                     | Skill                              |
| ---------------------------------------------------------- | ---------------------------------- |
| Préflight, sélection et chargement des skills            | `skill-gate`                     |
| Cadrage, ERP, audit et sauvegarde                          | `octacom-project-start`          |
| Orchestration intensive et sûre des sous-agents           | `octacom-parallel-delivery`      |
| Lecture et traduction de Figma                             | `figma-to-oxygen`                |
| Fondations et objets globaux Oxygen 6                      | `oxygen6-architecture`           |
| Page d'accueil                                             | `oxygen6-homepage`               |
| Pages internes                                             | `oxygen6-inner-pages`            |
| Responsive, images, accessibilité, performance et sans-JS | `oxygen6-frontend-quality`       |
| Loops, articles et contenus WordPress                      | `wordpress-dynamic-content`      |
| SEO et Yoast                                               | `wordpress-seo`                  |
| Formulaires, CAPTCHA et WP Mail SMTP                       | `wordpress-forms-deliverability` |
| Pages légales et Complianz                                | `wordpress-legal-consent`        |
| Recette et rapport final                                   | `wordpress-oxygen-qa`            |

Combiner le minimum de skills métier qui couvre réellement la tâche, en plus de `skill-gate`. Une construction de site complète utilise normalement le démarrage, l'orchestration parallèle, Figma, l'architecture, le skill accueil ou pages internes, les spécialités applicables, puis la QA.

Les instructions d'un skill priment dans son domaine, sauf que la dernière instruction utilisateur et les sources métier restent supérieures ; Figma reste la vérité visuelle selon l'ordre précédent.

---

## 4. Sous-agents : usage intensif mais sûr

Pour tout travail non trivial avec sous-agents disponibles, utiliser `octacom-parallel-delivery` : il fixe le choix du plus petit modèle capable, les missions disjointes, les barrières de phase et les preuves de retour. Chaque objet mutable garde un propriétaire unique ; les agents de page remontent les besoins globaux au coordinateur. Sans cible confirmée, déléguer seulement en lecture seule. Chaque sous-agent refait `skill-gate`, et le coordinateur vérifie l'état réel avant de conclure.

---

## 5. Principes non négociables

1. **Lire avant d'écrire.** Auditer le site, Figma, les sources et les composants existants.
2. **Ne rien inventer.** Aucun téléphone, email, horaire, prix, adresse, certification, témoignage, URL, image, texte métier ou donnée SEO factuelle.
3. **Une donnée requise manquante bloque.** Demander l'information à l'utilisateur et suspendre toute implémentation qui en dépend.
4. **Annotations Figma avant implémentation.** Lire toutes les annotations du périmètre, leurs cibles et leurs effets indirects. Une annotation inaccessible ou non résolue bloque toute écriture dépendante.
5. **Préserver le contenu validé.** Ne pas reformuler textes, avis, horaires, tarifs ou mentions légales sans demande.
6. **Respecter le périmètre.** Une demande sur la home n'autorise pas la refonte des autres pages.
7. **Une correction locale reste locale.** Aucun sélecteur global large pour résoudre un cas ponctuel.
8. **Oxygen 6.x reste éditable.** Un front fidèle mais cassé dans le builder est refusé.
9. **Oxygen natif d'abord.** Élément natif, Component existant, composition Oxygen, puis code custom ciblé en dernier recours avec HTML sémantique et WAI-ARIA applicable.
10. **Réutiliser avant de dupliquer.** Components, Classes, Selectors, Variables, Templates, Header, Footer, menus et loops sont factorisés à bon escient.
11. **Données WordPress réellement dynamiques.** Articles, titres, dates, images, permaliens et catégories ne sont pas copiés à la main.
12. **Navigation réelle.** Un déplacement utilise `<a href>` ; un bouton sert une action. Aucun `#`, `javascript:void(0)` ou URL de développement involontaire.
13. **HTML/CSS/Oxygen avant JavaScript.** Ne pas ajouter une dépendance ou un plugin sans besoin réel.
14. **Contenu visible sans JavaScript.** Contenu éditorial, navigation et actions essentielles restent clairs et utilisables si le script est bloqué ou échoue.
15. **Un seul état d'édition fait foi.** Après une mutation MCP ou externe, recharger Oxygen avant toute sauvegarde depuis un éditeur déjà ouvert.
16. **Sauvegarder selon le risque.** Lire l'état et préparer un retour arrière vérifié avant une mutation importante.
17. **Tester réellement.** Ne jamais annoncer fidélité, responsive, SEO, réception email ou conformité sans contrôle correspondant.
18. **Single Article et 404 toujours présents.** Tout site livré possède un Template Oxygen 6 pour les articles et un Template Oxygen 6 spécial `404 Not Found`, même si la mission initiale porte sur la home ou si aucun article n'est encore publié. Auditer et réutiliser les templates conformes existants ; ne jamais créer de doublon.
19. **Expéditeur email sur domaine client uniquement.** Le `From Email`, le Sender et l'envelope sender des formulaires utilisent toujours une adresse d'un domaine personnalisé appartenant au client et correctement authentifié. Gmail, Outlook, Hotmail, Yahoo et tout autre domaine grand public ou tiers sont interdits comme expéditeurs, même lorsqu'ils sont affichés publiquement comme contact du client.
20. **Animations d'apparition obligatoires.** Toute page construite ou refondue possède un système cohérent d'animations d'apparition sur ses principaux blocs. Cette obligation s'applique même lorsque la charte, Figma ou les annotations ne prévoient aucune animation. Leur absence ou leur validation incomplète bloque la livraison. Utiliser d'abord l'onglet Animations natif d'Oxygen 6. Reprendre les paramètres Figma lorsqu'ils existent. Si aucune source visuelle ne fixe le mouvement, définir un système sobre. La réduction ou la désactivation demandée par `prefers-reduced-motion` reste obligatoire et ne constitue pas un échec de ce critère.

---

## 6. Invariants globaux de livraison

### Oxygen et styles

- Cibler le nouvel Oxygen 6.x, jamais Oxygen Classic sauf demande explicite.
- Détecter la version exacte et utiliser uniquement les abilities exposées.
- Pour les objets partagés, l'éditabilité et les styles, suivre `oxygen6-architecture` ; lire la règle entière et ses usages avant modification.

### Templates obligatoires

Le Single Article et le 404 imposés en section 5 appartiennent au socle global. Suivre `oxygen6-architecture` pour leurs données dynamiques, Location, Conditions, Priority et contrôles front/builder ; réutiliser les templates conformes existants.

### Header

Le Header Oxygen dédié utilise le menu WordPress réel et reste sticky à tous les breakpoints sans masquer le contenu. Suivre `oxygen6-frontend-quality` pour hauteur, ancres, empilement et menu mobile.

### Footer et légal

Le Footer Oxygen global utilise le menu WordPress réel pour **Politique de protection des données**, **Mentions légales** et les **Conditions générales de vente** seulement si elles sont validées ou applicables selon le client. L'unique page de politique vient de Complianz et exécute dans Oxygen une seule occurrence de `[cmplz-document type="cookie-statement" region="eu"]`. Ne jamais inventer de données légales. Suivre `wordpress-legal-consent` pour la procédure et `oxygen6-architecture` pour le crédit Octacom obligatoire, même absent de Figma.

### Images et médias

Chaque image a un `alt` adapté. Convertir tout raster maîtrisé affiché en WebP avant import et utiliser le SVG source optimisé pour les vrais vecteurs ; ne pas vectoriser un raster. Préserver ratio et cadrage. Suivre `figma-to-oxygen` et `oxygen6-frontend-quality` pour les médias, LCP et performance.

### Interactions et accessibilité

- Aucune information essentielle uniquement au hover, en image, par couleur ou dans un pseudo-élément.
- Prévoir clavier, focus visible, tactile, ordre DOM logique, labels et noms accessibles.
- L'état par défaut d'un élément animé est visible. Appliquer l'état initial masqué seulement après initialisation réussie.
- Respecter `prefers-reduced-motion` et tester la page JavaScript désactivé.

### Liens et formulaires

Les liens ont une destination réelle. Pour un formulaire, charger `wordpress-forms-deliverability` avant toute configuration ou test : il fixe l'identité d'envoi sur le domaine final confirmé, l'unique destinataire de test `support@octacom.fr`, les données fictives, le retour à `contact@<FINAL_DOMAIN>` et la branche OVH `redirection vers`. Ne jamais tester vers le client ni déduire les paramètres SMTP. La redirection dans la console OVH reste hors périmètre.

---

## 7. Accueil et pages internes : workflows distincts

La home calibre le socle partagé ; utiliser `oxygen6-homepage` pour la construire sans anticiper les pages hors périmètre. Une page interne consomme ce socle ; utiliser `oxygen6-inner-pages` et ses propres sources métier. N'ouvrir plusieurs pages en parallèle qu'après stabilisation du socle, avec un propriétaire et un ID distincts par page. Les Templates Single Article et 404 restent obligatoires pour le site.

---

## 8. Workflow de haut niveau

1. Préflight `skill-gate`, puis `octacom-project-start` pour sources, ERP en lecture seule, audit et sauvegarde.
2. `figma-to-oxygen` pour lire toutes les annotations du périmètre ; aucune écriture dépendante avant `FIGMA_ANNOTATIONS_REVIEWED`.
3. `octacom-parallel-delivery` pour les propriétaires et barrières ; `oxygen6-architecture` pour le socle global, puis les skills des pages et spécialités réellement concernés.
4. Geler les mutations et appliquer `wordpress-oxygen-qa` ; corriger puis revérifier. Après chaque bloc majeur, contrôler le front et le builder et recharger tout éditeur périmé.

---

## 9. Fin de travail

Avant de déclarer le site terminé, charger `wordpress-oxygen-qa` et exécuter sa définition de fin et son contrôle final, y compris annotations Figma, Templates Single Article/404, front/builder, responsive, sans-JS, animations, médias, SEO, formulaire/SMTP, légal et retour arrière. Le rapport distingue implémenté, réutilisable, dynamique, testé et non vérifié. Pour un développement complet, détailler temps/tokens/coût par modèle seulement depuis les journaux accessibles ; ne jamais estimer une métrique absente.

---

## 10. Traçabilité de la migration

La version intégrale antérieure au découpage est conservée dans `docs/AGENTS.pre-skills-snapshot.md`, SHA-256 `ED720A6CC4906EC5D2D607BFA9BF0C684038F96D167AEA74B6794D3C4DAC1B5F`.

La matrice `docs/agents-skill-traceability.md` associe chaque ancienne section à sa destination active. Le snapshot sert à l'audit de non-perte, pas à la lecture normale : utiliser les skills et leurs références ciblées.
