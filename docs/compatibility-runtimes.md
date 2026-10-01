# Compatibilité des interfaces

La procédure partagée et la matrice de couverture sont dans [.agents/references/runtime-compatibility.md](../.agents/references/runtime-compatibility.md). Cette référence est livrée aux workspaces par la junction `.agents`.

Les preuves propres au dépôt sont conservées dans [runtime-interface-manifest.json](runtime-interface-manifest.json) et [verification/portable-runtimes.json](verification/portable-runtimes.json). Le manifeste distingue les adaptateurs de protocole, les hooks natifs observés et les scénarios qui demandent encore une vérification dans l'interface réelle.

Les sept conversations réelles Codex CLI sont documentées dans [la preuve consolidée](verification/model-scenarios-consolidated.json) et [la méthode d'évaluation](verification/model-scenarios.md). Les preuves [d'approbation des hooks](verification/runtime-after-approval.json) et [d'injection Desktop](verification/desktop-injection.json) restent séparées. L'interception Oxygen Desktop n'est pas observée.

Les probes et les tests se trouvent dans `scripts/probe-portable-runtimes.py`, `scripts/probe-codex-runtime.py` et `scripts/test-runtime-adapters.py`. Les scripts du kit restent dans son dépôt source, plutôt que dans chaque workspace de site.
