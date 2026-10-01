# Contrôles du kit

- Ground : hooks, installateur, signatures MCP, configuration effective et documentation officielle examinés.
- Sketch : deux candidats indépendants, hooks locaux et proxy MCP, comparés par un troisième lecteur.
- Agree : candidat A retenu avec invalidation conservatrice et états inconnus du candidat B. Décision dans `llm-controls-synthesis.md`.
- Implement : noyau de mission, snapshots, preuves versionnées, adaptateurs Claude/OpenCode et installation isolée implémentés. Tests locaux réussis. Huit hooks Codex approuvés, treize skills découverts, injection Desktop observée.
- Vérification terminée : sept scénarios réels Codex CLI réussis sur les mêmes empreintes finales. Les refus natifs avant effet sont observés dans OpenCode, Claude Code et T3 avec chacun de ses fournisseurs Codex et Claude. Les tentatives préparatoires arrêtées ne comptent pas parmi ces preuves.
- Preuves locales : 32 tests du workflow, 22 tests du noyau de mission, 10 tests des adaptateurs et 9 tests des comparaisons réussis. L'installation NTFS passe 79 assertions. Résultats et empreintes dans `../verification/control-tests.json` ; scénarios dans `../verification/model-scenarios-consolidated.json`.
- Limite Desktop : injection du préflight observée et huit hooks approuvés dans la configuration effective. L'interception Oxygen sur fixture dans ce chat n'est pas observée. Le détail par interface reste dans `../../.agents/references/runtime-compatibility.md`.
- Scrap : mode atomique refusé faute de CAS serveur. Les essais ne doivent pas transformer des assertions locales en certification visuelle ou en frontière de sécurité.

Propriétaires : coordinateur pour contrôles/hooks et intégration ; local_controls pour le validateur et les scénarios ; openai_research pour les adaptateurs et preuves des interfaces ; anthropic_research pour les invariants documentaires et l'installation, puis revue du noyau en lecture seule.

Les essais d'activation et d'évaluation utilisent des fixtures sans accès en écriture à un site client. Une preuve sur un runtime ne vaut pas preuve sur une autre interface.
