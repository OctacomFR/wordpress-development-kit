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

## Données et destinataire de test obligatoires

Lors de tout test qui remplit des champs, utiliser `support@octacom.fr` pour l'email et des valeurs fictives pour le reste, même si le test ne déclenche finalement aucun envoi.

Avant tout envoi de recette :

1. relever l'adresse finale validée afin de pouvoir la rétablir exactement après le test ;
2. remplacer temporairement tous les destinataires, CC et BCC du formulaire par l'unique adresse `support@octacom.fr` ;
3. saisir `support@octacom.fr` dans le champ email du formulaire afin que le Reply-To de test n'utilise aucune donnée client ;
4. remplir les autres champs avec des valeurs manifestement fictives et identifier l'envoi par `TEST OCTACOM - NE PAS TRAITER` ;
5. ne jamais utiliser le nom, le téléphone, l'adresse, l'email ou le message réel du client dans une soumission de test.

Après la preuve de réception sur `support@octacom.fr`, rétablir l'adresse finale validée du client et relire la configuration. Ne pas envoyer un test au client sauf demande explicite. L'adresse temporaire de réception ne remplace pas l'expéditeur SMTP validé.

## Tests séparés

- labels, erreurs, focus, mobile et rendu sans JavaScript ;
- case de consentement et lien légal ;
- CAPTCHA, honeypot et CSRF/nonce ;
- interaction CAPTCHA/Complianz, double initialisation et boucle de rechargement ;
- connexion WP Mail SMTP ;
- envoi réel vers `support@octacom.fr`, réception, Reply-To `support@octacom.fr`, échec contrôlé et journaux disponibles ;
- restauration et relecture du destinataire final validé avant livraison.

Un message de succès dans le navigateur ou la présence du plugin ne prouve pas la réception.

## Sous-agents

Les audits du formulaire, du CAPTCHA/consentement et de la configuration SMTP peuvent être parallèles et en lecture seule. Les écritures sur le formulaire, Complianz et WP Mail SMTP ont des propriétaires distincts mais sont coordonnées et sérialisées lorsqu'elles touchent le même flux.
