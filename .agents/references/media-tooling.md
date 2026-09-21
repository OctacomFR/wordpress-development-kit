# Outillage obligatoire des médias

Lire cette procédure avant toute transformation d'un fichier image ou vidéo destiné au site.

## Outils imposés

- Utiliser ImageMagick, via la commande `magick`, pour manipuler les images raster : orientation, conversion en WebP, redimensionnement, recadrage, compression, suppression de métadonnées et génération de vignettes.
- Utiliser FFmpeg, via la commande `ffmpeg`, pour manipuler les vidéos : transcodage, redimensionnement, compression, découpe, changement de conteneur et extraction d'une affiche ou d'une vignette. Inspecter les fichiers vidéo avec `ffprobe`.
- Utiliser une chaîne vectorielle pour les SVG. Conserver le `viewBox`, optimiser et assainir le fichier sans le rasteriser avec ImageMagick.
- Python peut orchestrer un traitement par lot et appeler ces commandes. Il ne remplace pas ImageMagick ou FFmpeg comme moteur de transformation.

Cette règle concerne la création ou la modification des fichiers. Les réglages d'affichage Oxygen ou CSS, tels que `object-fit`, `object-position`, le ratio et la taille rendue, restent gérés dans Oxygen/CSS.

Si `magick`, `ffmpeg` ou `ffprobe` manque ou échoue, suspendre la transformation dépendante. Installer ou faire installer l'outil requis au lieu d'utiliser silencieusement une autre bibliothèque, un service en ligne ou un réencodage par navigateur.

## Procédure

1. Conserver l'original de travail hors des assets de production et produire un fichier dérivé distinct.
2. Vérifier la disponibilité et la version de l'outil requis avant le traitement.
3. Inspecter le fichier source, puis choisir les paramètres à partir du rôle du média, de Figma et des contraintes du projet. Ne pas appliquer une qualité, une résolution, un ratio ou un codec universel.
4. Exécuter la transformation avec `magick` pour un raster ou `ffmpeg` pour une vidéo.
5. Inspecter le résultat avec `magick identify` pour une image, ou `ffprobe` pour une vidéo.
6. Contrôler visuellement le fichier dérivé avant import : cadrage, orientation, ratio, transparence, couleurs, netteté et artefacts. Pour une vidéo, vérifier aussi la durée, les flux audio, la résolution, la rotation et la lecture.
7. Consigner l'outil, sa version, la commande exécutée, le fichier source, le fichier produit, ses dimensions et son poids. Pour une vidéo, ajouter les codecs et la durée. Cette trace constitue la preuve utilisée pendant la QA.

Ne jamais écraser l'unique original ni déclarer une optimisation terminée sur la seule réussite de la commande.
