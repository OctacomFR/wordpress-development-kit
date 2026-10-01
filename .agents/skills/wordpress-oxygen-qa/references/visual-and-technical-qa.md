# QA visuelle, responsive et technique

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis harmonisée avec la matrice responsive canonique et la barrière active des annotations Figma.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 1320-1397 -->

## 18. QA visuelle obligatoire avec navigateur

Utiliser un navigateur pour contrôler le front réel. Pour tout périmètre Figma, lire et appliquer obligatoirement la [procédure de fidélité visuelle](../../../references/figma-visual-fidelity.md). Sans moyen fiable de capture et comparaison, la livraison est bloquée.

### 18.1. Workflow de comparaison

Pour chaque page ou objet référencé, comparer ses captures Figma et front à la largeur native de chaque frame et état spécifié. Couvrir la page entière et toutes ses sections, Header et Footer compris. Examiner réellement les vues côte à côte, superpositions et différences, avec les mesures des nodes et la matrice d'annotations.

Appliquer la boucle de correction et le registre de la procédure canonique jusqu'à zéro écart visuel non autorisé. Seuls les effets hover peuvent être interprétés. Aucune tolérance de score ou qualification d'écart « mineur » ne permet de terminer. Les preuves finales doivent dater d'après la dernière mutation affectant le rendu.

Franchir `FIGMA_VISUAL_MATCH_VERIFIED` avant de valider la QA. Un écart non résolu se consigne pendant le travail et bloque la livraison. Pour l'accueil, achever le contrôle desktop avant de valider les réglages responsive. Contrôler aussi 1920 px ; sans frame à cette largeur, documenter ce contrôle responsive sans lui attribuer une identité Figma non vérifiable.

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

- `FIGMA_VISUAL_MATCH_VERIFIED` est franchi pour chaque cible Figma ; les captures et comparaisons de chaque frame et état spécifié ont été examinées, le registre est clos et les preuves correspondent au rendu final sauvegardé ;
- toutes les annotations du périmètre possèdent un statut `vérifiée` et une preuve, ou un blocage utilisateur explicite qui empêche la livraison ;
- chaque page construite ou refondue possède des animations d'apparition sur ses principaux blocs ;
- animations d'apparition testées avec le mouvement normal au chargement et au scroll, sur desktop et mobile ;
- comportement testé avec `prefers-reduced-motion: reduce` : le mouvement est réduit ou désactivé et le contenu reste visible ;
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
- soumissions de test reçues sur `support@octacom.fr` via WP Mail SMTP, avec `contact@<FINAL_DOMAIN>` comme `From Email`, `support@octacom.fr` dans le champ email et uniquement des données fictives clairement marquées `TEST OCTACOM - NE PAS TRAITER` ;
- `support@octacom.fr` était l'unique destinataire pendant les tests, sans autre adresse en destinataire, CC ou BCC ; avant livraison, destinataire du formulaire et `From Email` configurés par défaut sur `contact@<FINAL_DOMAIN>`, ou sur une adresse alternative explicitement validée, sans envoi à l'adresse finale sauf demande explicite ;
- `From Email`, Sender, envelope sender et SMTP Username utilisent une adresse d'un domaine personnalisé contrôlé par le client ; aucune adresse Gmail, Outlook, Hotmail, Yahoo ou autre domaine tiers n'est utilisée pour l'expédition ;
- lorsqu'une source indique `redirection vers`, WP Mail SMTP utilise l'offre OVH réelle pour envoyer depuis `contact@<FINAL_DOMAIN>` vers `contact@<FINAL_DOMAIN>` ; l'adresse personnelle n'apparaît pas dans la configuration WordPress et la redirection console OVH est signalée hors périmètre ;
- la configuration WP Mail SMTP confirme séparément un SMTP Username rattaché à une vraie boîte authentifiable ; les en-têtes reçus confirment un `From` autorisé, un Return-Path/envelope sender sur un domaine personnalisé du client — sans imposer une égalité textuelle avec le `From` — et, pendant le test, un Reply-To égal à `support@octacom.fr` lorsque le champ email l'alimente ;
- CAPTCHA fonctionnel sans boucle de rechargement ;
- Complianz testé avant/après consentement et wrappers de carte/vidéo contrôlés ;
- l'unique page **Politique de protection des données** a été générée par Complianz puis éditée dans Oxygen ; elle contient une seule occurrence de `[cmplz-document type="cookie-statement" region="eu"]`, le document est rendu sur le front et aucun shortcode brut n'est visible ;
- pages **Politique de protection des données** et **Mentions légales** accessibles par le menu du footer, ainsi que les **Conditions générales de vente** lorsqu'elles existent ou sont applicables ;
- crédit Octacom présent, contrasté et non cassé ;
- éditeur Oxygen rechargé après la dernière mutation externe avant toute sauvegarde finale.
