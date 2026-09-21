# Cadrage, audit et sauvegarde

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis renforcée avec l'inventaire des identités email et redirections OVH.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 185-243 -->

## 4. Workflow obligatoire

### Phase A0 — Cadrage, ERP et sources

Avant de construire, obtenir ou retrouver :

- l'URL de préproduction et le domaine public final prévu ;
- `COMPANY_ID` et `PROJECT_ID`, puis consulter les deux fiches ERP en lecture seule ;
- le node Figma exact, les captures de référence et le dossier des captures de retours ;
- les documents qui associent les textes et médias à chaque page ou section ;
- les textes validés, coordonnées légales, horaires, tarifs et informations d'hébergement ;
- les URLs officielles des réseaux sociaux, de la fiche d'établissement et des destinations externes ;
- l'adresse email affichée sur le site, sans la confondre avec l'identité technique d'envoi ;
- le ou les domaines personnalisés appartenant au client, l'adresse de réception des formulaires, le `From Email`, le Sender/envelope sender, le fournisseur SMTP et l'existence de la boîte `contact@<FINAL_DOMAIN>` ;
- toute mention `redirection vers <adresse>`, qui déclenche selon la convention Octacom une préparation SMTP OVH mais aucune modification de la console OVH ; la mention ne permet pas de déduire l'offre, la région, la boîte ni les paramètres techniques ;
- les pages légales existantes et l'URL de la politique de protection des données ;
- les cartes, vidéos, PDF, téléchargements et codes d'intégration nécessaires ;
- la disponibilité des clés CAPTCHA, accès SMTP et licences, sans les recopier dans les comptes rendus ;
- les pages hors périmètre et les contraintes intangibles, par exemple les polices à conserver ;
- les dates de recette interne et de validation client lorsqu'elles existent.

Classer chaque donnée par source. Ne jamais compléter une donnée manquante par une supposition. Chercher d'abord dans WordPress, l'ERP consulté en lecture seule, les documents du projet et les sources fournies.

### Phase A1 — Audit du WordPress

Avant toute écriture via le MCP WordPress :

1. identifier la version WordPress si elle est exposée ;
2. confirmer la présence et la version exacte d'Oxygen 6.x ;
3. lister les pages importantes ;
4. identifier la page d'accueil ;
5. identifier les Templates Oxygen existants, leurs Locations, Conditions et Priority ;
6. identifier les Headers Oxygen existants et leurs règles d'application ;
7. identifier les Footers Oxygen existants et leurs règles d'application ;
8. identifier les Components existants et leurs Component Properties ;
9. identifier les menus WordPress et leurs items ;
10. identifier les classes/selectors et collections de Variables déjà utilisées ;
11. identifier les catégories d'articles et leur **slug réel** ;
12. identifier les articles récents utiles au développement ;
13. identifier les images/médias existants ;
14. vérifier Yoast SEO et les métadonnées existantes ;
15. relever les URLs réelles de contact, actualités, mentions légales, politique de confidentialité, réservation, etc. ;
16. lister les éléments Oxygen réellement disponibles, sans supposer qu'un élément Gallery, Accordion, Form ou Slider existe ;
17. vérifier les plugins actifs, leur rôle, leur licence si elle conditionne le fonctionnement, et les erreurs JavaScript existantes ;
18. ouvrir l'éditeur dans Chrome lorsqu'un problème semble propre au navigateur embarqué, avant de conclure que les données Oxygen sont cassées.

Ne pas créer un doublon d'une page, d'un menu ou d'un template qui existe déjà.

### Phase A2 — Sauvegarde proportionnée au risque

Avant une refonte, suppression, import global, modification de styles partagés ou opération difficile à annuler :

1. sauvegarder la base de données ;
2. sauvegarder les fichiers si l'intervention touche les médias, plugins, thèmes ou fichiers ;
3. exclure le répertoire de sauvegarde de sa propre archive ;
4. stocker la copie hors des répertoires publics du site ;
5. calculer une somme SHA-256 ;
6. noter le périmètre, la date, le chemin, la taille et la somme de contrôle ;
7. vérifier que les fichiers existent et ont une taille cohérente avant de commencer.

Une sauvegarde de base peut suffire pour une modification limitée aux structures Oxygen stockées en base. Toute modification de fichiers ou médias exige une sauvegarde complète. Sauvegarder aussi les arbres JSON, Components, Header, Footer, Templates, Selectors, Variables et réglages concernés lorsque les outils le permettent.
