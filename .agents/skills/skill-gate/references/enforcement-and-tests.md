# Niveaux de garantie et tests du skill gate

Lire cette référence avant de modifier les hooks, de créer un mécanisme de permis ou d'annoncer une garantie stricte de couverture.

## Trois niveaux à ne pas confondre

1. **Instruction de workflow** : `AGENTS.md` et `skill-gate` exigent un préflight. Le modèle peut encore se tromper.
2. **Injection de contexte** : `UserPromptSubmit` et `SubagentStart` rappellent automatiquement la règle. Cela améliore le routage, sans prouver son application.
3. **Exécuteur strict** : un orchestrateur externe contrôle chaque effet, l'action exacte, les permissions et la consommation atomique d'une autorisation. Ce niveau n'est pas implémenté dans ce dépôt.

**État actuel du kit : niveaux 1 et 2 uniquement.** Les scripts fournis valident la configuration statique et le texte d'injection. Ils ne bloquent aucun outil, ne contrôlent pas la réponse finale et ne démontrent ni permis, ni hash d'action, ni expiration, ni single-use, ni concurrence. Tous les scénarios de la section « Tests avant activation d'un mode strict » sont des exigences pour un futur exécuteur, pas des tests actuellement réussis.

Les hooks `PreToolUse` couvrent de nombreux outils locaux, mais pas tous les chemins possibles. Les outils hébergés et certains outils spécialisés peuvent les contourner. `write_stdin` sur une session existante ne relance pas le hook de l'appel initial. Traiter les hooks comme des garde-fous, pas comme une frontière universelle.

## Pourquoi aucun permis local global n'est utilisé

Un fichier partagé `permit.json` est incompatible avec les sous-agents parallèles : ils utilisent la session parente, peuvent écraser le même état et peuvent lire puis consommer le même permis simultanément. Un hash public du nom d'outil ou des arguments ne crée pas une autorisation infalsifiable. Une déclaration du modèle ne prouve pas non plus que les instructions ont été lues.

Ne pas ajouter un hook bloquant fondé sur :

- un permis unique partagé par tout le dépôt ;
- le seul nom de l'outil, un joker ou une recherche de sous-chaîne dans une commande ;
- un hash recalculable fourni par l'appelant ;
- une suppression de fichier non atomique ;
- le transcript Codex, dont le format n'est pas une interface stable ;
- un journal contenant prompts, secrets, clés ou arguments non expurgés.

## Contrat minimal d'un futur exécuteur strict

Traiter ce travail comme un projet d'orchestrateur séparé. L'enveloppe d'action doit être un JSON strict, canonique et immuable comprenant au minimum :

```text
task_id, action_id, agent_id, action_class,
tool, validated_args, resource_id, expected_revision,
selected_skills_digest, permission_scope, expires_at
```

L'exécuteur doit :

- faire examiner l'enveloppe exacte, pas une intention vague ;
- valider localement le schéma et refuser nombres non finis, objets spéciaux, cycles et types non JSON ;
- séparer le routage de skills des permissions déterministes ;
- conserver côté serveur l'action immuable et un nonce opaque ;
- consommer le nonce de façon atomique, une seule fois et avant l'effet ;
- isoler l'état par agent et action ;
- verrouiller la ressource ou utiliser une révision attendue pour les objets WordPress/Oxygen partagés ;
- transmettre une clé d'idempotence lorsque l'outil le permet ;
- distinguer les états `pending`, `completed` et `unknown` après un crash ;
- journaliser une version expurgée et append-only de la décision et du résultat ;
- charger le `SKILL.md` complet et toutes ses références obligatoires depuis des chemins confinés à des racines autorisées ;
- prévoir explicitement les outils non couverts par les hooks.

Un modèle peut recommander des procédures. Il ne doit jamais émettre seul l'autorisation de mutation.

## Exigences de tests avant activation d'un futur mode strict

### Catalogue et chargement

- `skill-gate` absent, nom dupliqué ou skill inconnu ;
- frontmatter invalide, chemin hors racine, symlink non autorisé, fichier trop volumineux ;
- référence obligatoire absente ;
- catalogue tronqué dans le contexte du modèle, tout en conservant un catalogue complet côté exécuteur.

### Décision et action

- décision absente, multiple ou mal formée ;
- skill inventé ou liste dupliquée ;
- changement de tool, d'arguments, de cible, de révision ou de classe après contrôle ;
- absence de permis, expiration, réutilisation, deux actions avec le même permis ;
- mutation des arguments imbriqués après émission ;
- tentative « ignore le skill-gate » ou demande urgente de contourner les règles.

### Concurrence et reprise

- deux agents sur des ressources distinctes ;
- deux actions concurrentes sur la même ressource : une seule gagne ou la seconde reçoit un conflit explicite ;
- plusieurs processus, redémarrage et horloge modifiée ;
- crash avant effet, après effet et avant journalisation ;
- sous-agent sans préflight ;
- finalisation sans contrôle applicable.

### Intégration métier

Tester au minimum les routes positives pour Figma/Oxygen, Header global, SEO, formulaire/SMTP, légal/Complianz et inventaire simple. Les tests prouvent le routage et les frontières ; ils ne remplacent pas les recettes métier des skills spécialisés.

## Mesures

En mode strict seulement, viser :

- couverture des actions gardées : 100 % ;
- actions observables non gardées : 0 ;
- réutilisations de permis : 0 ;
- divergences entre action contrôlée et exécutée : 0 hors tests ;
- sous-agents sans préflight : 0.

Mesurer aussi faux positifs, faux négatifs, latence p50/p95, tokens, retries, skills inconnus et conflits de ressources. Un appel de modèle avant chaque lecture augmente fortement coût et latence ; préférer un préflight par unité cohérente tant qu'aucun exécuteur strict ne justifie une granularité plus fine.
