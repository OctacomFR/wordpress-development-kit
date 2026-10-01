# Compatibilité des interfaces d'exécution

État au 1 octobre 2026. Le kit partage ses règles et son noyau Python entre Codex CLI, Codex desktop, Claude Code et OpenCode. T3 Code utilise un fournisseur. Chaque interface conserve ses permissions, sa confiance et des chemins non couverts.

## Couverture et preuves

| Interface | Entrée du kit | Preuve disponible | Vérification restante |
| --- | --- | --- | --- |
| Codex CLI | `.codex/config.toml`, `.codex/hooks.json`, `.agents/skills` | Sept conversations réelles Codex 0.159.2 passent sur le noyau final avec le modèle demandé `gpt-6.1-sol`; révision réelle du modèle non exposée. Approbation normale du kit vérifiée séparément : huit handlers trusted et treize skills repo | Autres chemins, sous-agents, reprises et recettes sur cible confirmée |
| Codex desktop | Mêmes fichiers, runtime de l'application | Configuration après approbation observée; injection `UserPromptSubmit` reçue dans la conversation | Dispatch Oxygen et scénarios dans cette interface |
| Claude Code | `.claude/settings.json`, bridge Python, import `CLAUDE.md` | Dix tests d'adaptateurs communs; hook natif observé avec Claude Code 2.1.286 portable | Découverte et confiance automatiques du projet, car le smoke utilise `--settings` explicite |
| OpenCode | Loader `.opencode/plugins/octacom-controls.js`, module `.mjs`, `AGENTS.md` | Dix tests communs; plugin découvert et refus natif observé avec OpenCode 1.18.34 portable | Modèle réel et recettes sur cible confirmée |
| T3 Code avec Codex | Fournisseur Codex sur workspace et home confirmés | Conversation native T3 0.0.44 → Codex 0.159.2 → modèle Responses loopback → MCP de fixture; injection et refus du hook observés, aucun effet MCP | Scénarios métier et configuration effective du workspace réel |
| T3 Code avec Claude | Fournisseur Claude et fichiers projet Claude | Conversation native T3 0.0.44 → Claude 2.1.286 → modèle Anthropic loopback → MCP de fixture; hooks projet injectent le préflight et refusent l'appel, aucun effet MCP | Scénarios métier et configuration effective du workspace réel |

Un catalogue disponible ne prouve pas la lecture des skills. Un refus observé sur une fixture ne certifie pas le raisonnement d'un modèle ni un site. Une sortie silencieuse du garde laisse les permissions natives décider.

Les sept conversations CLI couvrent une édition sauvegardée puis relue, un mauvais site, des annotations absentes, un échec d'outil, un builder périmé, un conflit de sources et une demande de fidélité injustifiée. Toutes passent les assertions du grader sur le noyau final; la fidélité reste non vérifiée. Ce sont des scénarios guidés, sans site réel, et chaque blocage ne force pas une tentative adversariale contre le hook. Les preuves consolidées et leur méthode résident dans `docs/verification/model-scenarios-consolidated.json` et `docs/verification/model-scenarios.md` du dépôt source. Elles sont distinctes des preuves d'approbation et d'injection Desktop.

## Contrat partagé

Les adaptateurs appellent `.codex/hooks/oxygen_site_gate.py` et transmettent un objet JSON sur stdin. Le format commun comprend `hook_event_name`, `cwd`, `session_id`, `tool_name`, `tool_input`, `tool_response` et `tool_use_id`. Le champ `runtime` identifie l'adaptateur. Les règles de mission, domaine, version, objet, propriétaire, révision et preuve restent dans le noyau.

Le bridge trouve le workspace par `AGENTS.md` et `.codex/hooks` en remontant depuis le répertoire natif. Il garde le chemin du workspace même si `.codex` est une junction vers le kit. `.octacom` reste un dossier réel propre au workspace du site.

Avant l'outil, `hookSpecificOutput.permissionDecision = "deny"` refuse l'appel. Un blocage générique du noyau devient aussi un refus natif. Les erreurs de sous-processus et sorties JSON invalides refusent l'appel avant exécution. Après l'outil, une erreur ne peut pas annuler un effet déjà produit. Ces contrôles couvrent seulement les appels transmis par l'interface.

Les processus Python sont invoqués sans shell et avec `-B`, afin de ne pas créer de cache dans le code partagé. Claude utilise l'exécutable `python` dans ses settings. OpenCode utilise `OCTACOM_PYTHON`, ou `python` par défaut. Un environnement qui expose seulement `python3` doit fournir le bon exécutable. L'adaptateur ne copie aucun secret ni setting global.

## Claude Code

Le fichier `.claude/settings.json` enregistre `SessionStart`, `UserPromptSubmit`, `SubagentStart`, `PreToolUse`, `PostToolUse` et `PostToolUseFailure`. Il utilise la forme exécutable plus tableau `args`. Le bridge conserve l'événement d'échec avec `isError: true` et le refus natif. L'injection ajoute uniquement la politique statique du noyau. Les prompts ne deviennent pas des instructions privilégiées. [Hooks officiels](https://code.claude.com/docs/en/hooks).

`.claude/CLAUDE.md` importe `../AGENTS.md`, pour les versions et sessions où sa découverte native manque ou où un `CLAUDE.md` ancêtre prend sa place. Les instructions restent du contexte pour le modèle. La découverte native des skills demande leur emplacement Claude; le préflight peut aussi lire les fichiers `.agents/skills` explicitement. [Mémoire et imports](https://code.claude.com/docs/en/memory).

Claude lit les settings projet depuis le répertoire principal de la session. Les overrides locaux et settings gérés peuvent changer le résultat. Une session cloud avec plusieurs dépôts ne charge pas les hooks projet de chaque clone. Inspecter la configuration effective dans la session réelle. [Portée des settings](https://code.claude.com/docs/en/settings).

## OpenCode

OpenCode découvre les plugins `.js` et `.ts` dans `.opencode/plugins`. Le loader `.js` exporte le module `.mjs` du kit. Le plugin n'ajoute aucune dépendance npm. Les callbacks avant et après outil transmettent `output.args` et `input.args`. Un refus devient une exception avant l'outil. [Plugins](https://opencode.ai/docs/plugins/), [source du chargeur](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/plugin.ts).

Le plugin ajoute le rappel statique via `experimental.chat.system.transform` et au contexte de compaction. Ces API sont expérimentales. Il conserve le résumé natif et ne fournit pas un contrôle `Stop` universel. Les chemins shell directs hors callbacks ne sont pas couverts. [Signatures des hooks](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts), [chemin shell](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/prompt.ts).

OpenCode construit les noms MCP avec le nom serveur nettoyé, un underscore et le nom outil nettoyé. La transformation peut être ambiguë. Le kit demande un mapping exact des outils Oxygen et WordPress dans `.octacom/runtime-tool-map.json`. Un nom de ces familles sans mapping est refusé. Le mapping décrit une identité, sans accorder de permission. [Construction des noms MCP](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/mcp/catalog.ts).

Exemple fictif à remplacer avec le catalogue réel du connecteur :

```json
{
  "opencode": {
    "serveur_oxygen_site_info": "mcp__serveur__oxygen_site_info",
    "serveur_oxygen_edit_post": "mcp__serveur__oxygen_edit_post"
  }
}
```

Le callback après outil expose du texte rendu et des métadonnées, sans garantir un `CallToolResult` MCP brut. Le bridge conserve une enveloppe MCP si tout le texte est un objet JSON portant `content`, `structuredContent` ou `isError`. Sinon, il transmet le texte intact dans `content`. Il ne fabrique ni succès, version ni révision. Le noyau vérifie les données attendues. Une information requise perdue bloque la preuve. Le contexte retourné par le noyau, notamment l'empreinte du snapshot, est ajouté au résultat visible après observation. [Contrat après outil](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts).

Un avertissement `systemMessage` après outil reste visible à la suite du résultat. Une lecture filtrée ou un schéma inconnu reste consultable pour inventaire, sans créer de base d'écriture. Les décisions explicites `deny` ou `block` restent bloquantes. Le plugin ne dispose d'aucun événement natif d'échec d'outil vérifié : une enveloppe `isError: true` reçue après outil ne devient pas un succès. Un échec sans callback de résultat ne peut pas être enregistré par cette voie.

OpenCode charge `AGENTS.md` avec un fallback `CLAUDE.md`. Une mention textuelle ne charge pas automatiquement les fichiers référencés. Lire les skills et références pendant le préflight. [Règles officielles](https://opencode.ai/docs/rules/).

## T3 Code

T3 Code transmet le travail à un fournisseur; le kit n'ajoute pas de hooks T3 propres. Son fournisseur Codex utilise `codex app-server`, avec binaire, cwd, variables et `CODEX_HOME` configurables. La preuve conserve ces paramètres exacts. Le home partagé et le shadow home changent la configuration et l'identité disponibles. [Documentation Codex T3](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-codex.md), [lancement du fournisseur](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/provider/Layers/CodexProvider.ts).

Le fournisseur Claude utilise le Claude Agent SDK avec les sources de settings sélectionnées dans les options de conversation. Son répertoire de configuration est distinct du home Codex. Le contrôle de santé périodique désactive tous les hooks Claude. Une disponibilité du fournisseur ne valide donc pas les hooks d'une conversation. [Documentation Claude T3](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-claude.md), [options de conversation](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/provider/Layers/ClaudeAdapter.ts), [contrôle de santé](https://github.com/pingdotgg/t3code/blob/main/apps/server/src/provider/Layers/ClaudeProvider.ts).

Le probe démarre le serveur T3 natif et interroge `server.getConfig`, puis `server.refreshProviders`, via son WebSocket authentifié avec une session temporaire. La réponse confirme workspace, fournisseur, binaire et home choisis. Il crée ensuite un projet et une conversation temporaires et demande un tour par `orchestration.dispatchCommand`; une subscription observe la conversation. Les fournisseurs Codex et Claude atteignent leur modèle loopback, demandent l'outil MCP local puis transmettent le refus réel du hook au modèle. Le serveur MCP n'exécute pas l'outil. [Contrat RPC T3](https://github.com/pingdotgg/t3code/blob/main/packages/contracts/src/rpc.ts), [contrat des conversations](https://github.com/pingdotgg/t3code/blob/main/packages/contracts/src/orchestration.ts).

Les clés du modèle sont factices et locales. Le home Codex de fixture contient uniquement sa configuration loopback et la confiance des huit définitions du kit par leurs hashes exacts. Cette confiance temporaire est distincte de l'approbation utilisateur dans le kit. La fixture Claude autorise son seul serveur MCP projet dans ses settings locaux; les options de conversation SDK restent celles du fournisseur T3. Le home global est protégé en lecture seule dans cette sandbox et son app-server ne peut pas y initialiser SQLite. Aucune configuration ni identité globale n'est copiée ou changée. [États du fournisseur](https://github.com/pingdotgg/t3code/blob/main/packages/contracts/src/server.ts).

## Recette et limites

Dans le dépôt source du kit, `python scripts/test-runtime-adapters.py` exécute dix tests. Les tests de contrat utilisent les vrais adaptateurs et des sous-processus Python de fixture. Ils vérifient refus, pannes du bridge, échecs d'outils, injection, identité de workspace, settings natifs, mapping, compaction et conservation des inventaires refusés comme snapshots.

Trois tests copient aussi le vrai noyau dans un workspace temporaire. Deux vérifient toute la chaîne Claude ou OpenCode vers Python et SQLite : mission, session, site et arbre Oxygen, acceptation de la base, mutation permise, résultat puis refus sur la base invalidée. OpenCode refuse également une opération inconnue. Le troisième conserve le résultat et l'avertissement des lectures filtrées, de schéma inconnu ou erronées, puis vérifie l'absence de snapshot et le refus d'écriture. Aucun test ne cible un site ni une API de modèle réelle.

Le probe `scripts/probe-portable-runtimes.py` télécharge dans TEMP des binaires officiels npm épinglés et vérifie leur SHA-512 contre le registre. Les homes, données et caches sont temporaires. Un fournisseur HTTP déterministe sur loopback demande l'appel d'un serveur MCP local sans effet. OpenCode découvre le plugin projet et son hook refuse une mutation sans mission. Claude observe son hook et refuse la même mutation avec les settings projet explicitement transmis. Le serveur MCP n'exécute aucun de ces outils refusés. Ce smoke teste le mécanisme natif, sans login ni coût de modèle. [Installation OpenCode](https://opencode.ai/docs), [installation Claude](https://code.claude.com/docs/en/setup), [installation T3](https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md).

Ce probe vise Windows x64 et exige Python, Git, un Node avec WebSocket natif et Codex sur PATH. Il utilise `full-access` uniquement dans les conversations de fixture temporaires pour que les permissions natives ne masquent pas le refus du noyau. Il ne change pas les permissions d'un workspace réel. Son code de retour échoue si l'une des quatre voies natives testées ne refuse pas l'appel ou si la fixture constate son exécution.

Les preuves propres au kit vivent dans `docs/verification/portable-runtimes.json`, `docs/verification/model-scenarios-consolidated.json`, `docs/verification/model-scenarios.md`, `docs/verification/runtime-after-approval.json`, `docs/verification/desktop-injection.json` et `docs/runtime-interface-manifest.json` du dépôt source. Ces fichiers ne sont pas requis dans un workspace de site. Cette référence partagée reste accessible via `.agents/references/runtime-compatibility.md`.

Pour chaque interface et fournisseur, la recette réelle conserve version, workspace, configuration effective, confiance et événements observés. Vérifier injection, refus sans mission, lecture d'identité suivie d'une action permise, mauvais domaine, mauvaise version, mauvaise ressource, preuve périmée et invalidation après mutation. Utiliser un connecteur de fixture sans effet externe tant qu'aucune cible de site n'est confirmée. Les journaux excluent credentials, prompts et arguments sensibles.

La découverte d'un plugin, la disponibilité d'un fournisseur et un succès sur fixture sont des preuves distinctes. Le front, Figma, le builder, les formulaires et les autres barrières demandent leurs preuves métier sur une cible confirmée.
