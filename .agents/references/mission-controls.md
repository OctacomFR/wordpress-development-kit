# Préparer et contrôler une mission

Avant une mutation Oxygen, une reprise après changement d'interface ou une livraison, utiliser cette procédure. L'état réside dans `.octacom` à la racine réelle du workspace. Les jonctions du kit partagent le code, jamais la fiche ou la base SQLite.

## Fixer les faits et le périmètre

Créer `.octacom/mission.json` depuis le format illustré dans [mission.example.json](templates/mission.example.json). Le modèle est incomplet et doit être remplacé par des valeurs confirmées. Il ne constitue pas une mission autorisée.

Renseigner la référence à l'instruction utilisateur, le périmètre, les critères de fin, SITE_URL exact, domaine public final confirmé, préfixe MCP exact et version Oxygen 6 observée. Une préproduction et le domaine public restent deux identités distinctes. Ajouter sources et versions, conflits non résolus, références Figma avec file/node/version/états et preuve de lecture des annotations. Attribuer à chaque objet un propriétaire et les opérations précisément autorisées. Le coordinateur est l'unique écrivain de la fiche.

Valider depuis le workspace :

```powershell
python -B .codex/hooks/mission_guard.py mission-check
```

Une valeur requise introuvable suspend l'écriture concernée. Une lecture d'inventaire reste possible sans fiche. La fiche documente l'autorisation existante ; elle ne remplace pas les permissions du runtime.

## Lier les lectures à l'écriture

1. Appeler `oxygen_site_info` sur le connecteur confirmé. Le hook compare le site complet, y compris son sous-chemin, et la version exacte.
2. Lire `oxygen_get_post_tree` pour chaque post à modifier, ou la lecture globale prise en charge pour l'objet global. Un résultat d'erreur ou un schéma inconnu ne crée aucun snapshot valide.
3. Lier la session runtime observée au propriétaire de la fiche. Lire son identifiant dans le contexte PostToolUse du snapshot, sans le deviner.
4. Examiner l'arbre, puis accepter son empreinte exacte comme base de l'action déjà autorisée.

```powershell
python -B .codex/hooks/mission_guard.py bind-session --session <SESSION_OBSERVÉE> --owner <PROPRIÉTAIRE>
python -B .codex/hooks/mission_guard.py status
python -B .codex/hooks/mission_guard.py accept-snapshot --resource post:42 --revision <EMPREINTE_OBSERVÉE>
```

Le hook refuse une mauvaise identité, une version différente, un objet ou une opération hors périmètre, un propriétaire non lié, des annotations requises absentes, un conflit, une observation périmée ou une empreinte différente. Chaque tentative consomme sa base et invalide les preuves avant l'effet. Relire et examiner l'état sauvegardé après l'action avant d'accepter une nouvelle base. Un résultat `unknown` demande une réconciliation ; il n'autorise aucun retry aveugle.

Une tentative `pending` bloque toute nouvelle écriture sur le même objet, ainsi que les écritures globales susceptibles de le toucher. Si Codex termine le tour sans événement de résultat, son hook `Stop` classe cette tentative de la même session en `unknown`. Le prompt suivant ou une reprise de session effectue aussi cette clôture conservatrice. Cela constate une absence de résultat observé, pas un échec serveur prouvé. Claude dispose en plus de son événement natif `PostToolUseFailure`.

Pendant cette tentative, aucune lecture de l'objet concerné ne peut fournir de snapshot acceptable ni de preuve de livraison. Le résultat observé ou la clôture sans résultat invalide à nouveau les bases et pièces concernées. Relire l'état après cette clôture avant toute nouvelle acceptation ou preuve. La présence d'une mutation `pending` bloque aussi le contrôle mécanique de livraison.

Les lectures de snapshots actuellement adaptées sont `oxygen_get_post_tree`, `oxygen_get_global_settings`, `oxygen_get_css_variables` et `oxygen_get_css_selectors`. Une opération globale sans lecture adaptée reste bloquée. Les créations autorisées utilisent une ressource `create:<type>` ; ajouter ensuite à la fiche les IDs effectivement retournés, puis refaire les lectures. Une opération Oxygen inconnue est refusée jusqu'à examen de son contrat.

Les snapshots globaux exigent leur schéma reconnu : objet `settings`, liste `variables` ou liste `selectors`. Lire variables et sélecteurs sans filtre, et les sélecteurs avec `include_properties: true`. Une lecture filtrée reste utilisable pour un inventaire, mais ne fournit aucune base d'écriture globale. Un format serveur différent exige un adaptateur vérifié. Un `post_id` explicitement retourné doit correspondre à celui demandé. Un résultat de mutation différent de l'action contrôlée invalide les preuves des objets attendu et observé et laisse la tentative dans l'état `unknown`.

`serial_observed` vérifie une empreinte et une fenêtre de fraîcheur maximale de 300 secondes. Cette empreinte est une version observée, pas une révision atomique serveur. Les outils inspectés n'acceptent aucun `expected_revision` : `atomic_revision` refuse donc toute mutation. Fermer les autres écrivains, garder le propriétaire unique et signaler cette limite dans le rapport.

## Garder les preuves actuelles

Le manifeste d'une preuve fixe `id`, `kind`, `mission_digest`, `resource`, `observed_revision`, `epoch`, `reviewer`, `review_source`, `open_differences: []` et les `files` avec chemins et SHA-256. Les pièces sont confinées au workspace. Une preuve visuelle ajoute `figma_reference`, `figma_version`, `state`, `front_url`, `viewport` et `comparison`.

Fournir au helper `compare_visuals.py --provenance qa/capture-context.json` un JSON contenant exactement `mission_digest`, `resource`, `observed_revision`, `epoch`, `figma_reference`, `figma_version`, `state`, `front_url` et `viewport`. Ce contexte vient des versions observées avant la capture. L'enregistrement exige ce même contexte dans `comparison.json`. Sans contexte, le helper produit des supports exploratoires qui ne peuvent pas être enregistrés comme preuve de livraison.

```powershell
python -B .codex/hooks/mission_guard.py register-evidence --manifest qa/home-desktop-proof.json
python -B .codex/hooks/mission_guard.py delivery-check
```

La comparaison relie captures et supports empreintés à la version de mission, au snapshot Oxygen et à la version Figma. Toute mutation locale invalide les preuves de l'objet. Une mutation globale invalide conservativement la mission entière. Changer la fiche, une source ou la référence Figma invalide les anciennes observations et preuves. Une relecture externe différente et une pièce altérée rendent aussi la preuve périmée.

Lorsqu'un builder est ouvert, vérifier son état réel, le recharger après mutation externe, puis enregistrer la référence de cette vérification :

```powershell
python -B .codex/hooks/mission_guard.py builder-reloaded --resource post:42 --source <PREUVE_FRONT_ET_BUILDER>
```

La commande consigne une assertion de vérification ; elle n'agit pas sur le builder. Les sauvegardes UI hors hooks demeurent à vérifier réellement. Une nouvelle mutation rend cette assertion périmée.

Toute livraison exige des pièces actuelles `octacom_credit`, `single_article` et `404`, y compris après une correction locale. Réutiliser et tester les objets conformes, sans créer de doublons. Le contrôle exige aussi une comparaison par référence Figma et état fourni.

Un résultat `mechanical_pass` signifie que ces pièces et assertions passent les contrôles de cohérence. Il ne certifie ni le contenu des captures ni leur conformité visuelle. Examiner réellement toutes les preuves selon [figma-visual-fidelity.md](figma-visual-fidelity.md) et les critères métier de QA avant de déclarer la livraison vérifiée.

## Vérifier l'interface

Suivre la [matrice des runtimes](runtime-compatibility.md). Prouver séparément instructions et skills découverts, configuration active, confiance et dispatch avant effet. Une fixture verte ne prouve pas un site client ; une sonde CLI ne certifie pas Desktop ou T3. Les fichiers locaux restent modifiables et les hooks ne couvrent pas tous les chemins. Le kit fournit des contrôles bornés, pas un exécuteur de sécurité universel.
