# Traçabilité AGENTS.md vers les skills

Cette matrice prouve la destination des informations contenues dans le snapshot antérieur au découpage.

- Snapshot : `docs/AGENTS.pre-skills-snapshot.md`
- Taille : 72 845 octets
- Lignes : 1 814
- SHA-256 : `ED720A6CC4906EC5D2D607BFA9BF0C684038F96D167AEA74B6794D3C4DAC1B5F`
- Principe : le nouveau `AGENTS.md` conserve les invariants transversaux ; les procédures et exemples résident dans les skills et références ci-dessous.

## Matrice des sections historiques

| Ancienne section | Lignes | Destination active principale |
|---|---:|---|
| Introduction | 1–7 | `AGENTS.md` |
| 0. Paramètres projet | 9–44 | `AGENTS.md`; `octacom-project-start/references/project-baseline.md` |
| 1. Ordre de priorité | 48–86 | `AGENTS.md`; `octacom-project-start/references/project-baseline.md` |
| 2. Principes non négociables | 90–110 | `AGENTS.md`; `octacom-project-start/references/project-baseline.md` |
| 3. Cible Oxygen 6.x | 114–181 | `oxygen6-architecture/references/oxygen6-target-and-primitives.md` |
| 4. Phase A0–A2 | 185–243 | `octacom-project-start/references/intake-audit-backup.md` |
| 4. Phase B–C | 245–314 | `figma-to-oxygen/references/figma-reading-and-inventory.md` |
| 4. Phase D–E | 316–351 | `oxygen6-architecture/references/implementation-order.md`; `oxygen6-homepage/SKILL.md` |
| 5. Traduction Figma | 355–445 | `figma-to-oxygen/references/translation-and-assets.md` |
| 6. Architecture réutilisable | 449–642 | `oxygen6-architecture/references/reusable-architecture.md` |
| 7. Éditabilité | 646–673 | `oxygen6-architecture/references/editability-mcp-custom-code.md` |
| 8. Responsive, motion, sticky | 677–772 | `oxygen6-frontend-quality/references/responsive-motion-sticky.md` |
| 9. Rail social | 776–818 | `oxygen6-frontend-quality/references/social-links-and-iframes.md` |
| 10. Coordonnées et boutons | 820–864 | `oxygen6-frontend-quality/references/social-links-and-iframes.md` |
| 11. Actualités dynamiques | 866–950 | `wordpress-dynamic-content/references/news-and-posts.md` |
| 12. Avis iframe | 954–968 | `oxygen6-frontend-quality/references/social-links-and-iframes.md` |
| 13.1–13.5 SEO | 972–1079 | `wordpress-seo/references/technical-seo.md` |
| 13.6 Articles | 1081–1094 | `wordpress-dynamic-content/references/news-and-posts.md` |
| 13.7 Légal et Complianz | 1096–1106 | `wordpress-legal-consent/references/legal-complianz.md` |
| 14. Images | 1110–1192 | `oxygen6-frontend-quality/references/images-performance-accessibility.md` |
| 15. Performance | 1194–1243 | `oxygen6-frontend-quality/references/images-performance-accessibility.md` |
| 16 et 16.1 Accessibilité/états | 1247–1273 | `oxygen6-frontend-quality/references/images-performance-accessibility.md` |
| 16.2 Formulaire/délivrabilité | 1275–1291 | `wordpress-forms-deliverability/references/forms-smtp-captcha.md` |
| 17. Anti-slop design | 1295–1316 | `figma-to-oxygen/references/anti-slop.md` |
| 18. QA visuelle | 1320–1397 | `wordpress-oxygen-qa/references/visual-and-technical-qa.md` |
| 19. Règles MCP | 1401–1444 | `oxygen6-architecture/references/editability-mcp-custom-code.md` |
| 20. Code custom | 1448–1475 | `oxygen6-architecture/references/editability-mcp-custom-code.md` |
| 21. Pages intérieures | 1479–1506 | `oxygen6-inner-pages/references/historical-inner-pages.md`; `oxygen6-homepage/SKILL.md` |
| 22. Definition of Done | 1510–1607 | `wordpress-oxygen-qa/references/definition-of-done-and-report.md` |
| 23. Rapport final | 1611–1673 | `wordpress-oxygen-qa/references/definition-of-done-and-report.md` |
| 24. Sources officielles | 1677–1780 | `wordpress-oxygen-qa/references/official-sources.md` |
| 25. Contrôle final | 1784–1814 | `wordpress-oxygen-qa/references/final-gate.md`; résumé dans `AGENTS.md` |

Les séparateurs Markdown qui occupaient les lignes intermédiaires ne contenaient aucune instruction.

## Enrichissements ajoutés

| Sujet nouveau | Destination |
|---|---|
| Parallélisation intensive mais sûre | `octacom-parallel-delivery/SKILL.md` |
| Mission et contrat de retour des sous-agents | `octacom-parallel-delivery/SKILL.md` |
| Barrières découverte/fondations/home/pages/QA | `octacom-parallel-delivery/SKILL.md` |
| Workflow propre à la page d'accueil | `oxygen6-homepage/SKILL.md` |
| Workflow propre aux pages internes | `oxygen6-inner-pages/SKILL.md` |
| Matrice de spécialistes | `AGENTS.md`; `octacom-parallel-delivery/SKILL.md` |
| Routage des sous-agents par capacité, coût et latence | `AGENTS.md`; `octacom-parallel-delivery/SKILL.md`; `oxygen6-frontend-quality/SKILL.md` |
| Blocage strict en cas d'information requise manquante | `AGENTS.md`; `octacom-project-start/SKILL.md`; `octacom-parallel-delivery/SKILL.md` |
| Lecture exhaustive et bloquante des annotations Figma | `AGENTS.md`; `figma-to-oxygen/SKILL.md`; `figma-to-oxygen/references/annotation-workflow.md`; skills accueil, pages internes et QA |
| Templates Single Article et 404 obligatoires sur chaque site | `AGENTS.md`; `oxygen6-architecture`; `wordpress-dynamic-content`; `oxygen6-homepage`; `oxygen6-inner-pages`; `wordpress-oxygen-qa` |
| Conversion obligatoire des rasters en WebP et usage maximal obligatoire du SVG pour les formes/illustrations vectorielles, sauf contrainte technique démontrée | `AGENTS.md`; `figma-to-oxygen`; `oxygen6-frontend-quality`; `wordpress-oxygen-qa` |

## Contrôles de non-perte

1. Le snapshot reste inchangé et son SHA-256 doit correspondre à la valeur ci-dessus.
2. Chaque plage contenant une instruction apparaît dans la matrice.
3. Chaque référence est liée depuis son `SKILL.md`.
4. Tous les skills possèdent un frontmatter valide et un nom identique à leur dossier.
5. Le fichier racine reste sous la limite de découverte usuelle de 32 Kio.

Les références conservent le fond des règles historiques. Les normalisations post-migration sont documentées : correction du chemin relatif du template de Mentions légales, obligation renforcée des Templates Oxygen Single Article et 404 sur chaque site, attribution au client ou à son conseil de la décision d'applicabilité des CGV, harmonisation de la QA avec la matrice responsive complète incluant 480 et 1920 px, clarification des URLs fixes de l'infrastructure et des assets officiels Octacom sans autoriser le hard-coding d'un domaine public client, et renforcement bloquant de la lecture et de la validation des annotations Figma. Le texte source exact reste disponible dans le snapshot.
