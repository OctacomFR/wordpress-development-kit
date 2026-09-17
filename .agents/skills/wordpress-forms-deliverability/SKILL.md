---
name: wordpress-forms-deliverability
description: "Construire et tester un formulaire WordPress/Oxygen avec consentement, CAPTCHA, sécurité, WP Mail SMTP et preuve de réception réelle sur le domaine final."
---

# Formulaires et délivrabilité

Utiliser l'élément Form Oxygen ou le composant validé du projet avant une implémentation manuelle.

## Référence à lire

Lire [references/forms-smtp-captcha.md](references/forms-smtp-captcha.md) avant de construire, configurer ou valider un formulaire.

## Prérequis

Confirmer le domaine public final, l'adresse de destination, l'expéditeur, le fournisseur SMTP, les besoins de consentement, la page **Politique de protection des données** et les clés autorisées pour ce domaine. Ne jamais inventer ni recopier les secrets dans un rapport.

## Tests séparés

- labels, erreurs, focus, mobile et rendu sans JavaScript ;
- case de consentement et lien légal ;
- CAPTCHA, honeypot et CSRF/nonce ;
- interaction CAPTCHA/Complianz, double initialisation et boucle de rechargement ;
- connexion WP Mail SMTP ;
- envoi réel, réception, Reply-To, échec contrôlé et journaux disponibles.

Un message de succès dans le navigateur ou la présence du plugin ne prouve pas la réception.

## Sous-agents

Les audits du formulaire, du CAPTCHA/consentement et de la configuration SMTP peuvent être parallèles et en lecture seule. Les écritures sur le formulaire, Complianz et WP Mail SMTP ont des propriétaires distincts mais sont coordonnées et sérialisées lorsqu'elles touchent le même flux.
