# WordPress development kit

Kit Octacom pour les projets WordPress et Oxygen 6.x.

## Installer le kit dans un workspace

Exécuter l'installateur depuis PowerShell en lui donnant le dossier choisi :

```powershell
& 'C:\Users\DEV\Documents\Octacom\wordpress-development-kit\scripts\install-wordpress-development-kit.ps1' `
    -Destination 'C:\chemin\vers\le\workspace'
```

L'installateur :

- refuse d'écraser un `AGENTS.md`, `.agents` ou `.codex` existant qui provient d'une autre source ;
- initialise une racine Git exacte lorsque nécessaire pour la résolution des hooks ;
- crée un hardlink pour `AGENTS.md` sur le même volume (sinon un lien symbolique) et des junctions pour `.agents` et `.codex` ;
- conserve automatiquement les futures mises à jour du kit dans les workspaces installés ;
- valide le catalogue, les références et les hooks, puis exécute les tests d'injection.

Lancer de nouveau la même commande est sans effet destructif. L'installateur reconnaît les liens déjà en place et revalide le workspace.

Après installation, fermer l'ancienne session Codex, ouvrir le workspace, le déclarer fiable, puis utiliser `/hooks` pour approuver les hooks et `/skills` pour contrôler les skills détectés. Ces étapes interactives ne sont pas automatisées.

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
