# AGENTS.md — WordPress + Oxygen 6.x avec Codex

Guide racine générique pour développer des sites WordPress depuis Figma avec un MCP WordPress, le MCP Figma et, lorsqu'il est disponible, Yoast SEO.

Objectif : produire des pages fidèles, éditables dans Oxygen 6.x, réutilisables, responsive, performantes, accessibles et propres pour le SEO, sans inventer de contenu ni transformer Figma en une accumulation de positions absolues.

Les procédures détaillées vivent dans les skills repo-scoped de `.agents/skills/`. Ce fichier conserve seulement les règles qui doivent influencer presque tous les travaux.

---

## 1. Paramètres projet

Ne jamais hard-coder un client ou un domaine dans ce guide.

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

Pour le design : dernière correction visuelle, puis Figma et ses annotations/commentaires accessibles, puis `frontend-design`, puis l'existant compatible, puis les règles génériques.

Si deux sources du même niveau se contredisent, signaler le conflit et demander laquelle fait foi avant publication. Ne jamais choisir silencieusement.

### Information requise introuvable : blocage

Une information est requise lorsqu'elle conditionne la justesse, la destination, le contenu, la conformité, la sécurité ou le comportement d'une implémentation.

La chercher dans les sources autorisées selon leur ordre de priorité. Si elle reste introuvable, ambiguë ou contradictoire, ne pas la déduire, la compléter, la remplacer par un placeholder ni choisir silencieusement une source.

C'est un blocage. Avant toute écriture ou configuration dépendante, expliquer précisément l'information manquante, les sources vérifiées, l'objet affecté et la décision attendue, puis demander une instruction explicite à l'utilisateur. Ne pas poursuivre l'implémentation affectée avant sa réponse.

Seuls les travaux indépendants en lecture seule peuvent continuer : audit, inventaire, nouvelle vérification des sources, cartographie des impacts et préparation d'options clairement non retenues. Aucune mutation ne peut contourner le blocage ou préparer un état publiable fondé sur une hypothèse.

---

## 3. Skills obligatoires et routeur

Quand ils sont disponibles, invoquer `caveman`, `unslop` et `frontend-design` sur chaque tour de conception, code ou correction visuelle. Ne jamais prétendre avoir utilisé un skill indisponible.

Utiliser les skills spécialisés suivants dès que leur description correspond :

| Besoin | Skill |
|---|---|
| Cadrage, ERP, audit et sauvegarde | `octacom-project-start` |
| Orchestration intensive et sûre des sous-agents | `octacom-parallel-delivery` |
| Lecture et traduction de Figma | `figma-to-oxygen` |
| Fondations et objets globaux Oxygen 6 | `oxygen6-architecture` |
| Page d'accueil | `oxygen6-homepage` |
| Pages internes | `oxygen6-inner-pages` |
| Responsive, images, accessibilité, performance et sans-JS | `oxygen6-frontend-quality` |
| Loops, articles et contenus WordPress | `wordpress-dynamic-content` |
| SEO et Yoast | `wordpress-seo` |
| Formulaires, CAPTCHA et WP Mail SMTP | `wordpress-forms-deliverability` |
| Pages légales et Complianz | `wordpress-legal-consent` |
| Recette et rapport final | `wordpress-oxygen-qa` |

Combiner le minimum de skills qui couvre réellement la tâche. Une construction de site complète utilise normalement le démarrage, l'orchestration parallèle, Figma, l'architecture, le skill accueil ou pages internes, les spécialités applicables, puis la QA.

Les instructions d'un skill priment dans son domaine, sauf que la dernière instruction utilisateur et les sources métier restent supérieures ; Figma reste la vérité visuelle selon l'ordre précédent.

---

## 4. Sous-agents : usage intensif mais sûr

Quand les sous-agents sont disponibles, les utiliser par défaut sur tout travail non trivial. Occuper les créneaux avec des missions indépendantes et spécialisées, puis réaffecter un agent terminé à la prochaine vérification utile.

### Choisir un modèle adapté

Lorsque l'outil de délégation permet de choisir le modèle, le faire explicitement. Sélectionner d'abord les capacités obligatoires, par exemple vision, code, outils, taille de contexte ou raisonnement. Parmi les modèles qui les possèdent, choisir le plus petit et le plus rapide qui peut satisfaire les critères d'acceptation. Le coût et la latence départagent seulement des modèles déjà capables de produire la qualité requise.

- Tâche simple et vérifiable, comme extraction, inventaire, contrôle de liens ou génération d'alts depuis des images accessibles : modèle compact et rapide.
- Génération d'alts ou contrôle visuel : modèle compatible vision obligatoire. Un modèle frontier n'est pas nécessaire pour une description factuelle simple.
- Architecture partagée, synthèse multi-source ambiguë, diagnostic complexe, arbitrage de conflits ou mutation à fort rayon d'impact : modèle avec raisonnement plus robuste.
- Capacité requise indisponible, image inaccessible ou contexte indispensable manquant : blocage et question à l'utilisateur, jamais de remplacement par une supposition.

### Paralléliser

- recherches et audits en lecture seule ;
- ERP/sources, WordPress/Oxygen, Figma/assets, contenus/liens, SEO, légal, formulaires et performance ;
- spécifications indépendantes ;
- pages internes différentes après stabilisation du socle ;
- QA finale par spécialité, sans écriture pendant la passe d'observation.

### Sérialiser

- le même fichier, la même page ou le même arbre Oxygen ;
- Header, Footer, Templates, Components, Variables, Classes et Selectors partagés ;
- menus, options WordPress, Complianz et WP Mail SMTP ;
- toute intégration ou correction qui affecte plusieurs consommateurs.

Un objet mutable a un propriétaire unique. Séparer les cibles avant de paralléliser ; une consigne « faites attention » ne protège pas un état partagé. Les agents de page signalent un besoin global au coordinateur au lieu de modifier le socle.

Chaque mission déléguée précise objectif, capacités requises, modèle choisi et justification, sources, objets lisibles, cible d'écriture exacte, IDs, objets interdits, informations bloquantes, critères d'acceptation et preuves attendues. Sans cible confirmée, elle reste en lecture seule et remonte le blocage. Le coordinateur relit l'état réel : « terminé » n'est jamais une preuve.

Utiliser `octacom-parallel-delivery` pour la procédure complète, les barrières de phase, les rôles spécialisés et le contrat de retour.

---

## 5. Principes non négociables

1. **Lire avant d'écrire.** Auditer le site, Figma, les sources et les composants existants.
2. **Ne rien inventer.** Aucun téléphone, email, horaire, prix, adresse, certification, témoignage, URL, image, texte métier ou donnée SEO factuelle.
3. **Une donnée requise manquante bloque.** Demander l'information à l'utilisateur et suspendre toute implémentation qui en dépend.
4. **Préserver le contenu validé.** Ne pas reformuler textes, avis, horaires, tarifs ou mentions légales sans demande.
5. **Respecter le périmètre.** Une demande sur la home n'autorise pas la refonte des autres pages.
6. **Une correction locale reste locale.** Aucun sélecteur global large pour résoudre un cas ponctuel.
7. **Oxygen 6.x reste éditable.** Un front fidèle mais cassé dans le builder est refusé.
8. **Oxygen natif d'abord.** Élément natif, Component existant, composition Oxygen, puis code custom ciblé en dernier recours avec HTML sémantique et WAI-ARIA applicable.
9. **Réutiliser avant de dupliquer.** Components, Classes, Selectors, Variables, Templates, Header, Footer, menus et loops sont factorisés à bon escient.
10. **Données WordPress réellement dynamiques.** Articles, titres, dates, images, permaliens et catégories ne sont pas copiés à la main.
11. **Navigation réelle.** Un déplacement utilise `<a href>` ; un bouton sert une action. Aucun `#`, `javascript:void(0)` ou URL de développement involontaire.
12. **HTML/CSS/Oxygen avant JavaScript.** Ne pas ajouter une dépendance ou un plugin sans besoin réel.
13. **Contenu visible sans JavaScript.** Contenu éditorial, navigation et actions essentielles restent clairs et utilisables si le script est bloqué ou échoue.
14. **Un seul état d'édition fait foi.** Après une mutation MCP ou externe, recharger Oxygen avant toute sauvegarde depuis un éditeur déjà ouvert.
15. **Sauvegarder selon le risque.** Lire l'état et préparer un retour arrière vérifié avant une mutation importante.
16. **Tester réellement.** Ne jamais annoncer fidélité, responsive, SEO, réception email ou conformité sans contrôle correspondant.

---

## 6. Invariants globaux de livraison

### Oxygen et styles

- Cibler le nouvel Oxygen 6.x, jamais Oxygen Classic sauf demande explicite.
- Détecter la version exacte et utiliser uniquement les abilities exposées.
- Préférer Variables, Classes, Selectors, States, Components, Dynamic Data, loops et Template Content Area.
- Lire une règle partagée entière et ses usages avant modification ; certains imports remplacent toute la règle du breakpoint.
- Ne pas reconstruire une page dans un gros bloc HTML/PHP ou avec JavaScript.

### Header

Le Header Oxygen est dédié, utilise le menu WordPress réel et reste sticky sur toutes les pages et tous les breakpoints. Mesurer sa hauteur réelle, compenser le premier contenu, maîtriser `top` et `z-index`, vérifier les ancêtres `overflow`, les ancres et le menu mobile accessible. Aucun contenu ne passe dessous.

### Footer et légal

Le Footer Oxygen est global et utilise le menu WordPress réel pour afficher :

- **Politique de protection des données**, titre strict, page générée/gérée avec Complianz ;
- **Mentions légales** ;
- **Conditions générales de vente** lorsqu'une page validée existe ou que le client confirme qu'elles s'appliquent.

Ne jamais inventer des CGV ni publier une page légale vide. Utiliser le template `templates/mentions-legales.html.tpl` avec des données confirmées. Configurer Complianz uniquement avec le domaine final et les services réellement présents.

Le crédit de réalisation Octacom est présent sur tous les sites, même absent de Figma, avec le markup et la variante rouge/blanche définis dans `oxygen6-architecture` selon le contraste du fond.

### Images et médias

Chaque image possède obligatoirement un attribut `alt` adapté : descriptif si informative, vide si décorative, nom pertinent pour un logo informatif. Aucun bourrage de mots-clés.

Préserver ratio, cadrage, dimensions ou espace réservé. Utiliser `contain` pour les médias qui ne doivent pas être coupés et `cover` uniquement pour les recadrages voulus. L'image LCP n'est pas lazy ; les médias sous le fold le sont lorsque pertinent.

### Interactions et accessibilité

- Aucune information essentielle uniquement au hover, en image, par couleur ou dans un pseudo-élément.
- Prévoir clavier, focus visible, tactile, ordre DOM logique, labels et noms accessibles.
- L'état par défaut d'un élément animé est visible. Appliquer l'état initial masqué seulement après initialisation réussie.
- Respecter `prefers-reduced-motion` et tester la page JavaScript désactivé.

### Liens et formulaires

- Liens HTTP externes : nouvel onglet avec `rel="noopener noreferrer"` ; liens internes : même onglet ; `tel:` et `mailto:` directs.
- Utiliser le Form Oxygen ou le composant validé avant une version manuelle.
- Confirmer destination, expéditeur, consentement, CAPTCHA et domaine final.
- Configurer WP Mail SMTP avec les données validées et prouver la réception réelle ; un message de succès front ne suffit pas.

---

## 7. Accueil et pages internes : workflows distincts

### Page d'accueil

La home calibre le système : direction visuelle, rythmes, Header, Footer, hero, Components réutilisables, parcours et aperçus dynamiques. Son arbre a un propriétaire unique. Stabiliser les fondations et identifier clairement ce qui reste local avant d'ouvrir les pages internes en parallèle.

Ne pas créer à l'avance les pages, archives, singles ou 404 hors périmètre.

### Pages internes

Une page interne consomme le socle validé. Elle part de ses propres sources métier et réutilise les objets adaptés sans copier toute la home. Ses layouts suivent la quantité de texte et le format réel des médias.

Après stabilisation du socle, plusieurs pages internes peuvent être construites en parallèle si chacune possède un propriétaire, un ID et des cibles distinctes. Aucun agent de page ne modifie seul un objet global.

---

## 8. Workflow de haut niveau

1. Cadrer le projet, consulter l'ERP en lecture seule et classer les sources.
2. Auditer WordPress, Oxygen, plugins, menus, médias et SEO.
3. Sauvegarder proportionnellement au risque.
4. Lire Figma et inventorier design, assets et interactions.
5. Planifier les objets Oxygen et les propriétaires d'écriture.
6. Construire les fondations globales avec un seul écrivain.
7. Construire et stabiliser la home si elle est dans le périmètre.
8. Construire les pages internes distinctes en parallèle.
9. Traiter contenus dynamiques, SEO, formulaires, SMTP, Complianz et légal avec leurs skills.
10. Geler les mutations, lancer la QA parallèle, intégrer les corrections, puis relancer les contrôles.

Après chaque bloc important : sauvegarder, ouvrir le front, vérifier le builder et recharger tout éditeur devenu périmé.

---

## 9. Fin de travail

Avant de déclarer terminé, utiliser `wordpress-oxygen-qa` et vérifier au minimum :

- contenu et médias exacts, aucun doublon ou placeholder ;
- Figma contrôlé dans le navigateur ;
- Header sticky et Footer global corrects ;
- menu légal, Complianz, crédit Octacom et CGV applicables ;
- Oxygen éditable après rechargement ;
- responsive, largeurs intermédiaires et absence d'overflow ;
- contenu, navigation et actions utilisables sans JavaScript ;
- alt, focus, clavier, hover/tactile et reduced motion ;
- liens, téléphone, email, CTA et permaliens ;
- contenu dynamique, cas zéro/un/plusieurs ;
- H1/Hn, title, description, canonical, Yoast et Schema applicables ;
- performance des images, LCP, CLS et widgets ;
- formulaire, réception SMTP, CAPTCHA et consentement ;
- sauvegarde et chemin de retour vérifiés.

Le rapport final distingue ce qui est implémenté, réutilisable, dynamique, réellement testé et non vérifié. Pour un développement complet, ajouter le détail temps/tokens/coût par modèle uniquement depuis les journaux accessibles ; ne jamais estimer une métrique absente.

---

## 10. Traçabilité de la migration

La version intégrale antérieure au découpage est conservée dans `docs/AGENTS.pre-skills-snapshot.md`, SHA-256 `ED720A6CC4906EC5D2D607BFA9BF0C684038F96D167AEA74B6794D3C4DAC1B5F`.

La matrice `docs/agents-skill-traceability.md` associe chaque ancienne section à sa destination active. Le snapshot sert à l'audit de non-perte, pas à la lecture normale : utiliser les skills et leurs références ciblées.
