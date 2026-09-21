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

Les hooks de `.codex/hooks.json` rappellent ce préflight au démarrage ou à la reprise d'une session, après compactage, à chaque prompt utilisateur et au démarrage de chaque sous-agent. Ils doivent être relus et approuvés avec `/hooks` dans un projet de confiance. Ces hooks injectent du contexte sans bloquer les actions. Aucun exécuteur strict, permis d'action, contrôle `PreToolUse` ou contrôle `Stop` n'est implémenté dans ce dépôt. Ils ne constituent donc pas une frontière de sécurité et ne couvrent pas nécessairement les outils hébergés ou certains chemins spécialisés. Ne jamais présenter leur présence comme une garantie absolue.

Quand ils sont disponibles, invoquer `caveman`, `unslop` et `frontend-design` sur chaque tour de conception, code ou correction visuelle. Ne jamais prétendre avoir utilisé un skill indisponible.

Utiliser les skills spécialisés suivants dès que leur description correspond :

| Besoin | Skill |
|---|---|
| Préflight, sélection et chargement des skills | `skill-gate` |
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

Combiner le minimum de skills métier qui couvre réellement la tâche, en plus de `skill-gate`. Une construction de site complète utilise normalement le démarrage, l'orchestration parallèle, Figma, l'architecture, le skill accueil ou pages internes, les spécialités applicables, puis la QA.

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

Le paquet de mission indique aussi les skills pressentis. Le sous-agent doit confirmer ou corriger cette sélection avec `skill-gate`, charger lui-même les instructions retenues et signaler les skills réellement appliqués dans son retour.

Utiliser `octacom-parallel-delivery` pour la procédure complète, les barrières de phase, les rôles spécialisés et le contrat de retour.

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

---

## 6. Invariants globaux de livraison

### Oxygen et styles

- Cibler le nouvel Oxygen 6.x, jamais Oxygen Classic sauf demande explicite.
- Détecter la version exacte et utiliser uniquement les abilities exposées.
- Préférer Variables, Classes, Selectors, States, Components, Dynamic Data, loops et Template Content Area.
- Lire une règle partagée entière et ses usages avant modification ; certains imports remplacent toute la règle du breakpoint.
- Ne pas reconstruire une page dans un gros bloc HTML/PHP ou avec JavaScript.

### Templates obligatoires

Tout site doit posséder avant livraison :

- un Template Oxygen 6 **Single Article**, appliqué aux articles WordPress, avec titre, date, image à la une, contenu et données dynamiques réelles ;
- un Template Oxygen 6 spécial **404 Not Found**, ciblé avec la Location Oxygen correspondante, qui conserve le Header, le Footer, un message clair et au moins un lien réel permettant de revenir vers une destination valide.

Ces deux templates font partie du socle global et ne sont jamais considérés comme hors périmètre. S'ils existent déjà, les auditer et les corriger au lieu de les dupliquer. Vérifier leurs Location, Conditions et Priority, leur rendu responsive, leur accessibilité, leur fonctionnement sans JavaScript et leur éditabilité dans Oxygen.

### Header

Le Header Oxygen est dédié, utilise le menu WordPress réel et reste sticky sur toutes les pages et tous les breakpoints. Mesurer sa hauteur réelle, compenser le premier contenu, maîtriser `top` et `z-index`, vérifier les ancêtres `overflow`, les ancres et le menu mobile accessible. Aucun contenu ne passe dessous.

### Footer et légal

Le Footer Oxygen est global et utilise le menu WordPress réel pour afficher :

- **Politique de protection des données**, titre strict, page générée avec Complianz puis éditée dans Oxygen pour y rendre exactement le shortcode `[cmplz-document type="cookie-statement" region="eu"]` ;
- **Mentions légales** ;
- **Conditions générales de vente** lorsqu'une page validée existe ou que le client confirme qu'elles s'appliquent.

Ne jamais inventer des CGV ni publier une page légale vide. Utiliser le template `templates/mentions-legales.html.tpl` avec des données confirmées. Configurer Complianz uniquement avec le domaine final et les services réellement présents. La page générée par Complianz est l'unique page **Politique de protection des données** : l'ouvrir ensuite dans Oxygen et intégrer une seule occurrence du shortcode exact dans un élément Oxygen capable de l'exécuter. Ne pas créer de page parallèle, recopier une politique statique ni laisser le shortcode visible comme texte brut.

Le crédit de réalisation Octacom est présent sur tous les sites, même absent de Figma, avec le markup et la variante rouge/blanche définis dans `oxygen6-architecture` selon le contraste du fond.

### Images et médias

Chaque image possède obligatoirement un attribut `alt` adapté : descriptif si informative, vide si décorative, nom pertinent pour un logo informatif. Aucun bourrage de mots-clés.

Convertir obligatoirement en WebP tout raster maîtrisé destiné à être affiché sur le site avant son import ou son utilisation. Ne livrer aucun JPEG, PNG ou GIF comme image de contenu. Seuls les formats techniques supplémentaires explicitement imposés par une plateforme peuvent rester dans ces formats, jamais les images affichées dans les pages. Conserver hors production les originaux nécessaires au travail source.

Utiliser au maximum des SVG pour les logos, icônes, pictogrammes, formes graphiques et illustrations réellement vectorielles. Réutiliser ou exporter le SVG source au lieu de rasteriser ces éléments. Optimiser et assainir chaque SVG avant usage ; ne jamais convertir artificiellement une photographie ou un raster en SVG.

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
- Séparer l'adresse affichée sur le site de l'identité technique d'envoi. Une adresse personnelle Gmail, Outlook ou équivalente peut être affichée si elle est validée, mais ne devient jamais le `From Email`, le Sender, l'envelope sender ni le destinataire direct configuré dans le formulaire. Le Reply-To saisi par un visiteur peut utiliser son adresse externe, car ce n'est pas l'expéditeur SMTP.
- Lors de tout test où le formulaire est rempli, saisir `support@octacom.fr` dans le champ email et utiliser uniquement des données manifestement fictives dans tous les autres champs, jamais les coordonnées ou informations du client. Avant chaque envoi de test, configurer temporairement `support@octacom.fr` comme unique adresse de réception et retirer tout destinataire, CC ou BCC client.
- Identifier clairement chaque soumission avec `TEST OCTACOM - NE PAS TRAITER`. Après les tests, configurer par défaut `contact@<FINAL_DOMAIN>` comme adresse de réception du formulaire et comme adresse d'expédition `From Email` de WP Mail SMTP. Utiliser une autre adresse seulement si une source projet prioritaire la fournit et la valide explicitement.
- Ne construire cette adresse qu'avec le domaine public final confirmé, jamais avec le domaine de préproduction. Vérifier que la boîte et l'expédition SMTP existent réellement ; sinon bloquer la livraison et demander les informations manquantes.
- Pour le dernier test de délivrabilité, garder `support@octacom.fr` comme destinataire unique et utiliser `contact@<FINAL_DOMAIN>` comme `From Email` afin de prouver l'expédition sans envoyer au client. Après réception, configurer aussi le destinataire sur `contact@<FINAL_DOMAIN>` et relire les réglages sans envoyer de test à cette adresse sauf demande explicite. Un message de succès front ne suffit pas.
- Lorsqu'une source projet indique `redirection vers <adresse>`, appliquer la convention Octacom : préparer WP Mail SMTP avec le fournisseur OVH et utiliser `contact@<FINAL_DOMAIN>` à la fois comme expéditeur et destinataire du formulaire. L'adresse indiquée après `redirection vers` reste uniquement la cible d'une redirection gérée dans la console OVH. Ne jamais la placer comme expéditeur ou destinataire direct dans WordPress.
- La création ou modification de la redirection dans la console OVH est hors périmètre. La signaler dans le rapport final sans intervenir dans la console. La mention `redirection vers` ne suffit pas à déduire l'offre, la région, le serveur, le port ou le chiffrement : les vérifier dans la documentation OVHcloud officielle correspondant à l'offre réelle. Si `contact@<FINAL_DOMAIN>` n'est pas une vraie boîte SMTP authentifiable, ou si l'offre OVH et les identifiants nécessaires ne sont pas confirmés, bloquer la configuration au lieu de deviner.

---

## 7. Accueil et pages internes : workflows distincts

### Page d'accueil

La home calibre le système : direction visuelle, rythmes, Header, Footer, hero, Components réutilisables, parcours et aperçus dynamiques. Son arbre a un propriétaire unique. Stabiliser les fondations et identifier clairement ce qui reste local avant d'ouvrir les pages internes en parallèle.

Ne pas créer à l'avance les autres pages ou archives hors périmètre. Le Template Single Article et le Template spécial 404 restent obligatoires dans le socle de chaque site.

### Pages internes

Une page interne consomme le socle validé. Elle part de ses propres sources métier et réutilise les objets adaptés sans copier toute la home. Ses layouts suivent la quantité de texte et le format réel des médias.

Après stabilisation du socle, plusieurs pages internes peuvent être construites en parallèle si chacune possède un propriétaire, un ID et des cibles distinctes. Aucun agent de page ne modifie seul un objet global.

---

## 8. Workflow de haut niveau

1. Exécuter le préflight `skill-gate`, puis cadrer le projet, consulter l'ERP en lecture seule et classer les sources.
2. Auditer WordPress, Oxygen, plugins, menus, médias et SEO.
3. Sauvegarder proportionnellement au risque.
4. Lire Figma, recenser toutes les annotations du périmètre, analyser leurs effets directs et indirects, résoudre les blocages, puis inventorier design, assets et interactions. Aucune implémentation Figma avant `FIGMA_ANNOTATIONS_REVIEWED`.
5. Planifier les objets Oxygen et les propriétaires d'écriture.
6. Construire les fondations globales avec un seul écrivain, y compris les Templates obligatoires Single Article et 404.
7. Construire et stabiliser la home si elle est dans le périmètre.
8. Construire les pages internes distinctes en parallèle.
9. Traiter contenus dynamiques, SEO, formulaires, SMTP, Complianz et légal avec leurs skills.
10. Geler les mutations, lancer la QA parallèle, intégrer les corrections, puis relancer les contrôles.
11. Refaire un préflight final, confirmer que tous les skills applicables ont été suivis et produire le rapport sans inventer les vérifications ou métriques absentes.

Après chaque bloc important : sauvegarder, ouvrir le front, vérifier le builder et recharger tout éditeur devenu périmé.

---

## 9. Fin de travail

Avant de déclarer terminé, utiliser `wordpress-oxygen-qa` et vérifier au minimum :

- contenu et médias exacts, aucun doublon ou placeholder ;
- toutes les annotations Figma recensées, appliquées et vérifiées avec leurs effets indirects ;
- Figma contrôlé dans le navigateur ;
- Header sticky et Footer global corrects ;
- Template Single Article et Template spécial 404 présents, correctement ciblés, éditables et testés ;
- menu légal, Complianz, shortcode `[cmplz-document type="cookie-statement" region="eu"]` rendu depuis Oxygen, crédit Octacom et CGV applicables ;
- Oxygen éditable après rechargement ;
- responsive, largeurs intermédiaires et absence d'overflow ;
- contenu, navigation et actions utilisables sans JavaScript ;
- alt, focus, clavier, hover/tactile et reduced motion ;
- liens, téléphone, email, CTA et permaliens ;
- contenu dynamique, cas zéro/un/plusieurs ;
- H1/Hn, title, description, canonical, Yoast et Schema applicables ;
- performance des images, LCP, CLS et widgets ;
- rasters convertis en WebP avant usage et SVG utilisés au maximum pour les formes et illustrations vectorielles ;
- formulaire, réception SMTP, CAPTCHA et consentement ;
- tests de formulaire reçus sur `support@octacom.fr` avec données fictives, puis destinataire et `From Email` rétablis par défaut sur `contact@<FINAL_DOMAIN>` avant livraison ;
- aucun expéditeur Gmail/Outlook ou domaine tiers ; branche `redirection vers` configurée avec SMTP OVH et redirection console signalée hors périmètre ;
- sauvegarde et chemin de retour vérifiés.

Le rapport final distingue ce qui est implémenté, réutilisable, dynamique, réellement testé et non vérifié. Pour un développement complet, ajouter le détail temps/tokens/coût par modèle uniquement depuis les journaux accessibles ; ne jamais estimer une métrique absente.

---

## 10. Traçabilité de la migration

La version intégrale antérieure au découpage est conservée dans `docs/AGENTS.pre-skills-snapshot.md`, SHA-256 `ED720A6CC4906EC5D2D607BFA9BF0C684038F96D167AEA74B6794D3C4DAC1B5F`.

La matrice `docs/agents-skill-traceability.md` associe chaque ancienne section à sa destination active. Le snapshot sert à l'audit de non-perte, pas à la lecture normale : utiliser les skills et leurs références ciblées.
