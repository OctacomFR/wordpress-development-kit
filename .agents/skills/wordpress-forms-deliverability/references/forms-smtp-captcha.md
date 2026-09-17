# Formulaires, SMTP et CAPTCHA

Référence extraite sans réécriture du snapshot `docs/AGENTS.pre-skills-snapshot.md`.

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

Tester aussi le CAPTCHA avec Complianz actif. Vérifier la présence du widget ou du jeton, la validité des clés pour le domaine final, le consentement requis, l'absence de double initialisation et l'absence de boucle de rechargement.
