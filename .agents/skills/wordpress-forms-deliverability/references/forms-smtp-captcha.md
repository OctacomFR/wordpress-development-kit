# Formulaires, SMTP et CAPTCHA

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis renforcée avec le protocole Octacom de test sans données client.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 1275-1291 -->

### 16.2. Formulaire de contact et délivrabilité

Utiliser l'élément Form Oxygen ou le composant déjà validé du projet lorsqu'il répond au besoin. Une implémentation manuelle vient en dernier recours et respecte HTML sémantique, WAI-ARIA applicable, sécurité serveur et amélioration progressive.

Le formulaire doit avoir :

- labels visibles et associés aux champs ;
- champs et bouton cohérents avec le design system ;
- case de consentement obligatoire quand le traitement l'exige, avec lien vers **Politique de protection des données** ;
- CAPTCHA réellement configuré, honeypot et protection CSRF/nonce ;
- adresse de destination et adresse d'expéditeur vérifiées ;
- messages de succès et d'erreur explicites ;
- focus visible, erreurs associées aux champs et affichage mobile pleine largeur.

Configurer WP Mail SMTP avec le fournisseur, le domaine public final, l'expéditeur et les identifiants validés. Ne pas inventer de serveur, port, chiffrement ou adresse. Tester séparément : connexion SMTP, envoi réel, réception, Reply-To, échec contrôlé et journaux disponibles. La présence du plugin ou d'un message de succès côté navigateur ne prouve pas la réception.

### Expéditeur sur domaine personnalisé

Le `From Email`, le Sender et l'envelope sender doivent appartenir à un domaine personnalisé contrôlé par le client. Il est interdit d'utiliser Gmail, Outlook, Hotmail, Yahoo ou un domaine tiers comme expéditeur, même si cette adresse est affichée sur le site ou reçoit habituellement les demandes du client.

Par défaut, le formulaire envoie depuis et vers `contact@<FINAL_DOMAIN>`. Une adresse personnelle affichée reste uniquement un contenu de contact. L'email du visiteur peut alimenter le Reply-To, mais jamais le `From Email`. Vérifier l'alignement SPF/DKIM/DMARC applicable, l'authentification de la boîte et la cohérence du domaine visible dans les en-têtes.

### Cas `redirection vers`

Si une source indique `redirection vers <adresse-personnelle>` :

- conserver `contact@<FINAL_DOMAIN>` comme expéditeur, SMTP Username et destinataire du formulaire ;
- préparer WP Mail SMTP avec l'offre OVH réelle et ses paramètres officiels à jour ;
- ne jamais renseigner l'adresse personnelle comme expéditeur ou destinataire WordPress ;
- traiter cette adresse uniquement comme cible de redirection dans la console OVH ;
- ne jamais intervenir dans la console OVH pour créer ou modifier cette redirection, car cette opération est hors périmètre ;
- signaler dans le rapport que la redirection OVH doit être créée ou vérifiée par la personne habilitée ;
- bloquer la configuration SMTP si `contact@<FINAL_DOMAIN>` n'est pas une vraie boîte disposant d'identifiants SMTP valides, si elle n'est qu'un alias ou une redirection non authentifiable, si l'offre OVH n'est pas identifiée ou si les accès manquent.

La mention `redirection vers` déclenche la branche OVH selon la convention Octacom, mais ne permet pas de déduire l'offre, la région, le serveur ou les identifiants. Vérifier la combinaison complète dans la documentation officielle à jour :

- MX Plan peut utiliser `smtp.mail.ovh.net` ou `ssl0.ovh.net` ; les guides OVHcloud exposent notamment 587/STARTTLS ou 465/SSL-TLS selon le contexte ;
- Email Pro utilise un hôte de la forme `pro?.mail.ovh.net`, où la valeur réelle remplace `?` ;
- Exchange utilise un hôte de la forme `ex?.mail.ovh.net` et sa configuration de connecteur d'envoi constitue un cas distinct ;
- Zimbra dépend de l'offre et des paramètres fournis pour le compte.

Ne jamais deviner le caractère `?`, la région, l'hôte, le port ou le chiffrement, ni associer le port d'une variante au chiffrement d'une autre. Sources officielles à revalider au moment de la configuration : [MX Plan](https://docs.ovhcloud.com/fr/guides/web-cloud/email-and-collaborative-solutions/mx-plan/how-to-configure-thunderbird-mac/), [Email Pro](https://docs.ovhcloud.com/fr/guides/web-cloud/email-and-collaborative-solutions/email-pro/how-to-configure-thunderbird/), [Exchange](https://docs.ovhcloud.com/fr/guides/web-cloud/email-and-collaborative-solutions/microsoft-exchange/how-to-configure-thunderbird-windows/), [Zimbra](https://docs.ovhcloud.com/fr/guides/web-cloud/email-and-collaborative-solutions/zimbra/mail-apps/) et [alias/redirections](https://docs.ovhcloud.com/fr/guides/web-cloud/email-and-collaborative-solutions/common-email-features/feature-redirections/).

### Protocole obligatoire pour les soumissions de test

- configurer temporairement `support@octacom.fr` comme unique destinataire du formulaire, y compris en retirant provisoirement tout CC/BCC client ;
- saisir `support@octacom.fr` dans le champ email du formulaire ;
- utiliser `TEST OCTACOM` comme identité et `TEST OCTACOM - NE PAS TRAITER` dans le sujet ou le message ;
- remplir les éventuels autres champs obligatoires avec des données clairement fictives compatibles avec leur validation ;
- ne jamais recopier dans le test le nom, le téléphone, l'adresse, l'email, le message ou une autre donnée réelle du client ;
- pour le dernier test de délivrabilité, garder `support@octacom.fr` comme destinataire unique, utiliser `contact@<FINAL_DOMAIN>` comme `From Email`, puis vérifier la réception, le contenu, les en-têtes, le Reply-To, les pièces jointes éventuelles et les messages de succès/erreur ;
- après les tests, configurer par défaut `contact@<FINAL_DOMAIN>` comme destinataire du formulaire et comme `From Email` WP Mail SMTP, puis contrôler les deux valeurs sans déclencher d'envoi vers cette adresse sauf demande explicite ;
- utiliser une autre adresse de production seulement si une source projet prioritaire la fournit, la valide explicitement et qu'elle appartient à un domaine personnalisé du client ;
- construire l'adresse par défaut uniquement depuis le domaine public final confirmé, jamais depuis la préproduction, puis vérifier l'existence de la boîte et la capacité d'expédition SMTP ;
- supprimer les entrées de test stockées dans WordPress lorsqu'elles ne servent plus de preuve et qu'une suppression sûre est disponible.

Ne jamais utiliser `support@octacom.fr` comme adresse d'expédition WP Mail SMTP. Pour le dernier test et la production, utiliser par défaut `contact@<FINAL_DOMAIN>` comme `From Email`, ou une autre adresse seulement si elle appartient à un domaine personnalisé du client et qu'une source projet prioritaire la valide explicitement. Le destinataire de test, l'email saisi dans le formulaire et l'expéditeur SMTP sont trois réglages distincts. Avant livraison, le destinataire et l'expéditeur reviennent par défaut à `contact@<FINAL_DOMAIN>`.

Tester aussi le CAPTCHA avec Complianz actif. Vérifier la présence du widget ou du jeton, la validité des clés pour le domaine final, le consentement requis, l'absence de double initialisation et l'absence de boucle de rechargement.
