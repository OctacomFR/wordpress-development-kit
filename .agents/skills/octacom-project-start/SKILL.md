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

## Informations manquantes

Chercher d'abord dans WordPress, l'ERP en lecture seule, Figma, les documents et les sources fournies. Ne jamais inventer. Demander uniquement ce qui reste introuvable et bloque une décision irréversible ou une configuration métier.

Le domaine public final est obligatoire avant Complianz, WP Mail SMTP, les cookies, les URLs absolues, les expéditeurs et les redirections. Ne pas le déduire de la préproduction.

Ne jamais copier dans un rapport, un prompt de sous-agent ou un fichier de suivi les mots de passe, clés SMTP, clés CAPTCHA, licences ou autres secrets.

## Sous-agents

Pour un cadrage non trivial, utiliser `octacom-parallel-delivery` et déléguer en lecture seule des inventaires disjoints : sources/ERP, WordPress/Oxygen, Figma/assets, plugins/SEO/conformité. Le coordinateur fusionne les constats avant la première écriture.

## Critère de sortie

Ne passer à la construction que lorsque le site et les connecteurs sont certains, les sources sont classées, les conflits bloquants sont résolus ou signalés, les IDs critiques sont connus et la stratégie de retour arrière est vérifiée.
