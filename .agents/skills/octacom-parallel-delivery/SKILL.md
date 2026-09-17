---
name: octacom-parallel-delivery
description: "Orchestrer intensivement des sous-agents sur un projet WordPress/Oxygen comportant plusieurs sources, pages, spécialités ou contrôles, tout en empêchant les conflits d'écriture sur les objets partagés."
---

# Livraison parallèle WordPress/Oxygen

Utiliser les sous-agents par défaut sur tout travail non trivial. Occuper les créneaux disponibles avec des tâches indépendantes, puis réaffecter rapidement les agents terminés. La vitesse vient de la séparation des responsabilités, jamais de plusieurs écrivains sur le même état.

Le coordinateur principal conserve la vue d'ensemble, les priorités, l'attribution des objets, les décisions transversales, l'intégration et la validation finale.

## Règle centrale

Séparer avant de paralléliser. Attribuer un propriétaire exclusif à chaque état mutable : page, arbre Oxygen, Header, Footer, Template, Component, Variable, classe, Selector, menu, catégorie, média, réglage WordPress, Complianz, WP Mail SMTP, formulaire ou fichier.

Deux agents écrivent en parallèle seulement si leurs cibles sont réellement distinctes. Les conventions verbales ne constituent pas un verrou.

## Choisir le modèle du sous-agent

Lorsque l'outil permet un choix de modèle, sélectionner d'abord les capacités requises par la mission : vision, code, outils, taille de contexte ou niveau de raisonnement. Choisir ensuite le plus petit et le plus rapide modèle capable d'atteindre les critères d'acceptation. Utiliser coût et latence comme critères de départage après capacité et qualité minimale.

- Modèle compact et rapide : inventaire, extraction, vérification de liens, comparaison structurée, contrôles déterministes et génération factuelle d'alts si la vision est disponible.
- Modèle compatible vision : images, captures, comparaison visuelle, identification du rôle d'un média et génération d'alts. Une tâche simple ne justifie pas par défaut un modèle frontier.
- Modèle au raisonnement plus robuste : architecture partagée, synthèse multi-source ambiguë, diagnostic complexe, arbitrage de conflits et mutation à fort rayon d'impact.

Ne pas hard-coder une gamme de modèles dans ce skill. Inspecter les modèles disponibles au moment de la délégation. Si aucun modèle ne possède la capacité nécessaire, remonter un blocage au lieu de simuler cette capacité.

## Blocages d'information

Un sous-agent ne déduit jamais une information requise. Si, après vérification des sources autorisées, une donnée reste introuvable, ambiguë ou contradictoire, il suspend immédiatement toute écriture qui en dépend, conserve la cible inchangée et remonte un blocage au coordinateur.

Le coordinateur vérifie l'application de l'ordre de priorité. Si le manque persiste, il demande une décision explicite à l'utilisateur et ne réattribue pas l'implémentation affectée avant sa réponse.

Les agents peuvent poursuivre uniquement des contrôles en lecture seule indépendants du blocage. Ils ne créent pas de placeholder, de contenu supposé ou de configuration provisoire publiable.

## Ce qu'il faut paralléliser largement

- lecture de l'ERP et des sources métier ;
- audit WordPress/Oxygen ;
- analyse Figma et inventaire des assets ;
- vérification des textes, médias, liens et IDs ;
- spécification des contenus dynamiques ;
- audits SEO, accessibilité, performance, légal et formulaires ;
- construction de pages internes différentes après stabilisation du socle ;
- QA finale par spécialité, en lecture seule.

## Ce qu'il faut sérialiser

- sauvegarde et opérations globales ;
- Variables, Classes, Selectors et Components partagés ;
- Header, Footer et Templates ;
- un même arbre Oxygen, même si les sections semblent séparées ;
- un même menu ;
- Complianz, WP Mail SMTP et options globales WordPress ;
- triage QA et corrections qui touchent un objet partagé ou plusieurs consommateurs.

Un éditeur Oxygen ouvert peut sauvegarder un ancien arbre entier. Après une mutation MCP ou externe, le considérer périmé et le recharger avant toute sauvegarde.

## Phases et barrières

### 1. Découverte parallèle

Lancer autant de spécialistes en lecture seule que les créneaux le permettent : ERP/sources, WordPress/Oxygen, Figma, contenus/médias, SEO/dynamique, plugins/formulaires/conformité.

Barrière `FIGMA_ANNOTATIONS_REVIEWED`, lorsque Figma est dans le périmètre : toutes les annotations du périmètre sont reliées à leur node, lues intégralement et analysées avec leurs effets directs et indirects. Aucun blocage d'annotation ne subsiste. Sans cette barrière, aucune écriture dépendante de Figma ne démarre.

Barrière `DISCOVERY_COMPLETE` : sources, conflits, IDs, slugs, objets existants, périmètre et risques sont consolidés. Toutes les informations requises pour la phase suivante sont confirmées. Si un blocage utilisateur subsiste, aucune écriture dépendante ne démarre.

### 2. Fondations globales mono-écrivain

Un seul architecte modifie successivement Variables, Classes/Selectors, Components, Header, Footer et Templates. Les autres agents relisent ou testent sans écrire.

Barrière `GLOBALS_STABLE` : le Header sticky, le Footer, les Templates obligatoires Single Article et 404, les autres objets globaux et l'éditabilité sont validés.

### 3. Accueil mono-écrivain

Un propriétaire unique construit la home. En parallèle, des agents en lecture seule vérifient les contenus, assets, loops, Figma, responsive, accessibilité et rendu sans JavaScript.

Barrière `HOME_STABLE` : l'accueil est calibré et les patterns réutilisables sont stabilisés.

### 4. Pages internes parallèles

Lorsque l'accueil est dans le périmètre, attendre `HOME_STABLE`. S'il est hors périmètre et que le socle existant a été audité et validé, `GLOBALS_STABLE` suffit.

Attribuer chaque page ou groupe indépendant à un agent différent avec son ID, ses sources et ses objets autorisés. Un agent de page ne modifie jamais un objet global ; il remet une demande au propriétaire du socle.

Barrière `PAGES_COMPLETE` : chaque propriétaire a testé localement sa cible et fourni ses preuves.

### 5. Gel et QA parallèle

Fermer les mutations, puis lancer des audits indépendants : visuel, responsive, builder, clavier/no-JS, SEO/liens/dynamique, performance/médias, formulaires/SMTP/CAPTCHA/Complianz/légal.

Barrière `MUTATIONS_CLOSED` : les agents QA signalent sans corriger. Le coordinateur déduplique les constats et réattribue les corrections aux propriétaires. Les pages ou fichiers distincts peuvent ensuite être corrigés en parallèle ; les objets partagés restent sérialisés.

Barrière `QA_PASS` : corrections intégrées, contrôles concernés relancés et régressions globales vérifiées.

## Paquet de mission obligatoire

Chaque délégation précise :

```text
Mission :
Skill à utiliser :
Objectif exact :
Capacités requises :
Modèle choisi et justification :
Sources autorisées :
Objets à lire :
Objets dont l'écriture est autorisée :
IDs WordPress/Oxygen concernés :
Nodes/frames Figma concernés, si applicable :
Annotations attendues et accessibles, si applicable :
Statut FIGMA_ANNOTATIONS_REVIEWED, si applicable :
Objets partagés interdits :
Dépendances validées :
Informations requises déjà confirmées :
Informations dont l'absence est bloquante :
Critères d'acceptation :
Preuves attendues :
Format du compte rendu :
```

Sans ID ou cible exacte, la mission reste en lecture seule. Ne transmettre aucun secret.

## Contrat de retour

Exiger un rapport vérifiable :

```text
STATUT : terminé | bloqué | constats uniquement
MODÈLE / CAPACITÉS / JUSTIFICATION : valeurs réellement utilisées
LU : objets, URLs et IDs contrôlés
MODIFIÉ : objets et IDs modifiés, ou aucun
PREUVES : captures, URLs, valeurs ou résultats de tests
CONFLITS : sources contradictoires
RISQUES : régressions possibles
BLOCAGE D'INFORMATION : donnée exacte | sources et IDs/URLs vérifiés | objet/phase affecté | écritures suspendues | question exacte à poser à l'utilisateur
DEMANDE AU COORDINATEUR : décision ou changement global requis
```

Ne jamais accepter « terminé » comme preuve. Le coordinateur relit l'état réel, intègre les résultats et reste responsable du résultat final.

## Spécialistes recommandés

- auditeur ERP et sources ;
- auditeur WordPress/Oxygen ;
- analyste Figma et assets ;
- auditeur des annotations Figma et de leurs effets indirects ;
- vérificateur de contenus ;
- architecte des fondations Oxygen ;
- intégrateur de l'accueil ;
- intégrateurs de pages internes disjointes ;
- spécialiste contenus dynamiques ;
- spécialiste SEO ;
- spécialiste légal/Complianz ;
- spécialiste formulaires/SMTP ;
- auditeurs responsive, accessibilité, performance, sans-JS et builder.

Un sous-agent peut sous-déléguer une recherche volumineuse ou un contrôle en lecture seule. Ne jamais créer une chaîne de sous-agents écrivains : l'écriture reste attachée au propriétaire désigné.
