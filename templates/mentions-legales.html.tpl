<!--
  MODÈLE GÉNÉRIQUE DE MENTIONS LÉGALES

  Usage :
  - obtenir chaque donnée depuis les sources validées du projet ;
  - remplacer toutes les variables délimitées par des doubles accolades ;
  - supprimer ou adapter chaque bloc conditionnel non applicable ;
  - faire valider le texte final par le client ou son conseil ;
  - construire la page avec des éléments Oxygen éditables, pas avec un unique bloc HTML opaque ;
  - ne jamais publier ce fichier avec une variable ou une condition non résolue.

  La page "Politique de protection des données" est générée et maintenue par Complianz.
  Ce modèle crée uniquement le lien vers cette page.

  Références contrôlées le 17 septembre 2026, à revérifier avant chaque publication :
  - LCEN, article 1-1 : https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000801164
  - LCEN, article 19 : https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000032236011/
  - RGPD : https://eur-lex.europa.eu/eli/reg/2016/679/oj?locale=fr
  - Exercice des droits : https://www.cnil.fr/fr/repondre-une-demande-de-droit-dacces
-->

<article class="legal-notices">
  <p>
    Dernière mise à jour : <time datetime="{{LAST_UPDATED_ISO_DATE}}">{{LAST_UPDATED_DISPLAY_DATE}}</time>
  </p>

  <p>
    Conformément notamment aux articles 1-1 et 19 de la loi n° 2004-575 du 21 juin 2004
    pour la confiance dans l'économie numérique, dite L.C.E.N., nous portons à la connaissance des
    utilisateurs et visiteurs du site
    <a href="{{SITE_URL}}">{{SITE_LABEL}}</a>
    les informations suivantes.
  </p>

  <h2>Définitions</h2>

  <p>
    <strong>Client :</strong> tout professionnel ou toute personne physique capable au sens des
    articles 1123 et suivants du Code civil, ou toute personne morale, qui visite le site objet des
    présentes conditions générales.
  </p>

  <p>
    <strong>Prestations et services :</strong>
    <a href="{{SITE_URL}}">{{SITE_LABEL}}</a> met à disposition des clients les prestations et
    services décrits sur le site.
  </p>

  <p>
    <strong>Contenu :</strong> ensemble des éléments constituant l'information présente sur le site,
    notamment les textes, images et vidéos.
  </p>

  <p>
    <strong>Informations clients :</strong> ensemble des données personnelles susceptibles d'être
    détenues par {{COMPANY_NAME}} pour la gestion de la relation client ainsi qu'à des fins d'analyse
    et de statistiques, selon les traitements réellement mis en œuvre.
  </p>

  <p><strong>Utilisateur :</strong> internaute qui se connecte au site et l'utilise.</p>

  <p>
    <strong>Informations personnelles :</strong> informations qui permettent, sous quelque forme que
    ce soit, directement ou non, l'identification des personnes physiques auxquelles elles
    s'appliquent, au sens de la législation applicable.
  </p>

  <p>
    Les termes « données à caractère personnel », « personne concernée », « sous-traitant » et
    « données sensibles » ont le sens défini par le Règlement général sur la protection des données,
    règlement UE 2016/679.
  </p>

  <h2>1. Présentation du site internet</h2>

  <p>
    En vertu de l'article 1-1 de la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l'économie
    numérique, les utilisateurs du site <a href="{{SITE_URL}}">{{SITE_LABEL}}</a> sont informés de
    l'identité des intervenants chargés de sa réalisation et de son suivi.
  </p>

  <dl>
    <dt>Éditeur du site</dt>
    <dd>
      {{COMPANY_NAME}}{{#IF_LEGAL_FORM}}, {{LEGAL_FORM}}{{/IF_LEGAL_FORM}}<br>
      {{COMPANY_ADDRESS_HTML}}<br>
      Téléphone : <a href="tel:{{COMPANY_PHONE_URI}}">{{COMPANY_PHONE_DISPLAY}}</a><br>
      Adresse électronique : <a href="mailto:{{CONTACT_EMAIL}}">{{CONTACT_EMAIL}}</a><br>
      {{#IF_COMPANY_REGISTRATION}}{{COMPANY_REGISTRATION_LABEL}} : {{COMPANY_REGISTRATION_NUMBER}}<br>{{/IF_COMPANY_REGISTRATION}}
      {{#IF_SHARE_CAPITAL}}Capital social : {{SHARE_CAPITAL}}<br>{{/IF_SHARE_CAPITAL}}
      {{#IF_VAT_NUMBER}}Numéro de TVA intracommunautaire : {{VAT_NUMBER}}{{/IF_VAT_NUMBER}}
    </dd>

    <dt>Responsable de la publication</dt>
    <dd>
      {{PUBLICATION_DIRECTOR_NAME}}, {{PUBLICATION_DIRECTOR_ROLE}}<br>
      <a href="mailto:{{CONTACT_EMAIL}}">{{CONTACT_EMAIL}}</a><br>
      {{PUBLICATION_DIRECTOR_PERSON_TYPE_SENTENCE}}
    </dd>

    <dt>Webmaster</dt>
    <dd>
      {{WEBMASTER_NAME}}<br>
      <a href="mailto:{{WEBMASTER_EMAIL}}">{{WEBMASTER_EMAIL}}</a>
    </dd>

    <dt>Hébergeur</dt>
    <dd>
      {{HOST_LEGAL_NAME}}<br>
      {{HOST_ADDRESS_HTML}}<br>
      Téléphone : <a href="tel:{{HOST_PHONE_URI}}">{{HOST_PHONE_DISPLAY}}</a>
    </dd>

    {{#IF_ADDITIONAL_STORAGE_PROVIDER}}
    <dt>Prestataire supplémentaire de stockage des données du service</dt>
    <dd>
      {{STORAGE_PROVIDER_LEGAL_NAME}}<br>
      {{STORAGE_PROVIDER_ADDRESS_HTML}}
    </dd>
    {{/IF_ADDITIONAL_STORAGE_PROVIDER}}

    <dt>Responsable du traitement des données</dt>
    <dd>
      {{DATA_CONTROLLER_NAME}}<br>
      <a href="mailto:{{DATA_CONTROLLER_EMAIL}}">{{DATA_CONTROLLER_EMAIL}}</a>
    </dd>

    {{#IF_DPO}}
    <dt>Délégué à la protection des données</dt>
    <dd>
      {{DPO_NAME}}<br>
      <a href="mailto:{{DPO_EMAIL}}">{{DPO_EMAIL}}</a>
    </dd>
    {{/IF_DPO}}

    <dt>Propriétaire du site</dt>
    <dd>{{SITE_OWNER_NAME}}<br>{{SITE_OWNER_ADDRESS_HTML}}</dd>
  </dl>

  {{#IF_REGULATED_ACTIVITY}}
  <h3>Activité réglementée</h3>
  <p>
    {{REGULATED_ACTIVITY_DISCLOSURE_TEXT}}
  </p>
  {{/IF_REGULATED_ACTIVITY}}

  <h2>2. Conditions générales d'utilisation du site et des services proposés</h2>

  <p>
    Le site constitue une œuvre de l'esprit protégée par les dispositions du Code de la propriété
    intellectuelle et des réglementations internationales applicables. Le Client ne peut pas
    réutiliser, céder ou exploiter pour son propre compte tout ou partie des éléments ou travaux du
    site sans autorisation préalable.
  </p>

  <p>
    L'utilisation du site <a href="{{SITE_URL}}">{{SITE_LABEL}}</a> implique l'acceptation pleine et
    entière des conditions générales d'utilisation décrites dans les présentes mentions légales.
    Ces conditions peuvent être modifiées ou complétées. Les utilisateurs sont invités à les
    consulter régulièrement.
  </p>

  <p>
    Le site est normalement accessible à tout moment. {{COMPANY_NAME}} peut toutefois interrompre
    l'accès pour une maintenance technique et s'efforcera, lorsque cela est possible, de communiquer
    au préalable les dates et heures de l'intervention. Le site et ses mentions légales peuvent être
    mis à jour à tout moment.
  </p>

  <h2>3. Description des services fournis</h2>

  <p>
    Le site <a href="{{SITE_URL}}">{{SITE_LABEL}}</a> a pour objet de fournir des informations sur
    les activités de {{COMPANY_NAME}}. {{COMPANY_NAME}} s'efforce de publier des informations exactes
    et à jour. Il ne peut toutefois garantir l'absence d'omissions, d'inexactitudes ou de carences de
    mise à jour, qu'elles soient de son fait ou du fait de tiers partenaires.
  </p>

  <p>
    Les informations publiées sont données à titre indicatif, peuvent évoluer et ne sont pas
    exhaustives. Elles restent soumises aux modifications intervenues depuis leur mise en ligne.
  </p>

  <h2>4. Limitations contractuelles sur les données techniques</h2>

  <p>
    Le site utilise la technologie JavaScript. {{COMPANY_NAME}} ne peut être tenu responsable de
    dommages matériels liés à l'utilisation du site. L'utilisateur s'engage à accéder au site avec
    un matériel récent, exempt de logiciel malveillant et avec un navigateur à jour.
  </p>

  <p>
    L'hébergeur assure la continuité de son service selon ses propres conditions. Il peut interrompre
    le service pour des opérations de maintenance, d'amélioration de son infrastructure, en cas de
    défaillance ou de trafic anormal.
  </p>

  <p>
    {{COMPANY_NAME}} et l'hébergeur ne peuvent être tenus responsables d'un dysfonctionnement du
    réseau Internet, des lignes de télécommunication ou du matériel de l'utilisateur empêchant
    l'accès au serveur.
  </p>

  <h2>5. Propriété intellectuelle et contrefaçons</h2>

  <p>
    {{INTELLECTUAL_PROPERTY_OWNER}} détient les droits de propriété intellectuelle ou les droits
    d'usage nécessaires sur les éléments accessibles sur le site, notamment les textes, images,
    graphismes, logos, vidéos, icônes et sons.
  </p>

  <p>
    Toute reproduction, représentation, modification, publication ou adaptation de tout ou partie
    des éléments du site est interdite sans l'autorisation écrite préalable de
    {{INTELLECTUAL_PROPERTY_OWNER}}. Toute exploitation non autorisée peut constituer une contrefaçon
    au sens des articles L.335-2 et suivants du Code de la propriété intellectuelle.
  </p>

  <h2>6. Limitations de responsabilité</h2>

  <p>
    {{COMPANY_NAME}} agit en qualité d'éditeur du site et répond du contenu qu'il publie dans les
    limites prévues par la loi.
  </p>

  <p>
    {{COMPANY_NAME}} ne peut être tenu responsable des dommages directs ou indirects causés au
    matériel de l'utilisateur lors de l'accès au site et résultant soit de l'utilisation d'un
    matériel qui ne répond pas aux prérequis indiqués à la section 4, soit de l'apparition d'un bug ou
    d'une incompatibilité.
  </p>

  <p>
    {{COMPANY_NAME}} ne peut pas non plus être tenu responsable des dommages indirects consécutifs à
    l'utilisation du site, dans les limites permises par la loi.
  </p>

  {{#IF_INTERACTIVE_AREAS}}
  <p>
    Des espaces interactifs permettent aux utilisateurs de transmettre du contenu. {{COMPANY_NAME}}
    se réserve le droit de supprimer, sans mise en demeure préalable, tout contenu contraire à la
    législation française et de mettre en cause la responsabilité civile ou pénale de son auteur.
  </p>
  {{/IF_INTERACTIVE_AREAS}}

  <h2>7. Gestion des données personnelles</h2>

  <p>
    Le Client est informé des règles applicables à la protection des données personnelles, notamment
    la loi Informatique et Libertés et le règlement UE 2016/679. Pour connaître les traitements mis en
    œuvre, consulter la
    <a href="{{PRIVACY_POLICY_URL}}">Politique de protection des données</a> générée avec Complianz.
  </p>

  <h3>7.1. Responsable du traitement</h3>

  <p>
    Le responsable du traitement est {{DATA_CONTROLLER_NAME}}, représenté par
    {{DATA_CONTROLLER_REPRESENTATIVE}}. Il détermine les finalités des traitements, informe les
    personnes concernées et maintient la documentation requise. Il prend les mesures raisonnables
    pour assurer l'exactitude et la pertinence des données au regard des finalités déclarées.
  </p>

  <h3>7.2. Finalités des données collectées</h3>

  <p>{{COMPANY_NAME}} traite uniquement les données nécessaires aux finalités validées suivantes :</p>

  <ul>
    {{DATA_PROCESSING_PURPOSES_LI}}
  </ul>

  <p>
    {{DATA_SALE_STATEMENT}}
  </p>

  <h3>7.3. Droits des personnes</h3>

  <p>Selon la réglementation applicable, les utilisateurs disposent notamment des droits suivants :</p>

  <ul>
    <li>droit d'accès et de rectification de leurs données ;</li>
    <li>droit à l'effacement lorsque les conditions légales sont réunies ;</li>
    <li>droit de retirer leur consentement à tout moment pour les traitements fondés sur celui-ci ;</li>
    <li>droit à la limitation du traitement ;</li>
    <li>droit d'opposition au traitement ;</li>
    <li>droit à la portabilité pour les traitements qui y sont éligibles ;</li>
    <li>droit de définir des directives relatives au sort de leurs données après leur décès.</li>
  </ul>

  <p>
    Pour exercer ses droits, l'utilisateur peut contacter {{DATA_CONTROLLER_NAME}} à l'adresse
    <a href="mailto:{{DATA_RIGHTS_EMAIL}}">{{DATA_RIGHTS_EMAIL}}</a> ou par courrier :
  </p>

  <address>
    {{DATA_RIGHTS_POSTAL_ADDRESS_HTML}}
  </address>

  <p>
    La demande doit permettre d'identifier son auteur et de préciser les données ou traitements
    concernés. Une preuve d'identité ne doit être demandée qu'en cas de doute raisonnable sur
    l'identité du demandeur, selon les règles applicables. Les demandes restent soumises aux
    obligations légales de conservation et d'archivage.
  </p>

  <p>
    L'utilisateur peut déposer une réclamation auprès de la CNIL :
    <a href="https://www.cnil.fr/fr/plaintes" target="_blank" rel="noopener noreferrer">déposer une plainte auprès de la CNIL</a>.
  </p>

  <h3>7.4. Destinataires et transferts</h3>

  <p>
    {{DATA_RECIPIENTS_AND_TRANSFERS_TEXT}}
  </p>

  <p>
    {{COMPANY_NAME}} choisit ses sous-traitants selon les garanties qu'ils apportent au regard du
    règlement UE 2016/679 et prend les mesures nécessaires pour protéger les informations contre les
    accès, usages ou divulgations non autorisés.
  </p>

  <h3>7.5. Types de données et durée de conservation</h3>

  <ul>
    {{COLLECTED_DATA_TYPES_LI}}
  </ul>

  <p>{{DATA_RETENTION_TEXT}}</p>

  <h2>8. Notification d'incident</h2>

  <p>
    Aucune méthode de transmission sur Internet ni méthode de stockage électronique ne garantit une
    sécurité absolue. En cas de violation de données personnelles, {{COMPANY_NAME}} applique les
    procédures de notification prévues par la réglementation et informe les personnes concernées
    lorsque la loi l'exige.
  </p>

  <p>
    Aucune information personnelle n'est publiée à l'insu de l'utilisateur, ni cédée ou vendue à des
    tiers en dehors des cas prévus dans la politique de protection des données. En cas de transmission
    de l'activité, le successeur reste tenu par les obligations applicables aux données reçues.
  </p>

  <h3>8.1. Sécurité</h3>

  <p>
    {{SECURITY_MEASURES_TEXT}}
  </p>

  <h2>9. Droit applicable et attribution de juridiction</h2>

  <p>
    Les présentes conditions d'utilisation sont régies par le droit français. Tout litige est porté
    devant les juridictions compétentes selon les règles légales applicables.
  </p>
</article>
