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

## Identité d'envoi obligatoire

- Le `From Email`, le Sender et l'envelope sender utilisent toujours une adresse d'un domaine personnalisé appartenant au client et authentifié pour l'envoi.
- Interdire Gmail, Outlook, Hotmail, Yahoo et tout autre domaine personnel, grand public ou tiers comme expéditeur SMTP, même si cette adresse est affichée sur le site.
- Par défaut, utiliser `contact@<FINAL_DOMAIN>` comme `From Email` et destinataire du formulaire. Une adresse alternative doit appartenir à un autre domaine personnalisé du client et être fournie et validée explicitement.
- L'adresse visible, le destinataire WordPress, le `From Email`, l'envelope sender, le SMTP Username et le Reply-To sont des champs distincts. Un visiteur peut fournir une adresse Gmail/Outlook comme Reply-To ; elle ne devient jamais le Sender.
- Vérifier que la boîte utilisée pour le SMTP est un compte authentifiable. Une simple redirection ou un alias sans identifiants ne suffit pas pour envoyer.

## Branche `redirection vers` et OVH

Lorsqu'une source métier ou l'ERP consulté en lecture seule contient `redirection vers <adresse>` :

1. utiliser `contact@<FINAL_DOMAIN>` comme `From Email`, SMTP Username et destinataire du formulaire ;
2. identifier l'offre email OVH réelle, par exemple MX Plan, Email Pro, Exchange ou Zimbra, et sa région ;
3. préparer WP Mail SMTP avec l'hôte, le port, le chiffrement et l'authentification indiqués par la documentation OVHcloud officielle de cette offre au moment du projet ;
4. ne jamais déduire les identifiants ni copier le mot de passe dans un rapport ou un prompt de sous-agent ;
5. conserver l'adresse personnelle indiquée après `redirection vers` uniquement comme cible de transfert côté OVH, jamais comme destinataire ou expéditeur WordPress ;
6. ne pas ouvrir, créer ou modifier la redirection dans la console OVH. Cette opération est hors périmètre et doit être signalée comme coordination externe.

`redirection vers` est la convention projet qui déclenche la préparation OVH ; ce libellé ne prouve pas à lui seul l'offre, la région, le serveur ou les identifiants. Les documentations OVHcloud exposent notamment des couples 587/STARTTLS et 465/SSL-TLS selon l'offre et le contexte. Ne jamais mélanger un port avec le chiffrement d'une autre configuration ni transformer un exemple en valeur universelle. MX Plan, Email Pro, Exchange et Zimbra peuvent employer des hôtes différents : vérifier dans la documentation officielle à jour la combinaison complète correspondant à l'offre, à la région et à la boîte réelles.

Si l'offre, la région, la boîte authentifiable, le serveur, le port, le chiffrement ou les identifiants manquent, bloquer la configuration. Une redirection ou un alias seul ne constitue pas une boîte SMTP authentifiable.

## Données et destinataire de test obligatoires

Lors de tout test qui remplit des champs, utiliser `support@octacom.fr` pour l'email et des valeurs fictives pour le reste, même si le test ne déclenche finalement aucun envoi.

Avant tout envoi de recette :

1. confirmer `FINAL_DOMAIN` et relever toute adresse alternative sur un domaine personnalisé du client explicitement validée par une source projet prioritaire ;
2. remplacer temporairement tous les destinataires, CC et BCC du formulaire par l'unique adresse `support@octacom.fr` ;
3. saisir `support@octacom.fr` dans le champ email du formulaire afin que le Reply-To de test n'utilise aucune donnée client ;
4. remplir les autres champs avec des valeurs manifestement fictives et identifier l'envoi par `TEST OCTACOM - NE PAS TRAITER` ;
5. ne jamais utiliser le nom, le téléphone, l'adresse, l'email ou le message réel du client dans une soumission de test.

Pour le dernier test de délivrabilité, conserver `support@octacom.fr` comme destinataire unique et configurer `contact@<FINAL_DOMAIN>` comme `From Email` afin de vérifier l'expédition de production sans solliciter l'adresse finale. Après réception, configurer aussi `contact@<FINAL_DOMAIN>` comme destinataire du formulaire. Une autre adresse n'est admise que si le projet la fournit, la valide explicitement et qu'elle appartient à un domaine personnalisé du client. Relire les deux réglages sans envoyer de test à l'adresse finale sauf demande explicite.

Ne jamais dériver `contact@<FINAL_DOMAIN>` de la préproduction. Vérifier l'existence de la boîte, l'authentification SMTP et l'alignement du domaine expéditeur. Si l'un de ces points ne peut pas être confirmé, la configuration finale reste bloquée.

## Tests séparés

- labels, erreurs, focus, mobile et rendu sans JavaScript ;
- case de consentement et lien légal ;
- CAPTCHA, honeypot et CSRF/nonce ;
- interaction CAPTCHA/Complianz, double initialisation et boucle de rechargement ;
- connexion WP Mail SMTP ;
- envoi réel vers `support@octacom.fr`, avec `From Email` de production `contact@<FINAL_DOMAIN>` et Reply-To `support@octacom.fr`, puis réception, échec contrôlé et journaux disponibles ;
- configuration et relecture du destinataire et du `From Email` de production, par défaut `contact@<FINAL_DOMAIN>`, avant livraison.

Un message de succès dans le navigateur ou la présence du plugin ne prouve pas la réception.

## Sous-agents

Les audits du formulaire, du CAPTCHA/consentement et de la configuration SMTP peuvent être parallèles et en lecture seule. Les écritures sur le formulaire, Complianz et WP Mail SMTP ont des propriétaires distincts mais sont coordonnées et sérialisées lorsqu'elles touchent le même flux.
