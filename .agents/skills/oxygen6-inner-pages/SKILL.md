---
name: oxygen6-inner-pages
description: "Construire ou corriger des pages internes Oxygen 6 en réutilisant le socle validé, sans recopier la home ni introduire de régression globale."
---

# Pages internes Oxygen 6

Une page interne consomme le système établi. Elle ne recrée pas l'accueil et ne redéfinit pas seule les fondations globales. Chaque page possède un écrivain unique et un ID WordPress confirmé.

## Référence historique

Lire [references/historical-inner-pages.md](references/historical-inner-pages.md) avant de décider quels objets réutiliser ou quelles pages dynamiques créer.

## Avant chaque page

1. Lire ses sources métier, son node Figma, toutes les annotations de son périmètre et les captures utiles. Franchir `FIGMA_ANNOTATIONS_REVIEWED` avant toute écriture de la page.
2. Résoudre ID, slug, médias, liens, contraintes et pages hors périmètre.
3. Inventorier les Templates, Components, Variables, classes et patterns autorisés.
4. Identifier les besoins propres et les skills spécialisés nécessaires.
5. Vérifier que les fondations communes sont stables.

## Réutilisation et isolation

Réutiliser Header, Footer, Template Content Area, hero interne, Variables, sections/conteneurs, titres, boutons, cartes, rail social et composants dynamiques lorsqu'ils correspondent au besoin.

Ne jamais copier la home entière ni modifier une classe globale pour corriger un problème local. Si une évolution globale paraît nécessaire, documenter le besoin et les consommateurs, puis la transmettre au propriétaire du socle.

Adapter la composition au contenu réel : longueur des textes, absence ou format des médias, tableaux, galeries, formulaires et médias sticky. Les règles détaillées se trouvent dans `oxygen6-frontend-quality`.

## Parallélisation

Après `HOME_STABLE` lorsque l'accueil est dans le périmètre, attribuer des pages différentes à des agents différents. Si l'accueil est hors périmètre et que le socle existant a été audité et validé, `GLOBALS_STABLE` suffit. Chaque mission fixe l'ID de page, ses sources et interdit les objets globaux. Ne jamais répartir les sections d'une même page entre plusieurs écrivains.

En parallèle, déléguer en lecture seule : vérification des textes/médias, liens/CTA, comparaison Figma, alt, responsive, builder, sans-JS et SEO.

## Familles et spécialistes

- éditoriale : texte, hiérarchie, équilibre texte/média ;
- galerie : ratios, alt, agrandissement, clavier, chargement ;
- service : CTA et composants réutilisés ;
- contact : formulaire, carte, consentement et délivrabilité ;
- légale : données validées, Complianz, menu Footer, aucun placeholder ;
- archive/actualités : données dynamiques, états vides et template single ;
- 404 : Template Oxygen spécial `404 Not Found`, navigation de sortie, responsive, sans-JS et héritage correct du Header/Footer ;
- tableau : lisibilité et alternative mobile ;
- média sticky : arrêt dans la section, offset du Header, désactivation mobile et exclusions.

## Critère de sortie

La page est terminée lorsque toutes ses annotations et leurs effets indirects sont vérifiés, son contenu et ses médias sont exacts, ses ajustements restent locaux, le Header sticky ne masque rien, responsive/liens/états/no-JS/builder sont testés et l'accueil comme les autres consommateurs n'ont pas régressé. La livraison du site reste bloquée tant que les Templates obligatoires Single Article et 404 ne sont pas validés.
