---
name: wordpress-oxygen-qa
description: "Effectuer la recette finale d'un site WordPress/Oxygen sur le front et dans le builder : visuel, responsive, sans-JS, SEO, médias, formulaires, conformité et rapport vérifiable."
---

# QA WordPress/Oxygen

Vérifier l'artefact réel. Ne jamais déclarer « pixel perfect », « responsive », « SEO OK » ou « terminé » à partir du code ou du compte rendu d'un autre agent.

## Références à lire

- Procédure navigateur, responsive et technique : [references/visual-and-technical-qa.md](references/visual-and-technical-qa.md).
- Definition of Done et rapport final : [references/definition-of-done-and-report.md](references/definition-of-done-and-report.md).
- Questionnaire final : [references/final-gate.md](references/final-gate.md).
- Preuves des transformations image et vidéo : [../../references/media-tooling.md](../../references/media-tooling.md). Lire cette procédure lorsqu'un média a été produit ou modifié pendant le projet ou pendant une correction de QA.
- Sources documentaires historiques, uniquement si une vérification documentaire est nécessaire : [references/official-sources.md](references/official-sources.md).

## Gel et audits parallèles

Avant la QA initiale, fermer les mutations. Utiliser `octacom-parallel-delivery` pour lancer des auditeurs en lecture seule :

- fidélité visuelle desktop ;
- annotations Figma, matrice de suivi et effets indirects ;
- responsive et débordements ;
- builder/editability ;
- clavier, accessibilité, motion et sans-JS ;
- SEO, liens et contenus dynamiques ;
- performance, images et widgets ;
- formulaires, SMTP, CAPTCHA, Complianz et pages légales.

Le coordinateur déduplique les constats, les attribue aux propriétaires, gèle de nouveau les mutations et relance les contrôles concernés. Aucun agent QA ne corrige pendant la passe d'observation.

## Vérifications indispensables

- comparer le front à Figma au viewport de référence puis aux largeurs responsive et intermédiaires ;
- vérifier que chaque annotation du périmètre est recensée, implémentée et validée, que ses effets indirects sont contrôlés et qu'aucun blocage ne reste silencieux ;
- tester au minimum 320, 360, 390, 480, 768, 1024, 1280, 1440 et 1920 px lorsque le site est destiné aux viewports standards, puis une largeur intermédiaire proche de chaque changement de layout ;
- tester le site avec JavaScript désactivé ;
- tester Header sticky, menu, liens, formulaires, CTA, médias, états et absence de boucle ;
- ouvrir Oxygen, sélectionner les éléments, modifier/annuler une propriété et recharger après mutation externe ;
- inspecter console, erreurs de ressources, placeholders, liens factices, assets Figma temporaires, alt, Hn, métadonnées et canonical ;
- vérifier que tous les rasters maîtrisés utilisés par les pages sont en WebP et que les logos, icônes, formes et illustrations vectorielles utilisent un SVG optimisé, sauf contrainte technique démontrée ;
- vérifier que chaque raster modifié l'a été avec ImageMagick et chaque vidéo avec FFmpeg, que les vidéos ont été inspectées avec FFprobe et que la commande, la version de l'outil et le résultat contrôlé sont consignés ;
- vérifier le Template Single Article et ouvrir une URL inexistante pour valider le Template Oxygen spécial 404, son statut HTTP, sa navigation, son responsive et son héritage du Header/Footer ;
- prouver la réception SMTP du formulaire sur `support@octacom.fr`, configuré comme unique destinataire sans CC/BCC client, avec `support@octacom.fr` dans le champ email, des données fictives uniquement et `contact@<FINAL_DOMAIN>` comme `From Email` de production ; puis vérifier qu'avant livraison le destinataire est lui aussi configuré par défaut sur `contact@<FINAL_DOMAIN>`, ou sur une autre adresse explicitement validée, sans envoyer de test à l'adresse finale sauf demande explicite ;
- refuser tout `From Email`, Sender ou envelope sender Gmail, Outlook, Hotmail, Yahoo ou autre domaine non contrôlé par le client ; si une source mentionne `redirection vers`, vérifier la configuration SMTP OVH vers/depuis `contact@<FINAL_DOMAIN>` et signaler la redirection console comme hors périmètre ;
- vérifier séparément dans WP Mail SMTP que le SMTP Username correspond à une vraie boîte authentifiable ; inspecter dans les en-têtes du message reçu le `From` autorisé, le Return-Path/envelope sender sur un domaine personnalisé contrôlé par le client sans exiger qu'il soit textuellement identique au `From`, et le Reply-To de test égal à `support@octacom.fr` lorsque le champ visiteur l'alimente ;
- vérifier que l'unique page **Politique de protection des données** a été générée par Complianz, contient dans Oxygen une seule occurrence de `[cmplz-document type="cookie-statement" region="eu"]` et rend le document sur le front sans afficher le shortcode brut ; vérifier aussi le menu légal, les autres pages rendues, le crédit Octacom et l'absence de variables de template.

## Rapport final

Présenter brièvement : implémenté, réutilisable, dynamique, QA effectuée, limites réelles. Une vérification impossible est indiquée explicitement.

Pour un développement complet, produire le récapitulatif temps/tokens/coût seulement depuis les journaux accessibles, détaillé par modèle et catégorie. Ne jamais estimer une donnée absente ; écrire `non disponible dans les journaux accessibles`. Citer la source et la date des tarifs utilisés.
