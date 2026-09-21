# WordPress development kit

Kit Octacom pour les projets WordPress et Oxygen 6.x.

Le dépôt du kit reste séparé des sites développés. Vous le clonez une fois, puis son installateur relie `AGENTS.md`, `.agents` et `.codex` à chaque workspace de développement.

## Comprendre les dossiers

| Dossier | Rôle |
|---|---|
| `C:\Users\DEV\Documents\Octacom\wordpress-development-kit` | Clone de référence du kit. Les mises à jour se font ici avec Git. |
| `C:\Users\DEV\Documents\Octacom\Sites\nom-du-site` | Workspace séparé dans lequel se déroule le développement d'un site. |
| Répertoires globaux de Codex | Outils et skills personnels disponibles dans tous les projets du développeur. |

Ne placez pas un workspace de site dans le clone du kit. Ne déplacez pas le clone après avoir installé des workspaces, car les liens Windows utilisent son chemin absolu.

## Installer les prérequis Windows

Installez ces outils au niveau global du poste :

- [Git pour Windows](https://git-scm.com/download/win), nécessaire pour cloner le kit et créer la racine Git des workspaces ;
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli?translationFallback=fr-FR), nécessaire pour lancer l'agent dans le projet ;
- [Chat GPT Desktop](https://chatgpt.com/fr-FR/download/) ou [T3 code](https://t3.codes/download), facilement contrôler les agents avec une ui ;
- la dernière version LTS de [Node.js](https://nodejs.org/en/download), avec `npm` et `npx`, nécessaire pour installer les skills externes et exécuter certains MCP ;
- la dernière version stable de [Python pour Windows](https://www.python.org/downloads/windows/), installée globalement avec le lanceur `py.exe`, nécessaire aux hooks et aux tests du kit ;
- la dernière version stable de [FFmpeg](https://ffmpeg.org/download.html), installée globalement et ajoutée au `PATH`, nécessaire au traitement des vidéos et de certains médias ;
- la dernière version stable d'[ImageMagick pour Windows](https://imagemagick.org/script/download.php#windows), installée globalement avec la commande `magick` disponible dans le `PATH`, nécessaire aux conversions et optimisations d'images ;
- Google Chrome à jour ;
- le mode développeur Windows, recommandé pour créer un lien symbolique durable vers `AGENTS.md`. Ouvrez ses réglages avec `start ms-settings:developers`.

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

Le dossier de destination peut être vide ou être la racine Git exacte d'un site existant. Il doit rester séparé du clone du kit et ne doit pas dépendre d'une autre racine Git parente.
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

- refuse d'écraser un `AGENTS.md`, `.agents` ou `.codex` provenant d'une autre source ;
- initialise une racine Git exacte si le dossier n'en possède pas ;
- crée un lien symbolique `AGENTS.md` vers le clone du kit ;
- crée des jonctions pour `.agents` et `.codex` ;
- valide le catalogue, les références et les hooks ;
- exécute les tests d'injection du `skill-gate` ;
- annule les liens créés pendant l'exécution si la validation échoue.

Le lien symbolique exige le mode développeur Windows ou une console disposant des droits requis. Si ces options sont impossibles, utilisez explicitement le mode dégradé :

```powershell
& "$kitRoot\scripts\install-wordpress-development-kit.ps1" `
    -Destination $workspace `
    -AllowHardLinkFallback
```

Le hardlink de secours ne garantit pas la propagation d'une mise à jour qui remplace physiquement `AGENTS.md`. La section « Mettre à jour le kit » indique comment le rafraîchir.

Lancer de nouveau la même commande est idempotent. L'installateur reconnaît les liens déjà en place et revalide le workspace.

## Ouvrir le workspace pour la première fois

Après l'installation :

1. Fermez toute session Codex déjà ouverte sur ce dossier.
2. Ouvrez le dossier de développement, pas le clone du kit.
3. Déclarez ce workspace fiable.
4. Exécutez `/hooks`, relisez les trois hooks et approuvez-les.
5. Exécutez `/skills` et vérifiez `skill-gate` ainsi que les skills Octacom.
6. Exécutez `codex mcp list` et vérifiez uniquement les MCP nécessaires au projet.

La confiance du projet et l'approbation des hooks restent des actions humaines. Le script ne les contourne pas.

## Prompt à donner à l'agent pour l'installation

Remplacez les deux chemins avant d'envoyer ce prompt :

```text
Installe le WordPress development kit Octacom dans mon workspace.

Clone ou source du kit : <KIT_ROOT>
Workspace de développement séparé : <WORKSPACE_ROOT>

Lis d'abord le README du kit et exécute le préflight skill-gate. Vérifie Git, Codex CLI, Node.js LTS, npm/npx, Python et py.exe. Ne devine aucun chemin et ne remplace aucun AGENTS.md, .agents ou .codex existant qui ne vient pas de ce kit.

Si le kit n'est pas encore cloné, clone https://github.com/OctacomFR/wordpress-development-kit.git dans <KIT_ROOT>. Utilise ensuite scripts/install-wordpress-development-kit.ps1 avec -Destination <WORKSPACE_ROOT>. Préfère le lien symbolique pour AGENTS.md. Si Windows refuse sa création, arrête-toi et demande-moi soit d'activer le mode développeur, soit d'autoriser explicitement -AllowHardLinkFallback.

Après l'installation, valide tous les skills déclarés, les tests du skill-gate, les trois hooks et la racine Git exacte. Ne configure aucun secret et ne modifie aucun projet ERP. Indique-moi ensuite les étapes humaines restantes : rouvrir le workspace, le déclarer fiable, approuver /hooks et vérifier /skills.
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

Le dépôt configure un rappel automatique du préflight `skill-gate` au démarrage ou à la reprise, après compactage, au début de chaque prompt Codex et de chaque sous-agent. Après ajout ou modification des hooks, ouvrir une nouvelle session dans ce projet de confiance, lancer `/hooks`, relire les commandes de `.codex/hooks.json`, puis les approuver.

Valider le workflow après toute modification des skills, de `AGENTS.md` ou des hooks :

```powershell
py -3 .agents/skills/skill-gate/scripts/validate_workflow.py
py -3 .agents/skills/skill-gate/scripts/test_workflow.py
```

Ces commandes valident statiquement le catalogue local, ses références déclarées, la configuration et le texte injecté. Elles ne testent pas le runtime Codex ni le blocage d'une action.

Recette manuelle après activation :

1. Contrôler dans `/hooks` que les trois événements du dépôt sont approuvés et actifs.
2. Envoyer une tâche simple et vérifier que le préflight est injecté avant le premier outil.
3. Lancer un sous-agent en lecture seule et vérifier que son retour indique `skill-gate` et ses skills métier.
4. Modifier temporairement le hook sur une branche de test et confirmer que Codex exige une nouvelle approbation ; annuler ensuite cette modification.

Les hooks injectent des instructions sans bloquer les actions. Aucun contrôle `PreToolUse`, `Stop`, permis single-use ou exécuteur strict n'est fourni ici. Ils ne remplacent ni les permissions, ni les blocages d'information, ni le propriétaire unique des objets WordPress/Oxygen partagés.
