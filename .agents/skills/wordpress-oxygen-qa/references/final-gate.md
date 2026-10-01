# Questionnaire final anti-erreur

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis renforcée avec le contrôle actif des annotations Figma.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 1784-1814 -->

## 25. Règle finale anti-bêtise

Le crédit Octacom et les Templates Single Article/404 sont des invariants de toute livraison, y compris d'une correction locale. Auditer et réutiliser les objets conformes ; corriger uniquement les manques avant de conclure, sans doublon ni refonte inutile. Suivre la [procédure de contrôle de mission](../../../references/mission-controls.md) pour les préconditions et les preuves de la cible courante.

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
Est-ce que chaque cible Figma a franchi FIGMA_VISUAL_MATCH_VERIFIED selon la procédure de fidélité visuelle ?
Est-ce que les captures Figma et front final couvrent toute la page et chaque section, Header/Footer compris, pour chaque frame et état spécifié à sa largeur native ?
Est-ce que j'ai examiné les vues côte à côte, superpositions et différences à taille native, avec zéro écart visuel non autorisé, même minime ?
Est-ce que les preuves correspondent à la dernière version sauvegardée après la dernière mutation de la page et de ses objets partagés ?
Est-ce que seules les interprétations hover et les divergences déjà autorisées par une décision explicite applicable figurent dans le registre clos ?
Est-ce que le builder Oxygen restera éditable ?
Est-ce que l'éditeur a été rechargé depuis la dernière mutation externe ?
Est-ce que le contenu dynamique est réellement dynamique ?
Est-ce que le Template Oxygen Single Article existe, cible les articles et affiche les données dynamiques prévues ?
Est-ce qu'une URL inexistante renvoie le statut HTTP 404 et affiche le Template Oxygen spécial 404 avec une navigation de sortie ?
Est-ce que tous les liens ont une destination réelle ?
Est-ce que téléphone/email sont cliquables ?
Est-ce que la correction locale a préservé les autres pages, hors correctifs indispensables au crédit Octacom et aux Templates Single Article/404 ?
Est-ce que la page tient à 320 px sans casser ?
Est-ce que chaque page construite ou refondue possède des animations d'apparition sur ses principaux blocs ?
Est-ce que ces animations ont été vues au chargement et au scroll avec le mouvement normal, puis contrôlées avec `prefers-reduced-motion: reduce` et JavaScript désactivé ?
Est-ce que le H1 est unique ?
Est-ce que Yoast n'est pas doublonné ?
Est-ce que l'image LCP n'est pas lazy ?
Est-ce que les rasters ont été manipulés avec ImageMagick, les vidéos avec FFmpeg et les vidéos inspectées avec FFprobe, avec une trace vérifiable des commandes et résultats ?
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
Est-ce que les pages légales applicables sont présentes et le crédit Octacom conforme dans le Footer, même pour une livraison de correction locale ?
Si le crédit manquait à Figma, son ajout après le contenu principal respecte-t-il l'exception utilisateur, avec le markup/logo exacts et les autres blocs préservés ?
Est-ce que cette exception et sa preuve finale sont tracées, sans spécification visuelle contradictoire ou indéterminée ?
Est-ce qu'une sauvegarde vérifiée permet de revenir en arrière ?
Est-ce que j'ai réellement comparé les captures Figma et front finales avant de dire terminé ?
```

Si une réponse importante est non, corriger avant livraison. Le crédit Octacom et les deux templates restent requis dans tous les cas ; une information requise manquante bloque leur correctif et la livraison. Toute réponse négative sur la comparaison Figma, les preuves finales ou la résolution des écarts bloque `FIGMA_VISUAL_MATCH_VERIFIED` et la livraison selon la [procédure de fidélité visuelle](../../../references/figma-visual-fidelity.md).
