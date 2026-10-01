# WordPress development kit

Kit Octacom pour les projets WordPress et Oxygen 6.x.

Le dépôt du kit reste séparé des sites développés. Vous le clonez une fois, puis son installateur relie les règles et adaptateurs partagés à chaque workspace de développement. L'état de mission `.octacom` reste un dossier réel propre au workspace, sans lien vers le kit.

## Comprendre les dossiers

| Dossier | Rôle |
|---|---|
| `C:\Users\DEV\Documents\Octacom\wordpress-development-kit` | Clone de référence du kit. Les mises à jour se font ici avec Git. |
| `C:\Users\DEV\Documents\Octacom\Sites\nom-du-site` | Workspace séparé dans lequel se déroule le développement d'un site. |
| Répertoires globaux de Codex | Outils et skills personnels disponibles dans tous les projets du développeur. |

Ne placez pas un workspace de site dans le clone du kit. Ne déplacez pas le clone après avoir installé des workspaces, car les liens Windows utilisent son chemin absolu.

Codex CLI, Codex Desktop, OpenCode, Claude Code et T3 doivent chacun suivre [la procédure de compatibilité et d'activation](docs/compatibility-runtimes.md). Vérifier l'interface réellement utilisée ; la présence d'un adaptateur ou la réussite dans Codex CLI ne prouve pas son activation dans une autre interface.

## Installer les prérequis Windows

Installez ces outils au niveau global du poste :

- [Git pour Windows](https://git-scm.com/download/win), nécessaire pour cloner le kit et créer la racine Git des workspaces ;
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli?translationFallback=fr-FR), nécessaire pour lancer l'agent dans le projet ;
- [Chat GPT Desktop](https://chatgpt.com/fr-FR/download/) ou [T3 code](https://t3.codes/download), facilement contrôler les agents avec une ui ;
- la dernière version LTS de [Node.js](https://nodejs.org/en/download), avec `npm` et `npx`, nécessaire pour installer les skills externes et exécuter certains MCP ;
- [Python pour Windows](https://www.python.org/downloads/windows/) 3.11 ou plus récent, accessible par `python.exe`, nécessaire aux hooks et aux tests du kit ;
- la dernière version stable de [FFmpeg](https://ffmpeg.org/download.html), installée globalement et ajoutée au `PATH`, nécessaire au traitement des vidéos et de certains médias ;
- la dernière version stable d'[ImageMagick pour Windows](https://imagemagick.org/script/download.php#windows), installée globalement avec la commande `magick` disponible dans le `PATH`, nécessaire aux conversions et optimisations d'images ;
- Google Chrome à jour ;
- le mode développeur Windows, recommandé pour les liens symboliques vers `AGENTS.md`, les settings Claude et son fichier d'instructions. Ouvrez ses réglages avec `start ms-settings:developers`.

Vérifiez le poste dans PowerShell :

```powershell
git --version
codex --version
node --version
npm --version
npx --version
python --version
py --version
ffmpeg -version
magick -version
```

ImageMagick et Imagick ne désignent pas la même installation. ImageMagick fournit la commande locale `magick`. Imagick est l'extension PHP utilisée côté serveur. Lorsqu'un workflow WordPress en dépend, vérifiez séparément la présence de l'extension Imagick dans la santé du site ou dans la configuration PHP du serveur.

`npx skills` installe les skills. Codex CLI les charge ensuite. La première commande `npx skills` peut télécharger le CLI [`skills`](https://github.com/antfu/skills-cli).

## Installer les skills globaux requis

Installez les trois skills utilisés par les règles du kit :

```powershell
npx skills add JuliusBrussee/caveman --skill caveman --global --agent codex --yes
npx skills add kentnielsen-droid/cursor-skills --skill unslop --global --agent codex --yes
npx skills add anthropics/skills --skill frontend-design --global --agent codex --yes
npx skills list --global --agent codex
```

Sources à contrôler avant installation :

- [`caveman`](https://github.com/JuliusBrussee/caveman) ;
- [`unslop`](https://github.com/kentnielsen-droid/cursor-skills/blob/main/pstack/skills/unslop/SKILL.md) ;
- [`frontend-design`](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md).

Ces skills sont globaux. Les skills WordPress et Oxygen propres à Octacom restent dans `.agents/skills` du kit et sont reliés automatiquement au workspace.

## Préparer les MCP et le navigateur

Chaque site doit disposer de son propre connecteur MCP WordPress. Créez ou configurez cette connexion avec l'URL et les accès exacts du site. Ne placez aucun secret dans `README.md`, `AGENTS.md`, un skill ou un prompt de sous-agent.

Le MCP Figma est déjà configuré dans le workspace Octacom. Vérifiez qu'il est accessible avant une tâche qui dépend d'une maquette. L'impossibilité de lire les annotations Figma bloque l'implémentation concernée.

Le MCP Chrome DevTools est facultatif, mais utile pour la console, le réseau et les audits de performance. Il exige Node.js LTS et Chrome :

```powershell
codex mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
codex mcp list
```

Consultez le dépôt [`chrome-devtools-mcp`](https://github.com/ChromeDevTools/chrome-devtools-mcp) avant de l'ajouter. Vous pouvez aussi installer l'[extension ChatGPT officielle pour Chrome](https://chromewebstore.google.com/detail/chatgpt/hehggadaopoacecdllhhajmbjkdcmajg) pour travailler avec les onglets et sessions déjà ouverts dans Chrome.

## Cloner le kit une seule fois

Choisissez un dossier stable, puis clonez le dépôt :

```powershell
$octacomRoot = 'C:\Users\DEV\Documents\Octacom'
$kitRoot = Join-Path $octacomRoot 'wordpress-development-kit'

git clone https://github.com/OctacomFR/wordpress-development-kit.git $kitRoot
git -C $kitRoot status --short
```

Si le dépôt existe déjà, ne le clonez pas une seconde fois :

```powershell
$kitRoot = 'C:\Users\DEV\Documents\Octacom\wordpress-development-kit'
git -C $kitRoot pull --ff-only
```

## Installer le kit dans un workspace de développement

Le dossier de destination peut être vide ou être la racine Git exacte d'un site existant. Son parent doit déjà exister. Il doit rester séparé du clone du kit et ne doit pas dépendre d'une autre racine Git parente.
L'idée c'est d'avoir un dossier dédié pour l'ouvrir en tant que workspace dans Codex/T3 Code/Opencode etc. On pourra lui laisser la liberté de créer des fichiers et de lui en donner à dispo (par exemple de dossier d'intégration) sans mélanger avec le repo wordpress-development-kit.

```powershell
$kitRoot = 'C:\Users\DEV\Documents\Octacom\wordpress-development-kit'
$workspace = 'C:\Users\DEV\Documents\Octacom\Sites\nom-du-site'

& "$kitRoot\scripts\install-wordpress-development-kit.ps1" `
    -Destination $workspace
```

Si PowerShell bloque uniquement l'exécution du script, autorisez-la pour le processus courant, puis relancez la commande :

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

L'installateur :

- vérifie les conflits de règles et d'adaptateurs avant toute création et préserve les configurations étrangères ;
- initialise une racine Git exacte si le dossier n'en possède pas ;
- crée un lien symbolique `AGENTS.md` vers le clone du kit ;
- crée des jonctions pour `.agents` et `.codex` ;
- crée un vrai dossier `.claude`, avec liens de fichiers pour `settings.json` et `CLAUDE.md`, et jonctions pour `hooks` et `skills` ;
- crée un vrai dossier `.opencode`, avec une jonction pour `plugins` ;
- crée un vrai dossier `.octacom`, ignoré par Git, et refuse tout lien dans cet état local ;
- valide le catalogue, les références et les hooks ;
- exécute les tests d'injection du `skill-gate` ;
- annule ses liens et dossiers nouveaux si la validation échoue, sans suivre les jonctions ni supprimer les fichiers préexistants.

Le lien symbolique exige le mode développeur Windows ou une console disposant des droits requis. Si ces options sont impossibles, utilisez explicitement le mode dégradé :

```powershell
& "$kitRoot\scripts\install-wordpress-development-kit.ps1" `
    -Destination $workspace `
    -AllowHardLinkFallback
```

Le hardlink de secours ne garantit pas la propagation d'une mise à jour qui remplace physiquement sa source. Cela concerne aussi les deux fichiers Claude. L'installateur signale alors un conflit ; vérifier le lien devenu ancien avant de le recréer. La section « Mettre à jour le kit » indique comment rafraîchir `AGENTS.md`.

Lancer de nouveau la même commande est idempotent. L'installateur reconnaît les liens déjà en place et revalide le workspace.

Depuis le kit, `pwsh -NoProfile -File scripts/test-installation.ps1` vérifie deux installations NTFS temporaires, leur isolation, les conflits et le retour arrière. La suite utilise explicitement le secours par hardlink et nettoie ses fixtures sans suivre les jonctions.

## Ouvrir le workspace pour la première fois

Après l'installation :

1. Fermez toute session Codex déjà ouverte sur ce dossier.
2. Ouvrez le dossier de développement, pas le clone du kit.
3. Déclarez ce workspace fiable.
4. Suivez [l'activation propre à votre interface](docs/compatibility-runtimes.md). Dans Codex, relisez et approuvez les hooks avec `/hooks`, puis vérifiez les skills avec `/skills`.
5. Contrôlez la configuration effective et la découverte des hooks/skills avec la sonde ci-dessous, puis observez le dispatch sur une fixture sans site réel.
6. Vérifiez uniquement les MCP nécessaires au projet dans cette interface.

La confiance du projet et l'approbation des hooks restent des actions humaines. L'installateur ne les contourne pas. Conservez leurs preuves et l'état de mission dans `.octacom` du workspace ; ce dossier ne doit pointer ni vers le kit ni vers l'état d'un autre site.

## Prompt à donner à l'agent pour l'installation

Remplacez les deux chemins avant d'envoyer ce prompt :

```text
Installe le WordPress development kit Octacom dans mon workspace.

Clone ou source du kit : <KIT_ROOT>
Workspace de développement séparé : <WORKSPACE_ROOT>

Lis d'abord le README du kit et exécute le préflight skill-gate. Vérifie Git, Codex CLI, Node.js LTS, npm/npx et Python 3.11+ accessible par python.exe. Ne devine aucun chemin et ne remplace aucun AGENTS.md, .agents ou .codex existant qui ne vient pas de ce kit.

Si le kit n'est pas encore cloné, clone https://github.com/OctacomFR/wordpress-development-kit.git dans <KIT_ROOT>. Utilise ensuite scripts/install-wordpress-development-kit.ps1 avec -Destination <WORKSPACE_ROOT>. Préfère le lien symbolique pour AGENTS.md. Si Windows refuse sa création, arrête-toi et demande-moi soit d'activer le mode développeur, soit d'autoriser explicitement -AllowHardLinkFallback.

Après l'installation, valide le catalogue local, les tests du skill-gate et la racine Git exacte. Suis .agents/references/runtime-compatibility.md pour l'interface utilisée et distingue les tests de scripts, la découverte par sonde et l'exécution observée des hooks. Conserve l'état local dans un vrai dossier .octacom du workspace. Ne configure aucun secret et ne modifie aucun projet ERP. Indique-moi les étapes humaines restantes de confiance et d'approbation propres à cette interface.
```

Pour créer ensuite la connexion WordPress du site, fournissez séparément à l'agent l'URL exacte du site, le nom attendu du connecteur et la méthode d'authentification autorisée. Fournissez aussi l'URL Figma node-specific, les identifiants entreprise et projet Octacom et le domaine public final. Une information requise manquante bloque la configuration qui en dépend.

## Mettre à jour le kit et les workspaces

Mettez à jour le clone de référence :

```powershell
$kitRoot = 'C:\Users\DEV\Documents\Octacom\wordpress-development-kit'
git -C $kitRoot pull --ff-only
```

Avec le lien symbolique recommandé, `AGENTS.md`, `.agents` et `.codex` reflètent immédiatement le clone mis à jour. Fermez et rouvrez les sessions Codex concernées. Si les hooks ont changé, Codex demande une nouvelle approbation dans `/hooks`.

Pour convertir une ancienne installation par hardlink après avoir activé le mode développeur Windows :

```powershell
& "$kitRoot\scripts\install-wordpress-development-kit.ps1" `
    -Destination $workspace `
    -RefreshAgentLink
```

Si le poste doit rester en mode hardlink, rafraîchissez explicitement le lien après chaque `git pull` :

```powershell
& "$kitRoot\scripts\install-wordpress-development-kit.ps1" `
    -Destination $workspace `
    -RefreshAgentLink `
    -AllowHardLinkFallback
```

`-RefreshAgentLink` ne remplace `AGENTS.md` que lorsque `.agents` et `.codex` pointent déjà vers ce même kit. Le script conserve temporairement l'ancien fichier et le restaure si la création du lien ou la validation échoue.

Mettez à jour séparément les skills globaux installés avec `npx` :

```powershell
npx skills update --global --yes
```

## Préflight des skills

Les adaptateurs rappellent `skill-gate` aux événements pris en charge par leur interface. Le contrôle de fin relance une fois les demandes d'action reconnues sans appel local observé. Pour une mutation, une reprise ou une livraison, suivre la [procédure de contrôle de mission](.agents/references/mission-controls.md). Après une modification d'adaptateur, revalider sa confiance, son approbation et son dispatch selon [la procédure de compatibilité](docs/compatibility-runtimes.md).

Valider le workflow après toute modification des skills, de `AGENTS.md` ou des hooks :

```powershell
python .agents/skills/skill-gate/scripts/validate_workflow.py
python .agents/skills/skill-gate/scripts/test_workflow.py
```

Ces commandes valident les fichiers et simulent des événements. Elles ne prouvent ni la découverte ni le dispatch dans une interface active.

Depuis le kit, lire l'état effectif d'un app-server Codex lancé pour le workspace :

```powershell
python scripts/probe-codex-runtime.py --cwd $workspace --output (Join-Path $workspace '.octacom/verification/runtime-codex.json')
```

La sonde utilise `config/read`, `hooks/list` et `skills/list`. Vérifier les couches effectives, l'état actif et la confiance de chaque handler attendu, les erreurs et le catalogue découvert. Ce résultat concerne l'app-server interrogé ; pour Desktop, T3, OpenCode ou Claude Code, compléter les preuves propres à l'instance utilisée. T3 ne garantit pas à lui seul un backend Codex actif.

Observer ensuite le dispatch sur une fixture isolée, sans appeler un site WordPress :

1. Déclencher chaque événement pris en charge et conserver la preuve du handler réellement exécuté, y compris sur le chemin d'outil utilisé.
2. Envoyer une tâche simple et contrôler le rappel avant le premier outil, puis les décisions sur cible et informations manquantes dans les scénarios de mission.
3. Contrôler un sous-agent et une reprise après compaction avec le bon contexte, sans transférer une permission d'un autre acteur.
4. Vérifier une action autorisée, une action refusée et l'indisponibilité du contrôle ; distinguer le résultat simulé, le résultat du runtime et le résultat métier.

Le contrôle `Stop` ne prouve ni pertinence ni réussite. Les contrôles de mission vérifient les préconditions structurées qu'ils prennent en charge ; leur état local ne constitue pas une autorisation infalsifiable. Les chemins non dispatchés restent hors de leur portée. `serial_observed` vérifie les observations acceptées sans éliminer une écriture concurrente distante. Le mode `atomic_revision` bloque actuellement les mutations, car les outils exposés ne fournissent aucun CAS serveur. La [référence d'enforcement](.agents/skills/skill-gate/references/enforcement-and-tests.md) détaille ces limites.

## Vérifier le rendu Figma avant livraison

Le kit exige un rendu final identique à Figma à 100 %. Seuls les effets hover peuvent être interprétés. La [procédure de fidélité visuelle](.agents/references/figma-visual-fidelity.md) impose des captures Figma et front à la largeur native de chaque frame, une comparaison de la page entière et de chaque section, puis des corrections et de nouvelles captures jusqu'à zéro écart visuel non autorisé. Les preuves doivent correspondre à la dernière version sauvegardée.

`FIGMA_VISUAL_MATCH_VERIFIED` bloque la stabilisation des cibles Figma et la livraison tant que les comparaisons sont incomplètes, les preuves manquent ou un écart subsiste. L'absence de navigateur ou de référence produit un rapport de blocage. Un score automatique ne remplace pas l'examen des images.

Toute livraison, correction locale comprise, exige le crédit Octacom et les Templates Single Article/404 conformes. Auditer et réutiliser l'existant, puis corriger uniquement les manques avant de conclure. L'ajout du crédit absent de Figma est une exception visuelle autorisée selon [AGENTS.md](AGENTS.md#footer-et-légal) et son [architecture Footer](.agents/skills/oxygen6-architecture/references/reusable-architecture.md). Une source métier ou une disposition requise manquante continue de bloquer l'écriture concernée.

Produire les supports de comparaison avec Python et ImageMagick déjà requis par le kit :

```powershell
python .agents/skills/wordpress-oxygen-qa/scripts/compare_visuals.py --figma qa/figma/home-desktop.png --front qa/front/home-desktop.png --output-dir qa/comparisons/home-desktop-final
python .agents/skills/wordpress-oxygen-qa/scripts/test_compare_visuals.py
```

Le helper exige deux captures PNG de mêmes dimensions et un dossier de sortie nouveau. Il génère une vue côte à côte, une superposition, une image des différences et un JSON contenant les empreintes des sources et la mesure. L'agent doit ouvrir ces images et documenter la comparaison. Cet outil produit des preuves consultables ; il ne certifie pas automatiquement l'identité visuelle et ne modifie pas les hooks.
