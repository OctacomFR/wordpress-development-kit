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
- Sources documentaires historiques, uniquement si une vérification documentaire est nécessaire : [references/official-sources.md](references/official-sources.md).

## Gel et audits parallèles

Avant la QA initiale, fermer les mutations. Utiliser `octacom-parallel-delivery` pour lancer des auditeurs en lecture seule :

- fidélité visuelle desktop ;
- responsive et débordements ;
- builder/editability ;
- clavier, accessibilité, motion et sans-JS ;
- SEO, liens et contenus dynamiques ;
- performance, images et widgets ;
- formulaires, SMTP, CAPTCHA, Complianz et pages légales.

Le coordinateur déduplique les constats, les attribue aux propriétaires, gèle de nouveau les mutations et relance les contrôles concernés. Aucun agent QA ne corrige pendant la passe d'observation.

## Vérifications indispensables

- comparer le front à Figma au viewport de référence puis aux largeurs responsive et intermédiaires ;
- tester au minimum 320, 360, 390, 480, 768, 1024, 1280, 1440 et 1920 px lorsque le site est destiné aux viewports standards, puis une largeur intermédiaire proche de chaque changement de layout ;
- tester le site avec JavaScript désactivé ;
- tester Header sticky, menu, liens, formulaires, CTA, médias, états et absence de boucle ;
- ouvrir Oxygen, sélectionner les éléments, modifier/annuler une propriété et recharger après mutation externe ;
- inspecter console, 404, placeholders, liens factices, assets Figma temporaires, alt, Hn, métadonnées et canonical ;
- prouver la réception SMTP et les scénarios Complianz/CAPTCHA applicables ;
- vérifier menu légal, pages rendues, crédit Octacom et absence de variables de template.

## Rapport final

Présenter brièvement : implémenté, réutilisable, dynamique, QA effectuée, limites réelles. Une vérification impossible est indiquée explicitement.

Pour un développement complet, produire le récapitulatif temps/tokens/coût seulement depuis les journaux accessibles, détaillé par modèle et catégorie. Ne jamais estimer une donnée absente ; écrire `non disponible dans les journaux accessibles`. Citer la source et la date des tarifs utilisés.
