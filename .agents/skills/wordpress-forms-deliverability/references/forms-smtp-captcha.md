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

### Protocole obligatoire pour les soumissions de test

- configurer temporairement `support@octacom.fr` comme unique destinataire du formulaire, y compris en retirant provisoirement tout CC/BCC client ;
- saisir `support@octacom.fr` dans le champ email du formulaire ;
- utiliser `TEST OCTACOM` comme identité et `TEST OCTACOM - NE PAS TRAITER` dans le sujet ou le message ;
- remplir les éventuels autres champs obligatoires avec des données clairement fictives compatibles avec leur validation ;
- ne jamais recopier dans le test le nom, le téléphone, l'adresse, l'email, le message ou une autre donnée réelle du client ;
- vérifier la réception sur `support@octacom.fr`, le contenu, les en-têtes, le Reply-To, les pièces jointes éventuelles et les messages de succès/erreur ;
- après les tests, rétablir le destinataire final validé du client et contrôler sa valeur dans la configuration sans déclencher d'envoi vers lui, sauf demande explicite ;
- supprimer les entrées de test stockées dans WordPress lorsqu'elles ne servent plus de preuve et qu'une suppression sûre est disponible.

Ne pas remplacer l'adresse d'expédition WP Mail SMTP par `support@octacom.fr` sauf si cette adresse a été explicitement validée comme expéditeur pour le domaine concerné. Le destinataire de test, l'email saisi dans le formulaire et l'expéditeur SMTP sont trois réglages distincts.

Tester aussi le CAPTCHA avec Complianz actif. Vérifier la présence du widget ou du jeton, la validité des clés pour le domaine final, le consentement requis, l'absence de double initialisation et l'absence de boucle de rechargement.
