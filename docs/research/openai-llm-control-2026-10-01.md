# Contrôle d'un agent Codex : documentation officielle OpenAI

Recherche vérifiée le 1er octobre 2026 pour l'audit du kit WordPress et Oxygen. Cette note explique les mécanismes documentés. Elle ne certifie ni la configuration active de ce poste, ni l'exécution de ses hooks, ni la conformité d'un site.

Skills appliqués : `skill-gate`, `openai-docs`, `technical-writing` et `unslop`. Recherche web explicite, pages officielles effectivement ouvertes. Aucun MCP de documentation OpenAI disponible dans la session. Les sources retenues appartiennent à `developers.openai.com` ou `learn.chatgpt.com`.

## 1. AGENTS.md possède une découverte, une hiérarchie locale et un plafond

Codex construit la chaîne d'instructions au démarrage. Il lit d'abord le guide global, puis un fichier par dossier entre la racine du projet et le répertoire courant. Dans chaque dossier, `AGENTS.override.md` passe avant `AGENTS.md`, puis viennent les noms de repli configurés. Les fichiers plus proches du répertoire courant apparaissent plus tard et remplacent les consignes locales antérieures. Le plafond combiné `project_doc_max_bytes` vaut 32 KiB par défaut. [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

Conséquence pour le kit, par déduction : la présence d'un fichier dans Git ne prouve pas son inclusion dans le prompt. L'audit doit identifier les fichiers réellement découverts et mesurer leur taille combinée. Des références Markdown ne sont pas assimilables à leur lecture intégrale. La priorité décrite ici concerne les guides locaux, pas une permission de remplacer les instructions du runtime.

Limite : la documentation décrit une découverte au lancement, particulièrement explicite pour le TUI. Elle ne démontre pas comment cette conversation desktop a injecté ses instructions. Une incohérence demeure : le guide AGENTS.md parle de taille combinée, alors qu'Advanced Configuration décrit une quantité lue par fichier. Le budget est exprimé en octets, distincts des tokens. La vérification de la chaîne réellement chargée reste nécessaire. [Advanced Configuration, Project instructions discovery](https://learn.chatgpt.com/docs/config-file/config-advanced#project-instructions-discovery)

## 2. Le catalogue de skills et leurs instructions sont deux étapes distinctes

ChatGPT et Codex commencent par les noms et descriptions. Ils chargent le `SKILL.md` complet lorsqu'ils sélectionnent un skill. Dans Codex, le catalogue initial contient aussi les chemins. Son budget par défaut vaut 2 % de la fenêtre de contexte, ou 8 000 caractères si sa taille est inconnue. Codex raccourcit les descriptions puis peut omettre des skills avec avertissement. La sélection explicite et la sélection implicite existent. `agents/openai.yaml` peut définir `allow_implicit_invocation: false`. [Build skills](https://learn.chatgpt.com/docs/build-skills)

La clé `skills.max_context_tokens` est reconnue. Une valeur explicite positive remplace le budget par défaut, avec un plafond de 10 000 tokens. Une configuration `[skills] max_context_tokens = 10000` est donc documentée. Les projets non approuvés ignorent cependant leur couche `.codex/`, dont la configuration locale, les hooks et les règles. [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)

Conséquence pour le kit, par déduction : afficher le catalogue ne prouve aucune lecture métier. Un préflight déclaratif améliore le routage mais doit être évalué sur les ouvertures effectives des fichiers. Les descriptions doivent rester spécifiques et courtes.

OpenAI recommande des routeurs minimaux et une lecture adaptée à la tâche. L'article vise particulièrement GPT-6 Astra et avertit que des règles utiles pour d'autres modèles peuvent le contraindre excessivement. [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)

Limite : aucune source ne garantit qu'un skill sélectionné sera compris ou exécuté correctement.

## 3. Les hooks ont une confiance explicite et une couverture partielle

Les hooks non gérés nécessitent la confiance de leur définition exacte. Une modification de hash impose une nouvelle revue. Les hooks projet exigent aussi un projet approuvé. `/hooks` expose la revue dans le CLI. `PreToolUse` peut bloquer ou réécrire les appels supportés. `PostToolUse` intervient après exécution et n'annule pas leurs effets.

La couverture inclut shell, `exec_command`, `apply_patch`, MCP et la plupart des fonctions locales. Les outils hébergés tels que `WebSearch` sont exclus. Certains chemins spécialisés peuvent échapper aux hooks. Les décisions s'appliquent aux appels imbriqués JavaScript en code mode. Un refus pré-exécution rejette leur promesse. `Stop` peut relancer un tour. Les hooks MCP utilisent une connexion existante et leurs erreurs ne bloquent pas. La documentation avertit que les hooks ne forment pas une frontière complète. [Hooks](https://learn.chatgpt.com/docs/hooks)

Conséquence pour le kit, par déduction : `functions.exec` n'est pas, à lui seul, un contournement établi. La preuve doit tester chaque chemin réel, l'activation et la confiance. Une injection de rappel ne prouve pas l'application du skill.

Limite : le comportement documenté dépend du runtime et de son orchestration locale ou cloud.

## 4. La politique MCP configurée est distincte des consignes du guide

Le guide MCP Codex CLI documente `enabled_tools`, `disabled_tools`, un serveur `required`, et les modes d'approbation `auto`, `prompt`, `writes` et `approve`. La liste d'exclusion s'applique après la liste d'autorisation. Le mode `writes` demande une approbation pour les outils qui ne sont pas marqués en lecture seule. [Model Context Protocol, surface CLI](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)

Conséquence pour le kit, par déduction : écrire "utiliser uniquement le connecteur du site" reste une consigne au modèle tant qu'aucune restriction de runtime ou de serveur n'interdit les autres destinations. Les annotations d'outils doivent correspondre aux effets réels.

Les annotations MCP renseignent les protections client. Elles ne donnent aucune permission et ne remplacent ni l'authentification, ni l'autorisation, ni les contrôles de périmètre, ni la validation des entrées. OpenAI demande aussi d'exposer séparément chaque opération appelable par le modèle. [Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines)

Limite : ces champs CLI ne prouvent pas la politique active dans l'application desktop. Aucun réglage du poste n'a été modifié.

## 5. La découverte des outils dépend de l'API et du client

Avec Responses, le MCP distant peut produire `mcp_list_tools`, contenant les définitions effectivement importées. `allowed_tools` filtre les imports. Les approbations utilisent `mcp_approval_request` et peuvent être configurées par `require_approval`. [MCP servers](https://developers.openai.com/api/docs/guides/tools-connectors-mcp)

Tool search peut différer les schémas. Une fonction individuelle différée garde initialement son nom et sa description. Un serveur ou namespace différé expose initialement sa description collective. Agents API et Responses n'utilisent pas exactement la même configuration de découverte MCP. [Tool search](https://developers.openai.com/api/docs/guides/tools-tool-search)

Conséquence pour le kit, par déduction : le catalogue visible dans la conversation et les définitions chargées ne sont pas nécessairement identiques. Il faut inspecter les capacités et schémas disponibles avant l'appel, puis vérifier le résultat. La règle du kit est cohérente avec cette séparation.

Limite : cette recherche ne démontre pas les mécanismes internes de `ALL_TOOLS` ni du chargeur spécifique de cette session.

## 6. Un schéma strict contrôle la forme, pas la vérité métier

`strict: true` contraint les arguments d'une fonction à son schéma. Les objets exigent `additionalProperties: false` et leurs propriétés doivent être requises. Dans Responses, l'absence de `strict` peut conduire à une normalisation, ou à un repli non strict si le schéma est incompatible. [Function calling](https://developers.openai.com/api/docs/guides/function-calling)

OpenAI précise que Structured Outputs peut encore contenir des erreurs. Un schéma peut même encourager une hallucination si l'entrée ne correspond pas à la tâche. [Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

Conséquence pour le kit, par déduction : un ID entier valide n'établit ni le bon site, ni l'existence de la page, ni son propriétaire. Un champ `verified: true` généré par le modèle n'établit aucune vérification. La concordance site, version, objet, révision et permissions doit être contrôlée par des données réelles et, si une garantie est exigée, par du code qui interdit l'opération invalide.

## 7. La priorité des contenus ne remplace pas celle des messages

La documentation API place les messages `developer` avant les messages `user`. Le paramètre Responses `instructions` est prioritaire sur le prompt `input`. Avec `previous_response_id`, les anciennes valeurs de `instructions` ne sont pas automatiquement reportées au prochain appel. [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)

OpenAI décrit l'injection comme une tentative de texte non fiable de modifier les instructions. La documentation recommande de garder ces données hors des messages développeur, d'extraire des champs structurés et de limiter leur influence sur les appels d'outils. Elle reconnaît que ces mesures n'éliminent pas tous les risques. [Safety in building agents](https://developers.openai.com/api/docs/guides/agent-builder-safety)

Conséquence pour le kit, par déduction : Figma, ERP, pages web et sorties MCP peuvent être des preuves métier sans devenir des autorités capables de changer le périmètre. L'ordre des sources du kit doit être compris dans les limites des permissions et instructions supérieures.

Limite : la recommandation d'approbation de cette page concerne Agent Builder. Elle n'impose pas une nouvelle approbation universelle dans ce chat Codex.

## 8. La compaction conserve un état utile sans fournir un registre auditable complet

Responses documente une compaction qui réduit le contexte en conservant l'état nécessaire à la suite. L'élément compacté peut être chiffré, opaque et non interprétable par un humain. Le chaînage manuel et `previous_response_id` ont des règles de conservation différentes. [Compaction](https://developers.openai.com/api/docs/guides/compaction)

Conséquence pour le kit, par déduction : une barrière critique fondée uniquement sur la mémoire du chat n'est pas une preuve durable. Un registre externe peut conserver l'identité de la cible, les sources, les décisions, les révisions et les artefacts attendus. Après compaction, une nouvelle lecture ciblée peut résoudre l'état réel.

Limite : la page décrit Responses. Elle ne certifie ni l'algorithme de résumé de Codex desktop ni la conservation intégrale de chaque règle. Ce document ne prétend pas que la compaction efface forcément une instruction précise.

## 9. Le suivi des instructions, le choix d'outil et les arguments se mesurent séparément

OpenAI décrit l'IA générative comme variable. Les évaluations doivent fixer un objectif, des données représentatives, des métriques, puis comparer et répéter. Pour un agent, la documentation distingue suivi des instructions, correction fonctionnelle, sélection d'outil et précision des arguments. Elle recommande des cas ordinaires, limites et adversariaux, et une calibration humaine. [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

Conséquence pour le kit, par déduction : "le modèle a annoncé le préflight" est un indicateur faible. Des traces peuvent vérifier l'ordre lecture puis mutation, le connecteur retenu, l'ID transmis et le blocage devant une annotation inaccessible. Les contrôles déterministes doivent rester séparés du jugement visuel ou sémantique.

Limite : un taux de succès sur un jeu fini n'est pas une garantie universelle. La page annonce une dépréciation de la plateforme Evals, avec passage en lecture seule le 31 octobre 2026 et arrêt prévu le 30 novembre 2026. Les principes d'évaluation ne dépendent pas de ce service.

## 10. Les guides de workflow et l'exécution du serveur ont des responsabilités différentes

Un skill enseigne le workflow. Le MCP publie des capacités et exécute les opérations. Le client découvre les outils, le modèle choisit l'appel, puis le serveur valide et réalise l'opération. [MCP server](https://developers.openai.com/plugins/concepts/mcp-server)

Conséquence pour le kit, par déduction : les règles "ne jamais inventer", "un propriétaire par objet" et "site confirmé avant mutation" gagnent à avoir des contrôles serveur quand elles conditionnent une écriture importante. Les critères visuels, éditabilité et contenu restent des vérifications sur les artefacts réels. Leur résultat ne devient pas vrai parce que l'agent respecte le format d'un rapport.

Limite : aucune source ouverte ne promet une fidélité Figma à 100 %, un contrôle sémantique complet par les hooks ou une exécution parfaite d'AGENTS.md.

## Redirections observées et portée de la recherche

Les anciennes URLs ont été réellement ouvertes. Leurs destinations au jour de la recherche sont les suivantes :

| URL demandée | Destination observée |
| --- | --- |
| `developers.openai.com/codex/guides/agents-md` | `learn.chatgpt.com/docs/agent-configuration/agents-md` |
| `developers.openai.com/codex/skills` | `learn.chatgpt.com/docs/build-skills` |
| `developers.openai.com/codex/hooks` | `learn.chatgpt.com/docs/hooks` |
| `developers.openai.com/codex/mcp` | `learn.chatgpt.com/docs/extend/mcp?surface=cli` |
| `developers.openai.com/api/docs/guides/tools-remote-mcp` | `developers.openai.com/api/docs/guides/tools-connectors-mcp` |

Cette note ne contient aucun patch. Elle ne vérifie pas la version du runtime installé, ses valeurs de configuration, la confiance effective des hooks, les permissions d'un connecteur WordPress, ni la couverture des hooks par des appels réels. Ces éléments demandent une inspection ou des essais locaux distincts. Aucun outil métier d'un site n'a été appelé.

