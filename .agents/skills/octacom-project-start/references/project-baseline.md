# Paramètres, priorités et principes historiques

Référence extraite sans réécriture du snapshot `docs/AGENTS.pre-skills-snapshot.md`.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 1-110 -->

# AGENTS.md — Développement WordPress + Oxygen 6.x depuis Figma avec Codex

Guide générique pour développer des sites WordPress avec Codex à partir d'une maquette Figma, en utilisant un MCP WordPress, le MCP Figma et, lorsqu'il est disponible, le connecteur Yoast SEO.

Objectif : produire des pages fidèles à la charte, réellement éditables dans Oxygen 6.x, réutilisables, responsive, performantes, accessibles et propres pour le SEO — sans inventer de contenu ni transformer la maquette Figma en soupe de `position:absolute`.

---

## 0. Paramètres projet

Ne jamais hard-coder un client ou un domaine dans ce fichier générique.

Les informations suivantes doivent être fournies dans le prompt projet ou détectées avec les MCP :

```text
SITE_URL=<url du site>
FINAL_DOMAIN=<domaine public final, obligatoire avant Complianz et l'envoi d'emails>
WORDPRESS_MCP=<serveur MCP WordPress du projet>
FIGMA_URL=<url Figma node-specific>
COMPANY_ID=<identifiant entreprise dans la base Octacom>
PROJECT_ID=<identifiant projet dans la base Octacom>
BUILDER=Oxygen 6.x
SEO_CONNECTOR=Yoast SEO si disponible
LANG=fr-FR sauf consigne contraire
```

Règles :

- Toujours utiliser le MCP WordPress correspondant au domaine du projet courant.
- Ne jamais écrire sur un autre WordPress simplement parce qu'un autre connecteur est disponible.
- Toujours résoudre les IDs, slugs, catégories, templates et médias depuis le site avant d'écrire.
- Ne jamais inventer le nom d'un outil MCP ou une capacité que le serveur n'expose pas : inspecter les outils disponibles d'abord.
- Demander ou retrouver dès le début `COMPANY_ID` et `PROJECT_ID`. Utiliser la base Octacom en lecture seule pour consulter le dossier ; ne jamais modifier le projet ou l'entreprise dans l'ERP sans demande explicite.
- Construire les URLs ERP uniquement avec les identifiants confirmés :

```text
https://base.octacom.fr/entreprises/<COMPANY_ID>
https://base.octacom.fr/entreprises/<COMPANY_ID>/projet/<PROJECT_ID>
```

- Demander le domaine public final avant de configurer Complianz, WP Mail SMTP, les URLs absolues, les cookies, les expéditeurs ou les redirections. Ne pas déduire ce domaine de l'URL de préproduction.
- Ne jamais inscrire de mot de passe, clé CAPTCHA, clé SMTP ou licence dans ce fichier, un compte rendu ou un journal de travail.

Documentation interne de référence : [Développement WordPress Octacom](https://app.notion.com/p/octacom/Dev-Wordpress-f6510f445ce44dad95d5c81e5c193540). La consulter lorsqu'elle est accessible pour les procédures Octacom, sans lui faire remplacer les sources métier propres au projet.

---

## 1. Ordre de priorité

### 1.1. Priorité générale

En cas de conflit :

1. Dernière instruction explicite de l'utilisateur.
2. Documents métier et contenus validés du projet pour les textes, horaires, prix, coordonnées et données légales.
3. Données vérifiées dans WordPress ou dans l'ERP Octacom consulté en lecture seule.
4. Figma pour le design et la disposition ; pour le contenu uniquement si le projet le désigne comme source éditoriale.
5. Le présent `AGENTS.md`.
6. Documentation officielle de l'outil concerné.

Si deux sources de même niveau ou deux sources métier se contredisent, signaler le conflit et demander laquelle fait foi avant de publier. Ne pas choisir silencieusement.

### 1.2. Priorité DESIGN

Pour toute décision visuelle :

1. Dernière correction visuelle explicite de l'utilisateur.
2. **Charte / maquette Figma du projet, y compris annotations et commentaires accessibles.**
3. Skill `frontend-design`.
4. Composants et patterns existants du site uniquement s'ils ne contredisent pas la nouvelle charte.
5. Règles génériques de ce document.

La charte Figma est donc la vérité visuelle. Le site existant est une référence technique, pas une excuse pour conserver un ancien design.

### 1.3. Skills obligatoires

Quand les skills sont disponibles dans l'environnement Codex :

- invoquer `caveman` ;
- invoquer `unslop` ;
- invoquer `frontend-design` ;
- les utiliser sur chaque tour qui implique conception, code ou correction visuelle.

Ne jamais prétendre avoir utilisé un skill indisponible. S'il n'est pas exposé par l'environnement, le signaler une fois puis continuer avec les règles de ce guide.

Les instructions propres aux skills priment sur ce document pour leur domaine, sauf pour le design où la charte Figma reste prioritaire conformément à la section précédente.

---

## 2. Principes non négociables

1. **Lire avant d'écrire.** Auditer le site, la maquette et les composants existants avant toute modification.
2. **Ne rien inventer.** Pas de téléphone, email, horaire, prix, adresse, certification, témoignage, URL, image, texte métier ou donnée SEO factuelle inventée.
3. **Figma décrit le design, pas l'implémentation.** Le React/Tailwind éventuellement retourné par Figma MCP est une référence de structure et de style, jamais du code à coller tel quel dans WordPress/Oxygen.
4. **Oxygen 6.x doit rester éditable.** Une page qui ressemble à Figma sur le front mais se casse dans le builder est considérée comme ratée.
5. **Réutiliser avant de dupliquer.** Components, Classes, Selectors, Variables, Templates, Headers, Footers, menus et composants de boucle doivent être factorisés.
6. **Pas de contenu statique pour des données WordPress dynamiques.** Articles, titres, dates, images à la une, permaliens, catégories et contenus récurrents doivent venir de WordPress.
7. **Pas de lien factice en production.** Aucun bouton `#`, `javascript:void(0)` ou URL dev si une vraie destination existe ou doit être résolue.
8. **Navigation = lien HTML réel.** Un élément qui navigue doit produire un `<a href="...">`; un `<button>` est réservé à une action applicative.
9. **Tester réellement.** Ne jamais écrire « pixel perfect », « responsive » ou « SEO OK » sans avoir fait les contrôles correspondants.
10. **Pas d'installation inutile.** Priorité à WordPress, Oxygen 6.x et aux plugins déjà présents. Pas de dépendance ou plugin supplémentaire sans besoin réel.
11. **Pas de JavaScript pour résoudre un problème que CSS/HTML/Oxygen savent déjà résoudre proprement.**
12. **Pas de CSS ou JS global destructif.** Toujours scoper les sélecteurs aux composants concernés.
13. **Ne pas modifier hors périmètre.** Une demande de home ne donne pas carte blanche pour refaire toutes les pages.
14. **Sauvegarder ou lire l'état existant avant une écriture importante.** En cas d'échec MCP, ne pas relancer aveuglément une mutation destructive.
15. **Une correction locale reste locale.** Une page ne doit pas changer les médias, carrousels, vidéos ou espacements d'autres pages par effet de bord.
16. **Préserver le contenu validé.** Ne pas reformuler les textes métier, avis, horaires, tarifs ou mentions légales sans demande explicite.
17. **Oxygen natif d'abord.** Chercher un élément, un Component ou une capacité Oxygen compatible avant tout code custom. Construire manuellement seulement en dernier recours, avec HTML sémantique, clavier, focus et WAI-ARIA lorsque nécessaire.
18. **Un seul état d'édition fait foi.** Après une modification externe ou MCP, recharger l'éditeur Oxygen avant toute nouvelle sauvegarde pour éviter qu'un onglet ancien réinjecte une version obsolète.
19. **Contenu visible sans JavaScript.** Le HTML et le CSS initiaux doivent afficher clairement tout le contenu éditorial, la navigation et les actions essentielles. JavaScript peut enrichir l'expérience, mais son absence ou son échec ne doit jamais laisser une page vide, un texte masqué ou une navigation inutilisable.
