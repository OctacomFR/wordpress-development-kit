# Rail social, liens, boutons et iframes

Référence extraite sans réécriture du snapshot `docs/AGENTS.pre-skills-snapshot.md`.

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 776-864 -->

## 9. Réseaux sociaux fixed avec libellé au hover

Lorsqu'un design prévoit des réseaux sociaux en position fixe :

- créer un seul composant rail social réutilisable ;
- `position: fixed` uniquement si la maquette ou le brief le demande ;
- chaque réseau est un vrai `<a>` ;
- icône exacte ;
- `aria-label` explicite ;
- libellé du réseau présent dans le DOM ;
- expansion au `:hover` ;
- même expansion ou équivalent au `:focus-visible` ;
- transition courte et légère ;
- ne pas masquer le contenu principal ;
- respecter les safe areas et petits écrans ;
- vérifier le z-index contre menu, cookies et modales.

Exemple de logique, à adapter aux classes réelles :

```css
.c-social-link {
  display: inline-flex;
  align-items: center;
  overflow: hidden;
}

.c-social-link__label {
  max-width: 0;
  opacity: 0;
  white-space: nowrap;
  overflow: hidden;
}

.c-social-link:hover .c-social-link__label,
.c-social-link:focus-visible .c-social-link__label {
  max-width: 10rem;
  opacity: 1;
}
```

Ne jamais faire dépendre le nom du réseau d'un `::after` uniquement : le texte doit exister dans le DOM.

---

## 10. Téléphone, email, adresse et boutons

### Téléphone

Affichage lisible, lien normalisé :

```html
<a href="tel:+33XXXXXXXXX">04 XX XX XX XX</a>
```

Ne pas inventer l'indicatif ou normaliser une donnée dont la valeur source n'est pas connue.

### Email

```html
<a href="mailto:contact@example.fr">contact@example.fr</a>
```

Pas besoin de `target="_blank"` sur `mailto:`.

### Adresse

Si une URL Maps réelle est fournie ou déjà utilisée par le site, rendre l'adresse cliquable.

Tous les liens HTTP externes s'ouvrent dans un nouvel onglet avec `rel="noopener noreferrer"`. Les liens internes restent dans le même onglet. `mailto:` et `tel:` ne reçoivent pas de `target="_blank"`.

```html
<a href="..." target="_blank" rel="noopener noreferrer">...</a>
```

### Boutons

Chaque bouton doit avoir :

- une action claire ;
- une destination réelle ;
- un libellé descriptif ;
- un état hover ;
- un état focus visible ;
- un contraste suffisant ;
- une zone tactile correcte.

Un bouton qui navigue doit être un lien, pas un faux bouton JavaScript.

---

<!-- Source : AGENTS.pre-skills-snapshot.md lignes 954-968 -->

## 12. Avis via iframe

Si le brief précise que les avis seront intégrés plus tard via iframe et demande uniquement le titre :

- créer uniquement la section et le titre demandés ;
- ne pas recopier les faux avis de la maquette ;
- ne pas fabriquer un iframe ;
- prévoir une structure qui pourra accueillir le widget sans devoir casser toute la section.

Lorsqu'un iframe réel est ajouté plus tard :

- `title` accessible obligatoire ;
- réserver la hauteur ou le ratio pour éviter le CLS ;
- lazy-load s'il est sous la ligne de flottaison et que le widget le supporte ;
- ne pas ajouter un `sandbox` susceptible de casser le widget sans vérifier sa documentation.
