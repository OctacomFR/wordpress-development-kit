# Audit local des contrôles du kit au 1er octobre 2026

Le kit fournit une instruction de préflight, une injection de contexte, un rappel de fin borné et un garde-fou Oxygen ciblé. Il ne vérifie pas automatiquement que l'agent a lu les skills, identifié le site correct ou examiné les preuves visuelles. Les documents expliquent cette limite. Les tests livrés passent dans l'environnement normal observé. Les sondes supplémentaires reproduisent plusieurs façons de satisfaire les contrôles locaux sans satisfaire les préconditions métier.

## Périmètre et méthode

Audit en lecture des scripts, configurations, tests, installateur et README. Une seule écriture dans le dépôt est autorisée, ce rapport. L'installateur n'a pas été exécuté. Aucun site WordPress, projet ERP, hook approuvé, connecteur ou configuration active n'a été modifié.

Skills lus et appliqués : `skill-gate`, sa référence `references/enforcement-and-tests.md`, `technical-writing` et `unslop`. La procédure partagée de fidélité Figma a été lue comme source de l'audit. Aucune QA de site ni implémentation Figma n'est annoncée.

Les essais Python importent les modules avec `python -B`, passent explicitement un dossier `TemporaryDirectory` à `handle()` et utilisent des copies du dépôt dans TEMP pour les variantes du validateur. Les tests en sous-processus reçoivent `TMP`, `TEMP`, `TMPDIR` et `PYTHONDONTWRITEBYTECODE=1`. Aucun état synthétique n'a été écrit dans les dossiers temporaires des hooks actifs. Les dossiers de test sont supprimés par `TemporaryDirectory`.

Environnement observé : Python 3.14.7, `C:\Users\DEV\AppData\Local\Python\pythoncore-3.14-64\python.exe`, ImageMagick 7.1.2-31 Q16-HDRI x64. Les autres versions de Python et les autres systèmes ne sont pas testés.

## Résultats des tests livrés

| Commande exécutée avec `python -B` | Résultat |
|---|---|
| `.agents/skills/skill-gate/scripts/validate_workflow.py` | Code 0, 13 skills, configuration statique et injections validées |
| `.agents/skills/skill-gate/scripts/test_workflow.py`, environnement Windows par défaut | Code 0, 17 tests |
| Même commande avec `PYTHONUTF8=1` et `PYTHONIOENCODING=utf-8` | Code 0, 17 tests |
| Même commande avec seulement `PYTHONIOENCODING=utf-8` | Code 1, 2 échecs sur 17, assertions textuelles contenant des accents |
| `.agents/skills/wordpress-oxygen-qa/scripts/test_compare_visuals.py` | Code 0, 7 tests avec images réellement générées par ImageMagick |

La première exécution groupée forçait uniquement `PYTHONIOENCODING=utf-8` et a révélé les deux échecs. Les nouvelles exécutions par défaut puis en mode UTF-8 complet passent. Cette différence est conservée dans l'audit, car le protocole d'encodage des sous-processus fait partie de la reproductibilité des tests.

## Constats reproduits

### A1. Le contrôle Oxygen accepte un contenu non vide sans contrôler le site ou la version

Importance élevée pour l'évaluation des garanties. C'est une limite déjà déclarée dans la documentation, mais elle interdit de traiter le marqueur comme une preuve d'identité.

`site_info_succeeded()` exige un dictionnaire, `isError is not True` et une valeur vraie dans `content` ou `structuredContent`. Il ne lit aucun champ d'identité. Sources : `.codex/hooks/oxygen_site_gate.py:62`, `:78` et `.agents/skills/skill-gate/references/enforcement-and-tests.md:13`.

Chaque sonde part d'un dossier d'état neuf, envoie un `PostToolUse` pour `mcp__site__oxygen_site_info`, puis un `PreToolUse` pour `mcp__site__oxygen_edit_post` avec le même `cwd` et `session_id`.

| Réponse synthétique de site info | Mutation refusée |
|---|---|
| `{"content":[{"type":"text","text":""}]}` | Non |
| `{"content":[{"type":"text","text":"ERROR unauthorized"}]}` | Non |
| `{"structuredContent":{"site_url":"https://other.invalid","builder_version":"5.0"}}` | Non |
| `{"isError":true,"content":[{"type":"text","text":"error"}]}` | Oui |
| `{"isError":1,"content":[{"type":"text","text":"error"}]}` | Non |
| `{"isError":"true","content":[{"type":"text","text":"error"}]}` | Non |
| `{"result":{"content":[{"type":"text","text":"site info"}]}}` | Oui |

Les deux cas `isError` mal typés sont des essais de robustesse. Ils ne prouvent pas que le connecteur réel émet ces formes. La réponse enveloppée montre aussi un refus possible si le runtime ne fournit pas la forme MCP attendue. Le résultat réel reçu par `PostToolUse` n'a pas été capturé dans cette mission.

Une lecture réussie suivie d'une lecture `isError=true` laisse le premier marqueur valide. Une mutation ultérieure dans la même session reste permise. Une autre session et un autre alias MCP sont refusés. Le marqueur repose sur `cwd`, `session_id` et le préfixe exact du nom d'outil, sans `turn_id`, URL, version, expiration ou révocation. Source : `.codex/hooks/oxygen_site_gate.py:54`. Cela implémente la règle "lecture pendant la session", sans détecter un changement de cible derrière le même connecteur.

### A2. Le rappel d'usage des outils comporte des faux positifs et faux négatifs

Importance moyenne. Ce contrôle reste une heuristique de rappel, sans preuve de pertinence.

La détection utilise une liste de verbes et dispense tout prompt commençant par un mot explicatif. Sources : `.codex/hooks/tool_use_gate.py:14` et `:26`.

| Prompt synthétique | `needs_tools()` |
|---|---|
| `Peux-tu regarder les hooks ?` | `False` |
| `Ameliore les hooks` | `False` |
| `Comment est le site ? Inspecte-le.` | `False` |
| `N'utilise aucun outil.` | `True` |
| `Analyse le site` | `True` |

Un `PostToolUse` nommé `functions.exec` avec `tool_response={"isError":true}` suffit à satisfaire un tour `Analyse le site`. Le `Stop` retourne `{}`. Le script ignore le résultat, les arguments et la pertinence de l'outil. Il exclut seulement les noms exacts `Agent` et `update_plan`. Source : `.codex/hooks/tool_use_gate.py:60`.

Les tests existants vérifient la relance unique, un appel MCP, une question simple, un autre tour et le passage UTF-8 du CLI. Ils ne testent pas les verbes absents, la négation, une question suivie d'une action, les appels échoués ou les noms normalisés des outils de planification et de délégation. Source : `.agents/skills/skill-gate/scripts/test_workflow.py:124`.

### A3. Le validateur peut annoncer une configuration valide avec des hooks inopérants

Importance moyenne pour l'installation et les mises à jour. Les sondes modifient uniquement une copie du dépôt dans TEMP.

Trois variantes ont retourné `[]`, donc aucune erreur de `validate()` :

- suppression de `AGENTS.md` ;
- remplacement de tous les matchers par `NEVER_MATCH_THIS_TOOL` et de toutes les commandes par `echo <nom_du_script.py>` ;
- ajout d'une référence directe valide dont le contenu pointe vers `missing-required.md`, fichier absent.

Le validateur ne traite pas l'absence d'`AGENTS.md` comme une erreur. Il contrôle sa taille seulement si le fichier existe. Source : `.agents/skills/skill-gate/scripts/validate_workflow.py:126`.

Les commandes de hooks sont reconnues par la présence du nom de script dans une chaîne. Les matchers, le type du handler, le timeout et l'exécution réelle de la commande ne sont pas validés. Sources : même fichier, `:158` et `:177`. Le test de matchers couvre les 25 noms de la liste `MUTATIONS`, mais les tests d'injection exécutent le fichier Python directement. Ils n'exécutent pas les commandes Unix ou Windows déclarées dans `hooks.json`. Sources : `.agents/skills/skill-gate/scripts/test_workflow.py:33` et `:244`.

La recherche de références porte sur le texte de chaque `SKILL.md` et sur une expression régulière restreinte à `references/...md`. Elle ne parcourt pas récursivement le contenu des références et n'analyse pas un arbre Markdown complet. Source : `.agents/skills/skill-gate/scripts/validate_workflow.py:15` et `:42`.

Le message "configuration statique et injections validées" est donc une validation limitée des fichiers attendus. Il ne certifie ni l'exécution des hooks ni le chargement de toutes les références obligatoires.

### A4. Les tests textuels dépendent de la concordance des encodages

Importance faible, résultat confirmé sous Windows et Python 3.14.7.

Avec seulement `PYTHONIOENCODING=utf-8`, les sous-processus du validateur émettent du UTF-8, mais `subprocess.run(text=True)` dans les tests ne fixe pas l'encodage de capture. Deux assertions accentuées échouent. Sources : `.agents/skills/skill-gate/scripts/test_workflow.py:72`, `:94`, `:80` et `:101`.

Les tests passent avec l'environnement normal observé et avec `PYTHONUTF8=1`. L'installateur force `PYTHONIOENCODING` pour le validateur, puis restaure sa valeur précédente avant les tests. Ce choix évite le problème lorsque la valeur précédente n'était pas forcée. Une valeur UTF-8 déjà présente reste un cas sensible. Sources : `scripts/install-wordpress-development-kit.ps1:273`, `:282` et `:291`.

## Couverture et chemins restant à vérifier dans Codex

`hooks.json` utilise un matcher Oxygen pour `PreToolUse` et un matcher `oxygen_site_info$` pour le marquage `PostToolUse`. Sources : `.codex/hooks.json:55` et `:79`. Le script reconnaît uniquement les noms commençant par `mcp__` et terminés par un suffixe exact de sa liste. Source : `.codex/hooks/oxygen_site_gate.py:45`.

La liste contient 25 mutations. Les 22 noms de mutation exposés dans la session et transmis par le coordinateur figurent tous dans cette liste. Aucun manque de couverture de liste n'est démontré pour ce connecteur. La sonde hypothétique `mcp__site__oxygen_update_post` retourne `{}` et montre seulement qu'une nouvelle mutation absente de la liste n'est pas protégée automatiquement.

Le parser local retourne également `{}` pour un événement synthétique nommé `functions.exec` ou `exec_command`, même si les arguments décrivent une mutation. Cette observation ne prouve pas un contournement réel par encapsulation. Le runtime peut décomposer les appels MCP imbriqués et fournir un événement propre à chaque outil. L'intégration nested JavaScript, le nom normalisé d'outil et la forme exacte de `tool_response` exigent une observation réelle des événements Codex. Aucun appel mutable n'a été lancé pour cette preuve.

Les mutations réalisées par terminal, HTTP, interface de builder ou autre capacité restent hors de la classification par noms MCP de ce script, sauf mécanisme séparé du runtime. Le kit ne fournit pas un exécuteur contrôlant tous les effets. Le README le dit explicitement à `README.md:231` et la référence d'enforcement à `.agents/skills/skill-gate/references/enforcement-and-tests.md:15`.

La configuration locale `features.hooks=true` existe à `.codex/config.toml:8`. Elle ne prouve pas l'approbation active de `/hooks`. L'installateur demande encore la réouverture du workspace, la confiance, l'approbation des hooks et la vérification des skills à `scripts/install-wordpress-development-kit.ps1:485`. Ces étapes n'ont pas été testées dans cette mission.

## Preuves visuelles et origine des barrières

Les sept tests ImageMagick passent. Ils prouvent la génération à taille native, les empreintes des sources, un déplacement d'un pixel mesuré sans seuil de réussite, le refus des tailles différentes, la préservation d'un dossier de preuve existant et les refus d'entrées absentes ou identiques par chemin. Sources : `.agents/skills/wordpress-oxygen-qa/scripts/test_compare_visuals.py:39` à `:85`.

Le helper vérifie les dimensions, refuse un dossier existant, mesure RMSE, contrôle la taille des sorties et revérifie les empreintes des sources après la comparaison. Sources : `.agents/skills/wordpress-oxygen-qa/scripts/compare_visuals.py:46`, `:51`, `:79` et `:91`. Il accepte les codes ImageMagick 0 et 1 pour la différence, puis termine avec code 0 lorsque les supports sont produits. Cela est cohérent avec sa fonction de production de preuves, sans verdict de conformité.

Une sonde supplémentaire génère un PNG blanc de 64 x 48, le copie vers un deuxième chemin et compare les deux. Elle réussit avec RMSE 0 et `visual_review_required=true`. L'identité des pixels ne prouve donc pas que le premier fichier vient de Figma et le second du front. Le helper n'affirme pas cette provenance.

`comparison.json` contient les clés `commands`, `generated_at_utc`, `inputs`, `outputs`, `rmse`, `tool` et `visual_review_required`. Chaque entrée source contient `path`, `sha256`, `width` et `height`. Sources : `.agents/skills/wordpress-oxygen-qa/scripts/compare_visuals.py:97` à `:114`. Le JSON ne contient pas le node Figma, sa révision, l'URL front, la révision Oxygen, la largeur CSS, le DPR, le zoom, le scroll, l'état, les sections couvertes ou le registre des écarts.

Ces métadonnées sont demandées dans la fiche documentaire de `.agents/references/figma-visual-fidelity.md:54`. Le helper ne les lie pas à une révision WordPress ou à une capture de navigateur. Une modification après comparaison ne révoque aucun état machine. La procédure exige une nouvelle capture à `:83`, mais l'application dépend de l'agent et du coordinateur.

La règle de zéro écart est précise : aucune différence non autorisée ou inexpliquée, aucun seuil global, aucune moyenne, aucun masque. Une différence de rasterisation des fontes requiert un examen des propriétés et des contours. Elle ne constitue pas un verdict automatique. Sources : `.agents/references/figma-visual-fidelity.md:3`, `:50` et `:74`.

`FIGMA_ANNOTATIONS_REVIEWED`, `GLOBALS_STABLE`, `HOME_STABLE`, `PAGES_COMPLETE`, `QA_PASS` et `FIGMA_VISUAL_MATCH_VERIFIED` sont des barrières de procédure. Les scripts audités ne possèdent ni registre machine de ces états ni mécanisme vérifiant les pièces, leurs révisions ou leur consultation. La procédure visuelle interdit elle-même une simple déclaration d'agent ou un marqueur écrit comme preuve à `.agents/references/figma-visual-fidelity.md:85`. Leur validité repose sur l'examen de preuves réelles par le coordinateur, pas sur un hook déterministe.

## Installateur inspecté, sans exécution

La lecture confirme des vérifications de source et de conflits, une racine Git exacte, des liens symboliques ou jonctions, un secours hardlink explicite, une validation statique et les tests du workflow. Sources : `scripts/install-wordpress-development-kit.ps1:137`, `:229`, `:259`, `:303`, `:363` et `:419`.

`-SkipValidation` permet de sauter la validation et les tests à `:429`. L'installateur n'exécute pas les tests ImageMagick. Les tests workflow calculent leur racine depuis `__file__.resolve()`, donc via une jonction du workspace ils peuvent tester le kit source. Le validateur reçoit séparément `--repo $InstalledRoot`. Sources : `.agents/skills/skill-gate/scripts/test_workflow.py:17` et `scripts/install-wordpress-development-kit.ps1:277`.

La lecture montre une restauration de l'ancien `AGENTS.md` et la suppression des nouveaux liens en cas d'échec. La suppression récursive de `.git` est confinée lexicalement au préfixe de destination. Sources : `scripts/install-wordpress-development-kit.ps1:438` à `:461`. Aucun comportement de lien NTFS, volume, concurrence, réanalyse de chemin ou retour arrière n'a été éprouvé. Aucun test dédié à l'installateur n'est fourni dans les fichiers inventoriés.

## Reproduction minimale des sondes

Depuis la racine du kit, cette commande ne change que son dossier temporaire :

```powershell
@'
import importlib.util, tempfile
from pathlib import Path
repo = Path.cwd()
spec = importlib.util.spec_from_file_location('gate', repo / '.codex/hooks/oxygen_site_gate.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
with tempfile.TemporaryDirectory() as td:
	base = {'cwd': str(repo), 'session_id': 'audit'}
	gate.handle(dict(base, hook_event_name='PostToolUse', tool_name='mcp__site__oxygen_site_info',
		tool_response={'structuredContent': {'site_url': 'https://other.invalid', 'builder_version': '5.0'}}), Path(td))
	print(gate.handle(dict(base, hook_event_name='PreToolUse', tool_name='mcp__site__oxygen_edit_post'), Path(td)))
'@ | python -B -
```

Résultat observé : `{}`. Sans le premier événement, le même appel retourne `permissionDecision=deny`.

Les suites se reproduisent avec la même isolation d'environnement :

```powershell
@'
import os, subprocess, sys, tempfile
with tempfile.TemporaryDirectory(prefix='octacom-audit-') as td:
	env = dict(os.environ, TMP=td, TEMP=td, TMPDIR=td, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
	for script in ['.agents/skills/skill-gate/scripts/validate_workflow.py',
		'.agents/skills/skill-gate/scripts/test_workflow.py',
		'.agents/skills/wordpress-oxygen-qa/scripts/test_compare_visuals.py']:
		result = subprocess.run([sys.executable, '-B', script], env=env, capture_output=True, text=True, encoding='utf-8')
		print(script, result.returncode, result.stdout, result.stderr)
'@ | python -B -
```

## Limites de la conclusion

Le rapport prouve le comportement des fonctions locales sur les événements synthétiques documentés et les suites livrées dans l'environnement observé. Il ne prouve pas l'approbation des hooks, leur dispatch dans Codex, la couverture des outils hébergés, la forme réelle des événements, le bon site, les permissions métier, un rendu Figma ou la fiabilité de l'installateur en fonctionnement. Aucun site ne peut être déclaré conforme sur la base de cet audit du kit.
