# Questionnaire final anti-erreur

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis renforcée avec le contrôle actif des annotations Figma.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 1784-1814 -->

## 25. Règle finale anti-bêtise

Avant de modifier le site, se demander :

```text
Est-ce que j'ai lu Figma et le WordPress actuel ?
Est-ce que toutes les annotations du périmètre ont été lues intégralement ?
Est-ce que chaque annotation est reliée au bon node, frame, composant ou section ?
Est-ce que les effets indirects sur parents, occurrences, breakpoints, interactions et objets partagés ont été vérifiés ?
Est-ce qu'une annotation inaccessible, ambiguë, contradictoire ou techniquement impossible reste sans décision utilisateur ?
Est-ce que la matrice d'annotations et ses preuves sont complètes ?
Est-ce que j'utilise le bon MCP WordPress ?
Est-ce que les identifiants entreprise/projet sont confirmés et l'ERP a été consulté sans mutation ?
Est-ce que le domaine public final est confirmé avant Complianz et WP Mail SMTP ?
Est-ce que je suis bien sur Oxygen 6.x et sur la bonne version exacte ?
Est-ce que j'ai réutilisé l'existant avant de recréer ?
Est-ce qu'un élément Oxygen natif couvre le besoin avant le code custom ?
Est-ce que le rendu respecte Figma plutôt que mes goûts ?
Est-ce que le builder Oxygen restera éditable ?
Est-ce que l'éditeur a été rechargé depuis la dernière mutation externe ?
Est-ce que le contenu dynamique est réellement dynamique ?
Est-ce que le Template Oxygen Single Article existe, cible les articles et affiche les données dynamiques prévues ?
Est-ce qu'une URL inexistante renvoie le statut HTTP 404 et affiche le Template Oxygen spécial 404 avec une navigation de sortie ?
Est-ce que tous les liens ont une destination réelle ?
Est-ce que téléphone/email sont cliquables ?
Est-ce que la correction locale a laissé les autres pages intactes ?
Est-ce que la page tient à 320 px sans casser ?
Est-ce que le H1 est unique ?
Est-ce que Yoast n'est pas doublonné ?
Est-ce que l'image LCP n'est pas lazy ?
Est-ce que tous les rasters maîtrisés ont été convertis en WebP avant usage ?
Est-ce que les logos, icônes, formes et illustrations vectorielles utilisent au maximum des SVG optimisés et assainis ?
Est-ce que les iframes/images réservent leur espace ?
Est-ce que Complianz, le formulaire, le CAPTCHA et l'envoi SMTP ont été testés réellement ?
Est-ce que l'unique page **Politique de protection des données** a été générée par Complianz, puis éditée dans Oxygen avec une seule occurrence de `[cmplz-document type="cookie-statement" region="eu"]` qui rend le document sur le front sans shortcode brut visible ?
Est-ce que `support@octacom.fr` était l'unique destinataire du test et l'adresse saisie dans le champ email ?
Est-ce que tous les autres champs utilisaient des données fictives marquées `TEST OCTACOM - NE PAS TRAITER`, sans aucune donnée client ?
Est-ce que le destinataire et le `From Email` sont revenus par défaut à `contact@<FINAL_DOMAIN>` construit depuis le domaine final confirmé, ou à une adresse alternative explicitement validée ?
Si une autre adresse est utilisée, est-elle fournie et validée explicitement par une source projet prioritaire ?
Cette adresse appartient-elle obligatoirement à un domaine personnalisé contrôlé par le client, sans Gmail, Outlook ou autre domaine tiers comme expéditeur ?
Si une source indique `redirection vers`, le SMTP OVH est-il préparé avec `contact@<FINAL_DOMAIN>` en expéditeur et destinataire, et la redirection console est-elle laissée hors périmètre ?
L'offre, la région, l'hôte, le port et le chiffrement OVH ont-ils été vérifiés ensemble dans la documentation officielle correspondant à la boîte réelle, sans transformer un exemple en réglage universel ?
La configuration WP Mail SMTP confirme-t-elle un SMTP Username authentifiable, et les en-têtes reçus confirment-ils séparément un `From` autorisé, un Return-Path/envelope sender sur un domaine personnalisé du client et le Reply-To de test attendu ?
Est-ce que la boîte et l'expédition SMTP existent réellement, sans envoi de test à l'adresse finale sauf demande explicite ?
Est-ce que les pages légales et le crédit Octacom sont présents dans le footer ?
Est-ce qu'une sauvegarde vérifiée permet de revenir en arrière ?
Est-ce que j'ai réellement regardé le rendu avant de dire terminé ?
```

Si une réponse importante est non : corriger avant livraison.
