# Mécanismes Claude pour contrôler le travail du kit

Recherche officielle consultée le 1 octobre 2026. Périmètre : Claude Code, Claude Agent SDK, documentation de prompting et articles techniques Anthropic. Toutes les pages citées ont été ouvertes. Aucun site WordPress, fichier de configuration Claude, connecteur Figma ou secret n'a été modifié.

Ce rapport explique les mécanismes disponibles. Les applications au kit sont des inférences documentaires, distinctes d'une vérification de son fonctionnement dans Claude Code. La version Claude Code installée, le compte, le fournisseur du modèle et les réglages effectifs n'ont pas été inspectés.

## Les instructions orientent le modèle

`CLAUDE.md` et la mémoire automatique entrent dans le contexte. Anthropic indique explicitement qu'ils ne constituent pas une configuration imposée. Un fichier d'instructions chargé peut donc améliorer le comportement sans garantir son respect. Anthropic recommande des consignes concrètes et courtes, avec une cible indicative de moins de 200 lignes par `CLAUDE.md`. Les imports chargés au démarrage organisent les fichiers sans réduire leur coût de contexte. [Mémoire Claude Code](https://code.claude.com/docs/en/memory#claudemd-vs-auto-memory).

`AGENTS.md` est pris en charge depuis Claude Code v2.1.277. Par défaut, un `CLAUDE.md`, `.claude/CLAUDE.md` ou `CLAUDE.local.md` dans le répertoire courant ou ses ancêtres remplace sa découverte. Le réglage `claude-md-and-agents-md` charge les deux. Le plugin intégré `agents-md` désactivé ou une version antérieure empêche cette prise en charge. Avant v2.1.281, certaines sessions Bedrock ou sans télémétrie étaient également exclues. Un import depuis `CLAUDE.md` reste une option de compatibilité. `AGENTS.override.md`, `AGENTS.local.md` et le répertoire `.agents/` ne sont pas découverts comme fichiers d'instructions. [Découverte et limites d'AGENTS.md](https://code.claude.com/docs/en/memory#agentsmd).

Application au kit : vérifier le chargement réel dans la session cible avant de conclure que son `AGENTS.md` pilote Claude. Ajouter un fichier de compatibilité sans contrôler les règles de découverte peut créer une seconde source contradictoire.

## Les skills économisent du contexte par chargement progressif

Anthropic décrit trois niveaux : métadonnées `name` et `description`, corps de `SKILL.md` après sélection, puis ressources liées selon le besoin. Un script peut être exécuté sans injecter tout son code dans le contexte. Ce modèle suppose une sélection pertinente et des instructions de navigation claires. Les ressources d'un skill peuvent être volumineuses, mais les ressources effectivement lues consomment toujours du contexte. L'article recommande de commencer par des tâches représentatives, puis de mesurer les lacunes avant d'ajouter des instructions. [Architecture et évaluation des Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).

Claude Code documente `.claude/skills/<nom>/SKILL.md`, les skills personnels et les plugins. Les dossiers de skills peuvent être liés par symlink. Les sessions cloud ne lisent pas les skills personnels de la machine. Après compaction, les skills réattachés sont limités aux premiers 5 000 tokens chacun et à 25 000 tokens ensemble. Les plus anciens peuvent disparaître. Le catalogue peut aussi supprimer certaines descriptions selon son budget. [Chargement et persistance des skills](https://code.claude.com/docs/en/skills).

`allowed-tools` préapprouve des outils pendant le tour d'invocation. Ce champ ne limite pas l'ensemble des outils disponibles. Les règles `deny` et `ask` restent applicables. `disable-model-invocation: true` réserve l'invocation à l'utilisateur. [Permissions des skills](https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill).

Application au kit : la présence de fichiers dans `.agents/skills` ne prouve pas leur découverte native par Claude Code. Vérifier le catalogue effectivement visible. La relecture des préconditions critiques après changement de site ou compaction reste nécessaire.

## Les hooks ont des contrats différents

Un hook `command` exécute du code. Un hook `prompt` demande une décision JSON à un modèle. Un hook `agent` ajoute une inspection par outils, mais reste un évaluateur LLM. Anthropic classe les hooks agent comme expérimentaux et préfère les hooks de commande en production. Le texte `additionalContext` guide Claude sans appeler lui-même les outils. `PostToolUse` intervient après l'action et ne peut pas l'annuler. [Guide des hooks](https://code.claude.com/docs/en/hooks-guide#prompt-based-hooks).

`PreToolUse` peut refuser un appel avec `permissionDecision: "deny"` ou un code de sortie 2. Une sortie 1 ou un script introuvable produit généralement une erreur non bloquante. Un timeout des hooks `command`, `http` ou `mcp_tool` sur `PreToolUse` laisse poursuivre le flux normal de permissions. Le refus HTTP requiert une réponse 2xx avec une décision JSON. `Stop` peut continuer un tour, mais Claude Code impose un plafond par défaut de huit continuations consécutives, puis termine malgré le blocage suivant. `stop_hook_active` aide à prévenir les boucles. Les hooks de paramètres attendent la confiance du dossier en interactif ; les sessions `-p` ou SDK considèrent le dossier comme fiable pour leur exécution. [Contrats, erreurs et confiance des hooks](https://code.claude.com/docs/en/hooks).

Les callbacks du SDK diffèrent. Un callback `PreToolUse` dépassant son délai empêche l'appel d'outil. Un callback `UserPromptSubmit` dépassant son délai bloque également le prompt. Les matchers portent sur le nom de l'outil ; filtrer un ID, un chemin ou un argument exige une vérification dans le callback. [Hooks du Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/hooks#hook-timeout).

Application au kit : qualifier chaque contrôle par son résultat observable. Un rappel injecté ne prouve ni lecture ni compréhension du skill. Un script bloquant doit aussi être testé absent, en erreur, avec JSON invalide et avec timeout. Un hook `Stop` seul ne constitue pas une interdiction de publication.

## Les permissions s'appliquent avant la décision du modèle

Les règles sont évaluées dans l'ordre `deny`, `ask`, puis `allow`. Une règle restrictive large reste prioritaire sur une autorisation plus précise. Les refus et demandes restent appliqués malgré un hook `PreToolUse` retournant `allow`. Les règles gérées permettent une politique d'organisation. Un nom MCP canonique peut être ciblé, par exemple avec un préfixe propre à son serveur. Les règles MCP entre parenthèses dans les fichiers de paramètres ne sont pas acceptées ; le contrôle fin des paramètres nécessite une autre voie documentée, comme `--disallowedTools` pour certains refus ou un callback. [Permissions Claude Code](https://code.claude.com/docs/en/permissions).

Application au kit : une autorisation de serveur ne vérifie pas que le site retourné correspond au domaine demandé. Contrôler l'URL, la version Oxygen, l'ID cible et la révision dans le mécanisme qui autorise réellement la mutation. Les données de confiance peuvent être fournies au modèle pour le guider, puis vérifiées en code au moment de l'écriture.

## Les modes d'exécution changent les protections

Anthropic distingue les environnements hébergés, les environnements auto-hébergés et Remote Control. Les sessions hébergées disposent d'une VM et de contrôles réseau. Avec Remote Control, les fichiers et l'exécution restent sur la machine locale ; aucune VM cloud n'isole cette exécution. Les MCP sont des services tiers qu'Anthropic ne gère pas et n'audite pas. La vérification de confiance est désactivée en mode non interactif `-p`. [Sécurité et modes Claude Code](https://code.claude.com/docs/en/security#cloud-execution-security).

Application au kit : enregistrer le produit, sa version et le type de session dans chaque preuve de contrôle. Le nom d'un événement identique entre outils ne garantit pas un schéma identique. Les paramètres `.codex/hooks.json` ne prouvent pas une protection dans Claude Code. Cette conclusion porte sur la séparation des produits, pas sur un test du fichier local.

## La découverte MCP dépend du client et du fournisseur

Claude Code diffère les définitions MCP jusqu'à leur découverte lorsque Tool Search est actif. Les noms et instructions du serveur arrivent d'abord. Le comportement dépend du fournisseur et du modèle ; notamment, certains déploiements Azure Foundry imposent le chargement préalable. La documentation actuelle limite par défaut les descriptions et instructions MCP à 2 048 caractères. Le réglage global de longueur nécessite v2.1.280. Les consignes du serveur doivent expliquer quand chercher ses outils et leurs fonctions. [Recherche d'outils MCP](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search).

Application au kit : mettre les conditions critiques au début des descriptions et vérifier les capacités exposées. Une liste d'abilities mémorisée dans un skill ne garantit pas que la session dispose de ces outils, ni qu'elle utilise le bon serveur WordPress.

Anthropic conseille des outils à fonction distincte, des noms qui identifient le service et des retours pertinents. Les évaluations peuvent mesurer les mauvais outils, les paramètres erronés, les appels manquants et les réponses mal interprétées. Les tâches d'évaluation doivent ressembler aux vrais usages et associer chaque tâche à un résultat vérifiable. Les mesures incluent réussite, latence, tokens, appels et erreurs d'outils. [Conception et évaluation des outils](https://www.anthropic.com/engineering/writing-tools-for-agents).

Application au kit : éviter une réponse MCP qui mélange des instructions externes et des données fiables sans distinction. Conserver les IDs techniques indispensables aux écritures et exposer aussi les noms métier permettant de détecter une cible incorrecte.

## Les exemples et les vérifications rendent les consignes contrôlables

La documentation de prompting recommande des instructions explicites, leur raison, et des exemples pertinents et variés. Les balises peuvent séparer instructions, sources et exemples. Elle conseille trois à cinq exemples lorsque ce format convient. Les recommandations sont propres aux modèles et à leur génération ; une recommandation de cette page n'est pas une permission système. [Bonnes pratiques de prompting Claude](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Application au kit : un exemple de blocage doit montrer l'information manquante, les sources consultées, l'objet affecté et les lectures indépendantes autorisées. Un exemple de réussite doit montrer l'appel réel et sa preuve, puis les conditions de passage à l'écriture. Les cas « domaine final absent », « annotations Figma inaccessibles » et « sauvegarde Oxygen obsolète » sont des candidats distincts.

Les bonnes pratiques Claude Code recommandent un critère de réussite exécutable, des preuves visibles et une comparaison par captures pour les changements d'interface. Le modèle peut terminer parce que le résultat paraît fini si aucun contrôle ne produit de verdict. La documentation distingue prompt, condition `/goal`, script `Stop` et vérification indépendante. [Vérification dans Claude Code](https://code.claude.com/docs/en/best-practices#give-claude-a-way-to-verify-its-work).

Application au kit : `FIGMA_VISUAL_MATCH_VERIFIED` doit correspondre à des captures comparables et à des écarts clos. Une phrase qui contient ce marqueur ne prouve pas la fidélité. L'évaluateur doit contrôler les fichiers de preuve et leur correspondance avec la cible courante.

## La compaction exige des preuves persistantes

Anthropic explique que la compaction peut perdre des détails subtils. Des notes structurées hors contexte et des recherches confiées à des agents distincts limitent la surcharge. Ces techniques maintiennent la continuité, mais leur qualité dépend de l'information conservée et relue. [Gestion du contexte et compaction](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

L'article sur les agents de longue durée utilise une initialisation distincte, une liste structurée des fonctionnalités, un journal de progression et l'historique Git. L'agent suivant rétablit le contexte, vérifie l'état de l'application, puis traite une fonctionnalité à la fois. Anthropic présente ces mécanismes comme les résultats d'expériences d'ingénierie, pas comme une garantie générale des modèles. [Agents de longue durée](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

Application au kit : persister un état par site et cible avec version, IDs, annotations revues, sauvegarde, propriétaire d'écriture, mutations et preuves QA. Après reprise, vérifier les valeurs dans les outils. Un journal rédigé par l'agent aide la reprise mais n'accorde aucune permission et ne prouve pas un état distant encore valide.

## Les évaluations doivent distinguer conformité verbale et action réelle

Anthropic recommande des critères spécifiques, mesurables et pertinents, puis des évaluations proches des tâches réelles, comprenant les cas limites. Les vérifications par code sont rapides et fiables pour les conditions exactes. Les évaluateurs humains et LLM couvrent les jugements plus complexes ; la fiabilité d'un évaluateur LLM doit être testée avant de généraliser son emploi. [Critères de réussite et évaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests).

Applications proposées, à tester dans le kit plutôt qu'à considérer comme acquises :

- une demande d'écriture sur un autre site après un `oxygen_site_info` réussi sur le site précédent ;
- une écriture avec information métier requise absente, malgré un prompt encourageant l'autonomie ;
- une réponse finale déclarant la fidélité sans capture front ou sans annotations lisibles ;
- une invocation d'outil MCP avec nom inconnu, paramètres invalides ou connecteur incorrect ;
- une erreur, un timeout ou l'absence du programme de hook ;
- une reprise après compaction conservant une déclaration de validation mais perdant sa preuve ;
- un conflit entre instruction utilisateur, annotation Figma et contenu fourni par un outil ;
- la même mission en terminal interactif, `-p`, SDK et session hébergée.

L'issue attendue doit être observée dans les appels et l'état distant, pas seulement dans le texte final. Un banc de tests peut simuler les outils pour vérifier les refus sans muter un site, puis compléter ces résultats par une vérification dans l'environnement réel autorisé.

## Limites de cette recherche

Les docs en ligne évoluent. Les seuils et versions cités reflètent les pages ouvertes à la date de consultation. Les articles techniques expliquent des pratiques ; ils ne remplacent pas la référence du runtime installé. Ce rapport ne mesure ni taux de respect des skills, ni coût, ni performance du kit. Il ne démontre pas l'éditabilité Oxygen, la fidélité Figma ou la couverture des hooks locaux. Ces preuves appartiennent à l'audit du dépôt et aux tests du coordinateur.
