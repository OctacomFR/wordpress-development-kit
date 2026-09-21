---
name: octacom-project-start
description: "Cadrer un projet WordPress/Oxygen Octacom avant toute mutation : sources, ERP en lecture seule, domaine final, audit WordPress/Oxygen et sauvegarde. À utiliser au démarrage d'un site, d'une refonte ou d'une reprise importante."
---

# Démarrage d'un projet Octacom

Établir un dossier de travail fiable avant de construire. Ne rien modifier tant que le site cible, les sources, le périmètre et les objets existants ne sont pas identifiés.

## Références à lire

- Lire [references/project-baseline.md](references/project-baseline.md) pour les paramètres, priorités et invariants historiques.
- Lire [references/intake-audit-backup.md](references/intake-audit-backup.md) pour le cadrage, l'audit et la sauvegarde.

## Séquence obligatoire

1. Confirmer `SITE_URL`, `FINAL_DOMAIN`, `WORDPRESS_MCP`, `FIGMA_URL`, `COMPANY_ID`, `PROJECT_ID`, la version d'Oxygen, le connecteur SEO et la langue.
2. Vérifier que le MCP WordPress correspond au site courant. Inspecter ses outils avant de nommer une capacité.
3. Construire les URLs ERP avec les identifiants confirmés et consulter l'entreprise et le projet en lecture seule. Ne jamais modifier l'ERP sans demande explicite.
4. Recenser les sources métier, leur niveau de priorité et les contradictions.
5. Auditer WordPress, Oxygen, les menus, plugins, médias, pages, objets globaux, contenus dynamiques et métadonnées existants.
6. Identifier les pages hors périmètre et les contraintes intangibles.
7. Créer et vérifier une sauvegarde proportionnée au risque avant toute mutation importante.
8. Produire une fiche de départ courte : données confirmées, éléments manquants, conflits, IDs et slugs réels, périmètre, sauvegarde et risques.

Pendant le recensement des sources, distinguer obligatoirement : adresse email affichée, domaine(s) personnalisé(s) appartenant au client, adresse technique de réception du formulaire, adresse d'expédition SMTP, fournisseur email et éventuelle mention `redirection vers <adresse>`. Une adresse Gmail, Outlook ou autre adresse personnelle affichée ne peut jamais devenir l'expéditeur SMTP.

Si une source indique `redirection vers`, appliquer la convention Octacom : relever en lecture seule l'adresse cible et préparer la branche de configuration OVH décrite dans `wordpress-forms-deliverability`. Cette mention déclenche la branche OVH, mais n'autorise pas à inventer l'offre, la région, le serveur, le port, le chiffrement, la boîte ou les identifiants. Retrouver et confirmer ces données ou bloquer la configuration. Ne jamais créer ou modifier la redirection dans la console OVH : cette opération reste hors périmètre.

## Informations manquantes : blocage strict

Identifier toute information requise pour chaque décision ou mutation : contenu, média, URL, cible, ID, périmètre, donnée légale, paramètre de configuration ou validation métier.

Chercher d'abord dans les sources autorisées selon leur ordre de priorité : instruction utilisateur, documents métier validés, WordPress ou ERP vérifiés, Figma dans son rôle applicable, puis documentation. Une information introuvable, ambiguë ou contradictoire ne peut jamais être déduite ou remplacée par une valeur plausible.

Toute information requise encore absente bloque l'implémentation qui en dépend. Documenter le manque, les sources contrôlées, les objets affectés et la décision attendue, puis demander l'instruction de l'utilisateur. Ne faire aucune écriture ni configuration affectée avant sa réponse.

Le travail peut continuer seulement en lecture seule et hors dépendance : audits, inventaires, vérification complémentaire des sources, cartographie des impacts et préparation d'options explicitement non retenues. Ne pas créer de placeholder ou de brouillon publiable pour contourner le blocage.

Le domaine public final est obligatoire avant Complianz, WP Mail SMTP, les cookies, les URLs absolues, les expéditeurs et les redirections. Ne pas le déduire de la préproduction.

Ne jamais copier dans un rapport, un prompt de sous-agent ou un fichier de suivi les mots de passe, clés SMTP, clés CAPTCHA, licences ou autres secrets.

## Sous-agents

Pour un cadrage non trivial, utiliser `octacom-parallel-delivery` et déléguer en lecture seule des inventaires disjoints : sources/ERP, WordPress/Oxygen, Figma/assets, plugins/SEO/conformité. Le coordinateur fusionne les constats avant la première écriture.

## Critère de sortie

Ne passer à la construction que lorsque le site et les connecteurs sont certains, les sources sont classées, toutes les informations requises pour la phase sont confirmées, les blocages ont reçu une décision explicite de l'utilisateur, les IDs critiques sont connus et la stratégie de retour arrière est vérifiée.
