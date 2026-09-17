---
name: wordpress-legal-consent
description: "Créer ou compléter les pages légales WordPress, configurer Complianz pour le domaine final et maintenir le menu légal réel du Footer sans inventer de données juridiques."
---

# Légal et consentement

Le template structure la collecte et la rédaction ; il ne remplace pas la validation du client ou de son conseil.

## Références et asset

- Lire [references/legal-complianz.md](references/legal-complianz.md).
- Utiliser [`templates/mentions-legales.html.tpl`](../../../templates/mentions-legales.html.tpl) pour les Mentions légales.

## Données à confirmer

Obtenir raison sociale, forme juridique, capital si applicable, adresse postale complète, téléphone et email publiables, immatriculations, responsable de publication, responsable de traitement, DPO si applicable, hébergeur, propriétaire du site et domaine public final. Aucun placeholder ne peut être publié.

## Règles de livraison

- La page porte strictement le titre **Politique de protection des données** et est générée/gérée par Complianz.
- Le menu WordPress réel du Footer contient **Politique de protection des données**, **Mentions légales** et **Conditions générales de vente** lorsqu'une page validée existe ou que le client confirme qu'elles s'appliquent.
- Ne jamais inventer des CGV ni publier une page vide.
- Le Footer Oxygen rend ce menu ; aucune seconde liste légale codée à la main.
- Complianz est configuré pour le domaine final, la zone juridique et les services réellement observés.
- Tester absence de consentement, acceptation, refus et retrait, ainsi que les wrappers des cartes, vidéos et iframes.
- Conserver le crédit Octacom obligatoire prévu par `oxygen6-architecture`, avec la variante de logo adaptée au contraste.

Une page vide, un shortcode brut non rendu, un lien cassé ou une variable de template restante bloque la livraison.

## Sous-agents

Déléguer en lecture seule la collecte des coordonnées, l'inventaire des services/cookies, la vérification des pages et du menu. Un propriétaire écrit les pages/Complianz ; le propriétaire du Footer applique toute modification de structure globale.
