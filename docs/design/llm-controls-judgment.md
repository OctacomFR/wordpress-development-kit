# Jugement des propositions de contrôle LLM

Revue du 1er octobre 2026 par l'agent `local_controls`, modèle hérité. Les deux [propositions A](llm-controls-candidate-a.md) et [B](llm-controls-candidate-b.md) ont été lues intégralement. Skills appliqués : `skill-gate`, `technical-writing`, `unslop`. Aucune nouvelle famille de modèle n'était disponible pour une comparaison indépendante entre familles. Cette revue juge les propositions, pas une implémentation livrée.

La base recommandée est A. Elle peut améliorer les refus et la fraîcheur des preuves avec les composants locaux déjà présents. B décrit mieux une frontière d'exécution indépendante, mais son endpoint upstream, ses credentials réservés et le retrait des routes directes ne sont pas acquis. La création de cette infrastructure dépasse l'amélioration locale du kit.

## Scores selon le rubric

Chaque critère vaut de 0 à 2. Deux points indiquent une réponse explicite et compatible avec l'objectif. Un point indique un mécanisme utile qui reste à préciser. Zéro indique une dépendance majeure non disponible pour le périmètre actuel.

| Critère | A | B | Motif |
|---|---:|---:|---|
| Réalisable avec runtime et MCP exposés | 2 | 0 | A adapte les scripts et hooks déjà présents. B exige un service indépendant et une route MCP exclusive dont la disponibilité n'est pas démontrée. |
| Refus précis de domaine, version, objet et révision, sans fausse sécurité | 2 | 2 | Les deux refusent les identités incomplètes et distinguent observation locale et révision atomique. A nomme les champs réels `site_url` et `builder_version`. B refuse explicitement le mode strict sans capacité distante. |
| Preuves versionnées et invalidation conservatrice | 1 | 2 | A invalide les consommateurs connus et bloque si le graphe manque, mais ne définit pas une invalidation globale simple pour toutes les dépendances inconnues. B invalide alors la mission entière. |
| État isolé du workspace et concurrence | 1 | 2 | A sépare `.octacom` des jonctions et prévoit SQLite, mais l'identité d'appel et d'acteur exploitable reste ouverte. B définit un registre privé, des acteurs liés au canal et des transitions transactionnelles. Sa faisabilité d'installation est déjà pénalisée au premier critère. |
| Périmètre et entretien limités | 2 | 0 | A conserve les contrôles locaux et le helper existant. B ajoute un service, un plan de contrôle, des credentials privés et une nouvelle configuration des routes. |
| Smoke et évaluation fondés sur traces et effets | 2 | 2 | Les deux demandent dispatch réel, appels imbriqués, état de fixture et scénarios adversariaux. B formule des critères précis de zéro effet après refus et de reprise sans doublon. |
| Total | **10/12** | **8/12** | Base A avec les règles conservatrices de B. |

## Greffes retenues

Conserver le mode `atomic_revision` de A, mais le traiter comme une capacité positive à démontrer. L'absence de CAS ou de verrou distant coopérant doit produire un refus explicite. Le mode d'observation doit nommer sa fenêtre de course. Ni SQLite, ni un hash, ni une relecture avant écriture ne rendent la mutation WordPress atomique.

Reprendre l'invalidation de la mission entière de B lorsque les consommateurs d'un objet global ne sont pas inventoriés. L'invalidation précède l'effet tenté. Un résultat inconnu conserve les preuves périmées et empêche la conclusion. Une nouvelle lecture permet une réconciliation, sans transformer l'absence d'erreur en preuve de sauvegarde.

Reprendre la distinction de B entre résultat confirmé et résultat inconnu après crash. Une déduplication locale empêche deux dispatchs locaux identiques si l'identité est fiable. Elle ne garantit pas un effet distant unique après perte de réponse. Aucun retry automatique d'une mutation inconnue sans idempotence upstream ou preuve univoque de l'effet.

Reprendre les critères d'évaluation de B : zéro appel de fixture après refus, aucun bundle périmé accepté, conflit observable et reprise sans doublon. Le verdict utilise les appels, arguments expurgés, décisions et état réel des fixtures. Le texte final du modèle ne suffit pas.

## Réserves à résoudre dans la synthèse

La [sonde runtime conservée](../verification/runtime-before.json) contient `hooks=true`, huit handlers `enabled` et `trusted`, et treize skills repo actifs. Elle prouve la découverte et l'approbation rapportées par l'app-server. Elle ne prouve pas l'interception avant effet. Un smoke d'action inoffensive doit vérifier cette frontière avant toute annonce de couverture runtime.

A est formulé principalement autour des événements Codex et de son app-server. Les cinq runtimes demandés ne possèdent pas encore dans cette proposition une matrice d'adaptateurs ni des preuves de dispatch. Le noyau peut être portable. La couverture de chaque bridge exige son contrat d'événement, son format de refus, son comportement sur erreur et timeout, et son smoke. Un runtime sans bridge validé reste explicitement non couvert.

L'identité des acteurs ne doit pas venir d'un `agent_id` fourni librement dans une fiche. Si un runtime expose seulement une session partagée, les sous-agents demeurent en lecture seule sur les mutations gardées, comme le prévoit A. L'identité des appels nécessaire à la reprise doit également être observée ou remplacée par une règle de sérialisation explicite, sans revendiquer une déduplication universelle.

Les versions locales ne remplacent pas les versions distantes. L'état peut invalider les effets qu'il observe. Les changements WordPress par builder, HTTP ou autre runtime exigent une nouvelle observation et demeurent une limite lorsque le serveur ne fournit pas de révision atomique.

Le registre vérifie les pièces et leurs empreintes. Il ne prouve pas l'origine Figma ou navigateur de PNG arbitraires. La revue visuelle et le registre des écarts clos restent requis. Un champ `verified=true` ne peut pas franchir seul une barrière de livraison.

## Décision proposée

Sélectionner A pour le kit actuel, garder B comme architecture future si une frontière indépendante des agents devient requise et disponible. Greffer immédiatement l'invalidation globale conservatrice, les états inconnus et les critères de traces de B. La capacité `atomic_revision` reste refusée tant que son contrat distant n'est pas démontré. L'activation de chaque runtime reste conditionnée à un smoke réel de son bridge.
