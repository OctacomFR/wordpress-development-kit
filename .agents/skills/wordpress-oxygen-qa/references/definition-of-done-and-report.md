# Definition of Done et rapport final

Référence extraite du snapshot `docs/AGENTS.pre-skills-snapshot.md`, puis renforcée avec la barrière active des annotations Figma.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 1510-1673 -->

## 22. Definition of Done

Le travail n'est terminé que si tous les points applicables sont vrais.

### Design

- [ ] Structure des sections conforme à Figma.
- [ ] Assets réels utilisés.
- [ ] Typographies conformes.
- [ ] Couleurs conformes.
- [ ] Espacements contrôlés.
- [ ] États hover/interactions conformes.
- [ ] Toutes les annotations du périmètre ont été lues intégralement et reliées à leur node/frame/composant/section.
- [ ] Chaque annotation applicable et ses effets indirects ont été vérifiés sur le front, aux breakpoints et états concernés.
- [ ] La matrice d'annotations contient un statut et une preuve pour chaque ligne ; aucune annotation inaccessible, ambiguë ou contradictoire ne reste sans décision utilisateur.

### Oxygen 6.x

- [ ] Version exacte d'Oxygen confirmée.
- [ ] Header Oxygen dédié et règles Location/Conditions vérifiées.
- [ ] Header sticky fonctionnel sur toutes les pages et tous les breakpoints, sans masquer le contenu.
- [ ] Footer Oxygen dédié et règles Location/Conditions vérifiées.
- [ ] Template Oxygen 6 Single Article présent, appliqué aux articles et lié aux données dynamiques réelles.
- [ ] Template Oxygen 6 spécial 404 présent avec la Location `404 Not Found`, Header/Footer et navigation de sortie.
- [ ] Templates utilisant Template Content Area lorsque nécessaire.
- [ ] Components réutilisables créés sans sur-abstraction.
- [ ] Component Properties utilisées pour les variations pertinentes.
- [ ] Variables existantes réutilisées avant création de valeurs parallèles.
- [ ] Classes/Selectors réutilisés.
- [ ] Page éditable dans Oxygen.
- [ ] Aucun gros blob HTML remplaçant le builder.
- [ ] Aucun concept Classic (`Reusable Part`, `Inner Content`, `Easy Posts`) introduit dans un nouveau build.
- [ ] Éditeur rechargé après les mutations externes et dernière version sauvegardée sans écrasement.
- [ ] Toute classe globale modifiée a été relue en entier et ses pages consommatrices ont été contrôlées.

### Responsive

- [ ] 1920, 1440, 1280, 1024, 768, 480, 390, 360 et 320 px testés.
- [ ] Une largeur intermédiaire proche de chaque changement de layout testée.
- [ ] Desktop testé à la taille de référence Figma.
- [ ] Aucun overflow horizontal.
- [ ] Menu utilisable.
- [ ] Fixed elements non bloquants.

### Contenu dynamique

- [ ] Actualités viennent de WordPress.
- [ ] Catégorie résolue par slug/ID réel.
- [ ] Ordre date DESC.
- [ ] 2 derniers posts si demandé.
- [ ] Permaliens réels.
- [ ] Cas 0/1 article acceptable.

### Liens

- [ ] Tous les CTA ont une destination.
- [ ] `tel:` sur téléphone.
- [ ] `mailto:` sur email.
- [ ] Aucun `#` factice involontaire.
- [ ] Liens externes ouverts dans un nouvel onglet munis de `rel="noopener noreferrer"`.

### SEO

- [ ] H1 unique.
- [ ] Hiérarchie Hn cohérente.
- [ ] Title vérifié.
- [ ] Meta description vérifiée.
- [ ] Canonical vérifiée.
- [ ] Liens crawlables.
- [ ] Alt images vérifiés.
- [ ] Yoast non dupliqué par du markup manuel.
- [ ] Schema cohérent si applicable.

### Performance

- [ ] Tous les rasters maîtrisés utilisés sur le site ont été convertis en WebP avant import ou utilisation.
- [ ] Les logos, icônes, pictogrammes, formes et illustrations vectorielles utilisent au maximum des SVG optimisés et assainis.
- [ ] Aucun JPEG, PNG ou GIF n'est chargé comme image de contenu par les pages.
- [ ] LCP image non lazy.
- [ ] Images sous fold lazy lorsque pertinent.
- [ ] Dimensions/ratio des images réservés.
- [ ] Pas d'assets Figma temporaires.
- [ ] JS custom minimal.
- [ ] Iframes/widgets ne provoquent pas de CLS évitable.

### QA

- [ ] Front contrôlé avec navigateur si disponible.
- [ ] Builder Oxygen contrôlé.
- [ ] Site contrôlé avec JavaScript désactivé : contenu, navigation et actions essentielles visibles et utilisables.
- [ ] Animations défaillantes ou non initialisées ne masquent aucun contenu.
- [ ] Console sans erreur liée au dev.
- [ ] Aucun asset 404.
- [ ] Une URL inexistante renvoie réellement un statut HTTP 404 et le Template Oxygen spécial attendu.
- [ ] Le Template Single Article et le Template 404 ont été contrôlés sur le front et dans le builder.
- [ ] Aucun placeholder involontaire.
- [ ] Sauvegarde proportionnée au risque créée et vérifiée.
- [ ] Complianz configuré et scénarios de consentement testés.
- [ ] Page **Politique de protection des données** générée par Complianz et présente dans le menu du footer.
- [ ] Page **Mentions légales** présente dans le menu du footer.
- [ ] **Conditions générales de vente** validées et présentes dans le menu du footer lorsqu'elles existent ou sont applicables.
- [ ] WP Mail SMTP configuré pour le domaine final et réception réelle du test vérifiée sur `support@octacom.fr`.
- [ ] Pendant les tests, `support@octacom.fr` était l'unique destinataire et l'adresse saisie dans le champ email ; aucune donnée réelle du client n'a été utilisée.
- [ ] Les autres champs contenaient uniquement des valeurs fictives et la soumission était marquée `TEST OCTACOM - NE PAS TRAITER`.
- [ ] Le destinataire final validé du client a été rétabli et relu avant livraison, sans envoi au client sauf demande explicite.
- [ ] Formulaire, consentement, CAPTCHA, honeypot et messages testés.
- [ ] Mentions légales remplies avec des données validées et sans variable de template restante.
- [ ] Crédit de réalisation Octacom présent dans le footer avec la bonne variante de logo.

---

## 23. Rapport final de l'agent

À la fin, répondre de façon courte et vérifiable :

```text
Implémenté
- ...

Réutilisable
- ...

Dynamique
- ...

QA effectuée
- Figma desktop : ...
- Responsive : ...
- Oxygen builder : ...
- SEO : ...
- Performance : ...

Reste / limites
- uniquement les vrais points non vérifiés
```

Ne pas écrire « tout est bon » si une partie n'a pas été testée.

Si le navigateur n'est pas disponible, écrire explicitement que la comparaison visuelle front n'a pas pu être effectuée.

Si les annotations Figma ne sont pas exposées ou si leur exhaustivité ne peut pas être vérifiée, l'implémentation dépendante reste bloquée. Le rapport indique la limite et la question posée à l'utilisateur ; il ne revendique pas une conformité Figma complète.

### Rapport de temps, tokens et coût

À la fin d'un développement complet, ajouter un récapitulatif du type `Récap <nom du site> — <modèle principal>` à partir des journaux réellement disponibles. Ne jamais estimer des tokens ou des coûts sans données.

Inclure, lorsque les journaux les exposent :

- heure de début et de fin, durée totale avec pauses et temps d'exécution actif ;
- détail par modèle utilisé ;
- tokens d'entrée hors cache, tokens d'entrée en cache, tokens de sortie incluant le raisonnement et total ;
- coût unitaire ou source tarifaire, coût par catégorie, coût par modèle et total ;
- part du cache dans les tokens d'entrée ;
- périmètre temporel exact du relevé et éventuelles lacunes des journaux.

Format recommandé :

```text
Récap <site> — <modèle principal>

Période : <début> à <fin>
Durée totale avec pauses : <durée>
Temps d'exécution cumulé : <durée>

Modèle | Entrée hors cache | Entrée en cache | Sortie + raisonnement | Total tokens | Coût
...

Total : <tokens> | <coût>
Part du cache dans les entrées : <pourcentage>
Source des tarifs : <source et date>
Limites du relevé : <aucune ou détails>
```

Si le runtime ne donne pas accès à une métrique, écrire `non disponible dans les journaux accessibles` au lieu de l'inventer. Les coûts doivent utiliser les tarifs applicables aux modèles et à la date du travail, avec la devise explicitée.
