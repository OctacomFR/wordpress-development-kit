# Pages légales et Complianz

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis harmonisée pour corriger le lien relatif et attribuer au client ou à son conseil la décision d'applicabilité des CGV.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 1096-1106 -->

### 13.7. Pages légales, Complianz et consentement

- Créer ou compléter les mentions légales à partir de [`templates/mentions-legales.html.tpl`](../../../../templates/mentions-legales.html.tpl). Remplacer chaque variable par une donnée confirmée. Ne jamais publier un placeholder.
- Demander en amont la raison sociale, la forme juridique, le capital si applicable, l'adresse postale complète, les téléphones et emails publiables, les numéros d'immatriculation, le responsable de publication, les coordonnées du responsable de traitement, le DPO si applicable, l'hébergeur et le propriétaire du site.
- Faire valider le contenu juridique par le client ou son conseil. Le template structure la collecte et la rédaction ; il ne constitue pas une validation juridique.
- La page de confidentialité porte strictement le titre **Politique de protection des données**.
- Générer d'abord cette page avec Complianz afin que le plugin crée et gère le document. Réutiliser cette page, sans doublon.
- Après la génération, ouvrir cette même page dans Oxygen. Ajouter une seule occurrence du shortcode exact `[cmplz-document type="cookie-statement" region="eu"]` dans l'élément Oxygen natif prévu pour exécuter les shortcodes, ou dans l'élément équivalent réellement disponible dans la version installée. Ne pas l'ajouter comme simple texte, ne pas conserver une seconde occurrence dans l'éditeur WordPress classique et ne pas recopier le document sous forme de contenu statique.
- Vérifier sur le front que Complianz rend le document à la place du shortcode, puis rouvrir la page dans Oxygen pour confirmer que la structure reste éditable.
- Ajouter **Politique de protection des données** et **Mentions légales** au menu WordPress du footer. Ajouter aussi les **Conditions générales de vente** lorsqu'une page validée existe ou que le client ou son conseil confirme qu'elles sont applicables à l'activité. L'agent ne décide jamais seul de cette applicabilité. Rendre ce menu dans le Footer Oxygen et ne pas maintenir une seconde liste de liens légaux codée à la main. Ne jamais inventer des CGV ni publier une page CGV vide.
- Configurer Complianz pour le domaine public final, les services réellement présents, la zone juridique du projet et les scripts/iframes observés. Tester avant consentement, après acceptation, après refus et après retrait du consentement.
- Vérifier les wrappers ajoutés par Complianz autour des cartes, vidéos et autres iframes. Ils doivent respecter la largeur prévue et réserver leur hauteur.
- Une page légale vide, un shortcode absent, dupliqué ou brut non rendu, ou un lien de footer cassé bloque la livraison.
