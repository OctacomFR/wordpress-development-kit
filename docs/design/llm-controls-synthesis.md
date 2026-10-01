# Choix des contrôles de mission

Base retenue : candidat A. Les lectures du code et des signatures MCP montrent qu'un proxy strict demanderait des accès et un contrôle de révision distante absents du kit. A s'intègre aux workspaces existants sans présenter ces capacités comme acquises.

Le jugement indépendant recommande A avec des greffes de B. Les deux candidats et le juge utilisent la famille disponible dans cette session ; cette exploration ne constitue pas une comparaison entre fournisseurs de modèles.

Critères de choix : faisabilité avec les outils exposés, refus des cibles incorrectes, fraîcheur des preuves, isolation entre workspaces, entretien limité, vérification par traces réelles.

Greffes de B : invalider dès la tentative d'écriture, conserver un état inconnu après résultat perdu, invalider toute la mission pour une mutation globale, refuser le mode atomique quand l'API ne propose pas de CAS. Les empreintes servent à comparer les versions observées, jamais à créer des permissions.

Le périmètre demandé inclut désormais Codex CLI et Desktop, Claude Code, OpenCode et T3 Code. Le domaine et l'état restent dans un module Python partagé. Des adaptateurs traduisent les événements natifs ; T3 exige une preuve par fournisseur réellement sélectionné. Une sonde app-server prouve la configuration du moteur interrogé, pas celle d'une autre interface.

Contrat d'implémentation : `.codex/hooks/mission_guard.py` possède validation, état SQLite propre au workspace, vérification des snapshots et pièces de preuve. `oxygen_site_gate.py` adapte les événements d'outils. Les bridges Claude/OpenCode traduisent ces mêmes événements. L'état réside dans `.octacom`, hors des jonctions du kit.

La fiche fixe cible, connecteur exact, version Oxygen, sources, conflits, annotations, objets, propriétaires et critères de fin. Les événements lient les observations à une session et à cette version de fiche. Avant une mutation, le contrôle exige l'objet autorisé et une empreinte attendue identique à une lecture récente. Après la tentative, l'empreinte attendue et les preuves doivent être renouvelées.

Le kit garde deux limites : un agent ayant accès au disque peut modifier ses propres déclarations, et une relecture suivie d'une écriture conserve une fenêtre de concurrence distante. Le mode `atomic_revision` refuse les mutations tant qu'un adaptateur garantissant une révision atomique n'existe pas. La revue visuelle et la vérification du builder restent des contrôles réels à effectuer.

Le crédit Octacom et les Templates Single Article et 404 sont des critères de toute livraison, y compris après une correction locale. Réutiliser les objets conformes permet de satisfaire ce critère sans refaire les autres pages.

Validation effectuée : fixtures positives et négatives, adaptateurs exécutés, installation dans deux workspaces isolés et lecture effective de configuration. Les traces natives montrent les refus avant effet dans OpenCode, Claude Code et T3 avec Codex et Claude. Sept conversations réelles Codex CLI passent les critères de leurs scénarios sur les empreintes finales. Les résultats sont liés dans [le rapport de modifications](../verification/kit-controls-changes.md).

Dans ce chat Desktop, l'injection du préflight et la configuration approuvée sont observées ; l'interception Oxygen sur fixture reste non observée. Le rapport conserve cette distinction et les limites de concurrence distante et de certification visuelle.
