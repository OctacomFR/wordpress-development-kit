# QA visuelle, responsive et technique

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis harmonisée avec la matrice responsive canonique et la barrière active des annotations Figma.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 1320-1397 -->

## 18. QA visuelle obligatoire avec navigateur

Lorsque l'environnement fournit un navigateur ou outil de preview, il doit être utilisé.

### 18.1. Workflow de comparaison

Pour chaque section :

1. ouvrir la page front ;
2. régler le viewport sur la largeur Figma de référence ;
3. comparer à la capture Figma ;
4. croiser la section avec toutes les lignes de la matrice d'annotations qui concernent le node, ses parents, ses variantes et ses autres occurrences ;
5. contrôler :
   - dimensions globales ;
   - max-width ;
   - alignements ;
   - gaps ;
   - padding ;
   - typo ;
   - line-height ;
   - couleurs ;
   - rayons ;
   - crops images ;
   - overlays ;
   - décorations ;
   - états hover ;
6. vérifier ordre, visibilité, responsive, sticky, interactions, destinations, Components et effets indirects demandés par les annotations ;
7. corriger ;
8. recharger et comparer à nouveau, puis joindre la preuve à la matrice.

Ne pas tout juger « à l'œil » depuis le code.

### 18.2. Responsive QA

Tester au minimum 1920, 1440, 1280, 1024, 768, 480, 390, 360 et 320 px, puis une largeur intermédiaire proche de chaque changement de layout.

Vérifier :

- overflow horizontal ;
- textes coupés ;
- éléments fixed qui masquent le contenu ;
- menu ;
- boutons ;
- images ;
- colonnes ;
- carrousels ;
- footer ;
- rail social ;
- hover/focus ;
- zone tactile.
- formulaires et cartes utilisant toute la largeur disponible ;
- sticky désactivé ou sûr aux largeurs prévues ;
- aucun rechargement en boucle.

### 18.3. QA technique

Avant de déclarer terminé :

- toutes les annotations du périmètre possèdent un statut `vérifiée` et une preuve, ou un blocage utilisateur explicite qui empêche la livraison ;
- page testée avec JavaScript désactivé : tout le contenu, la navigation et les actions essentielles restent clairs et visibles ;
- animations testées sans JavaScript et en cas d'échec de déclenchement : aucun élément ne reste masqué ;
- aucune erreur JS console liée aux modifications ;
- aucun 404 de ressource ;
- une URL volontairement inexistante renvoie le statut HTTP 404 et affiche le Template Oxygen 6 spécial `404 Not Found`, avec Header/Footer, message clair et lien de sortie fonctionnel ;
- le Template Single Article existe, cible les articles WordPress, reste éditable dans Oxygen et affiche ses données dynamiques correctement lorsqu'un article réel est disponible ;
- liens CTA testés ;
- téléphone/email testés ;
- permaliens actualités testés ;
- H1/H2 inspectés ;
- meta title/description inspectés ;
- canonical inspectée ;
- images alt inspectées ;
- aucun raster maîtrisé de contenu n'est livré en JPEG, PNG ou GIF : les fichiers utilisés par les pages sont en WebP ;
- logos, icônes, pictogrammes, formes et illustrations vectorielles utilisent un SVG optimisé et assaini, sauf contrainte technique démontrée ;
- pas de Figma asset temporaire dans le HTML final ;
- pas de contenu placeholder involontaire ;
- pas de lien `#` involontaire ;
- pas de style détruit dans le builder Oxygen ;
- front vérifié dans Chrome lorsque disponible ;
- formulaires reçus à l'adresse prévue via WP Mail SMTP ;
- CAPTCHA fonctionnel sans boucle de rechargement ;
- Complianz testé avant/après consentement et wrappers de carte/vidéo contrôlés ;
- pages **Politique de protection des données** et **Mentions légales** accessibles par le menu du footer, ainsi que les **Conditions générales de vente** lorsqu'elles existent ou sont applicables ;
- crédit Octacom présent, contrasté et non cassé ;
- éditeur Oxygen rechargé après la dernière mutation externe avant toute sauvegarde finale.
