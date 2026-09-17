# Plan et ordre d implementation

Référence extraite sans réécriture du snapshot `docs/AGENTS.pre-skills-snapshot.md`.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 316-351 -->

### Phase D — Plan d'architecture Oxygen

Avant de construire la home, décider :

- ce qui appartient à un Template ;
- ce qui appartient à un Header ou Footer dédié ;
- ce qui devient Component ;
- quelles valeurs deviennent Component Properties ;
- ce qui devient classe/selector réutilisable ;
- ce qui devient Variable globale ;
- ce qui est propre à la home ;
- ce qui doit devenir dynamique avec WordPress ;
- ce qui peut servir aux futures pages internes.

### Phase E — Implémentation par blocs

Construire dans cet ordre recommandé :

1. Variables globales nécessaires ;
2. Classes / Selectors réutilisables ;
3. Components génériques ;
4. Header Oxygen ;
5. Footer Oxygen ;
6. Templates + Template Content Area si nécessaires ;
7. Component Hero ;
8. sections propres à la home ;
9. contenus dynamiques / Post Loop Builder ;
10. interactions ;
11. responsive ;
12. SEO ;
13. formulaires, Complianz et WP Mail SMTP ;
14. pages légales et menus associés ;
15. performance ;
16. QA finale.

Après chaque gros bloc : sauvegarder, ouvrir le front, contrôler le rendu avant de continuer.
