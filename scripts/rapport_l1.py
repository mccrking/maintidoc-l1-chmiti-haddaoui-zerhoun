from reportlab.platypus import Flowable,Spacer
from reportlab.lib import colors

ARCHITECTURE='''flowchart TD
 UI[Interface : question et photo] -->|identité, question, image| API[API : authentification et validation]
 API -->|requête et groupes autorisés| ORCH[Orchestration : plan et états]
 ORCH -->|image sans secret| VLM[Modèle vision-langage]
 VLM -->|description et incertitude| ORCH
 ORCH -->|requête avec filtre de groupes| RAG[Recherche documentaire]
 RAG -->|passages, figures, versions, pages| ORCH
 STORE[(Stockage : documents, index, métadonnées)] --> RAG
 ORCH -->|équipement autorisé| MCP[Outil MCP : historique et tickets]
 MCP -->|historique fictif ou résultat contrôlé| ORCH
 ORCH --> CIT[Validation des citations]
 CIT -->|réponse sourcée ou demande de précision| UI
 ORCH --> PRE[Prévisualisation du ticket]
 PRE -->|approbation liée au contenu| HUMAN[Technicien]
 HUMAN -->|accord explicite et droits revérifiés| MCP
'''
INGESTION='''flowchart LR
 A[Document candidat] --> H[Relecture humaine et droits]
 H -->|admis seulement| I[Inventaire UTF-8]
 I --> F{Format}
 F -->|PDF texte| T[Extraction par page]
 F -->|scan| O[OCR et contrôle visuel]
 T --> C[Passages, tableaux et figures]
 O --> C
 C --> M[ID, version, page, élément, équipement, groupes]
 M --> E[Embeddings]
 E --> V[Index avec filtre d’accès]
'''
TICKET='''sequenceDiagram
 participant U as Technicien
 participant A as Orchestrateur
 participant M as MCP
 U->>A: Demande documentaire
 A->>U: Brouillon du ticket et citations
 U->>A: Approbation du contenu exact
 A->>A: Vérifier identité, groupe, hash du brouillon
 A->>M: create_ticket(draft, approval, idempotency_key)
 M->>M: Vérifier droits, approbation et absence de doublon
 M-->>A: Identifiant ou résultat déjà enregistré
 A-->>U: Statut confirmé, sans nouvel appel automatique
'''

class Architecture(Flowable):
 def __init__(self,width):super().__init__();self.width=width;self.height=360
 def draw(self):
  c=self.canv;w=self.width;navy=colors.HexColor('#19354A');teal=colors.HexColor('#087F8C');pale=colors.HexColor('#EDF5F6')
  def box(x,y,ww,hh,t,sub):
   c.setFillColor(pale);c.setStrokeColor(teal);c.roundRect(x,y,ww,hh,4,fill=1,stroke=1)
   c.setFillColor(navy);c.setFont('AB',10);c.drawCentredString(x+ww/2,y+hh-17,t)
   c.setFont('A',8);c.drawCentredString(x+ww/2,y+12,sub)
  def arrow(x,y,xx,yy,label=''):
   c.setStrokeColor(teal);c.line(x,y,xx,yy)
   if yy<y:c.line(xx-3,yy+5,xx,yy);c.line(xx+3,yy+5,xx,yy)
   if label:c.setFont('A',7.5);c.setFillColor(navy);c.drawString((x+xx)/2+5,(y+yy)/2,label)
  mid=w/2;bw=220
  box(mid-bw/2,307,bw,45,'Interface','Question + photo ; réponse et prévisualisation')
  box(mid-bw/2,241,bw,45,'API et accès','Identité vérifiée ; groupes autorisés')
  box(mid-bw/2,175,bw,45,'Orchestration','Plan ; abstention ; contrôle des citations')
  arrow(mid,307,mid,286,'requête / identité')
  arrow(mid,241,mid,220,'contexte autorisé')
  small=(w-24)/3
  box(0,82,small,53,'Vision-langage','Image : description, incertitude')
  box(small+12,82,small,53,'Recherche RAG','Filtre avant recherche ; pages')
  box(2*(small+12),82,small,53,'Outil MCP','Historique ; ticket approuvé')
  for x in [small/2,w/2,w-small/2]:arrow(mid,175,x,135)
  box(0,4,w,47,'Stockage : documents, index et métadonnées','Versions, équipements, groupes ; journaux sans secrets')
  arrow(w/2,82,w/2,51)
  c.setFont('AI',7.4);c.setFillColor(navy)
  c.drawString(0,65,'Action ticket : approbation humaine + droits revérifiés côté MCP + clé d’idempotence.')

def report_pages(P,H,T,D,W,C):
 pages=[]
 def page(title,*objects):pages.append([P(title,'title'),*objects])
 page('1. Cadrage du projet',
  P('MaintiDoc - Parc informatique pédagogique','h'),
  P('Livrable 1 sur 6 | Module IA générative multimodale - EMSI 2026 | 1 novembre 2026','small'),
  P('Équipe : Mehdi Chmiti, Ismail Haddaoui et Ayman Zerhoun. Nom normalisé : CHMITI-HADDAOUI-ZERHOUN. Enseignante : Pr. Mariam CHERRABI. Ce dossier prépare les décisions de la semaine 1 ; le prototype complet reste à construire.'),
  H('Contexte et utilisateurs'),
  P('Un technicien doit retrouver rapidement une procédure adaptée à un poste ou à un périphérique, comprendre un message affiché et préparer un ticket sans recopier des secrets. Un responsable de maintenance doit contrôler les versions, les droits et les propositions d’action. Le terrain choisi est un parc pédagogique fictif : aucune intervention réelle ni donnée d’utilisateur n’est présentée.'),
  H('Deux familles retenues'),
  P('Famille 1 : postes informatiques sous Windows 11, incluant leur configuration réseau, Firefox et le stockage. Famille 2 : périphériques informatiques, notamment imprimante, station USB-C, accessoire Bluetooth, caméra, microphone et sortie audio. Les logiciels sont des composants des postes ; ils ne forment pas une troisième famille.'),
  T(['Cas d’usage','Besoin et résultat attendu'],[
   ('UC1 - Réseau','Comprendre un poste connecté sans Internet ; citer une procédure et une page.'),
   ('UC2 - Impression','Lire un état ou une file d’attente ; distinguer hors connexion et blocage.'),
   ('UC3 - Image et son','Distinguer caméra, entrée microphone et sortie audio ; demander le matériel concerné.'),
   ('UC4 - Versions','Comparer deux procédures contradictoires et identifier la version courante.'),
   ('UC5 - Ticket','Préparer un ticket sur un équipement autorisé ; le créer seulement après approbation.')],[110,W-110]))
 page('1. Cadrage : objectifs et limites',
  H('Objectifs vérifiables pour la semaine 6'),
  T(['Objectif','Comment vérifier le comportement'],[
   ('Réponse justifiée','Une question connue reçoit des citations document_id, version et page qui soutiennent les affirmations.'),
   ('Image incertaine','Une image illisible ou sans équipement identifiable entraîne une demande de précision.'),
   ('Accès séparés','Un technicien des postes ne reçoit aucun passage réservé aux périphériques.'),
   ('Versions distinguées','La réponse sur le délai courant signale 30 / 60 secondes et cite la version v2 du scénario.'),
   ('Action contrôlée','Sans approbation valide, create_ticket est refusé ; rejouer une requête ne crée pas de doublon.'),
   ('Injection ignorée','Le texte piégé ne change ni le filtrage, ni les citations, ni les conditions d’appel MCP.')],[110,W-110]),
  P('Ces objectifs définissent des comportements à observer. Aucun score de précision, de rappel ni de temps de réponse n’est revendiqué ; les indicateurs chiffrés seront fixés en semaine 5.'),
  H('Périmètre et hors-périmètre'),
  P('Entrées : question en français, photo ou capture autorisée et identifiant d’équipement. Sorties : réponse sourcée, demande de précision ou brouillon de ticket. Outils MCP envisagés : consultation d’historiques fictifs et création contrôlée de ticket. Sont exclus : pilotage du matériel, diagnostic garanti, modification automatique de Windows, contournement de BitLocker et intervention autonome.'),
  H('Hypothèses et ressources'),
  P('Relevé du poste de travail : 15,6 Gio de RAM utilisable et NVIDIA GeForce RTX 4050 Laptop GPU, 6 141 Mio de VRAM déclarés par nvidia-smi. Cela ne prouve pas qu’un VLM donné fonctionne sur cette configuration. Le modèle, sa quantification et sa consommation seront testés en semaine 2. Le temps hebdomadaire de chaque membre reste à confirmer.'))
 page('2. Constitution du corpus',
  H('Volume et organisation'),
  P('La proposition comporte 36 documents de trois pages chacun, soit 108 pages. Le format de trois pages conserve le choix de présentation initial ; il n’est pas imposé par la consigne L1. Les 29 fiches techniques utiles du corpus V2.2 sont adaptées ; le cas Cloudflare est remplacé par un tableau de codes locaux, et six documents complémentaires sont ajoutés.'),
  T(['Famille','Nb.','Équipements de démonstration'],[
   ('Postes informatiques',str(C['familles']['postes_informatiques']),'PC-A-01'),
   ('Périphériques informatiques',str(C['familles']['peripheriques_informatiques']),'IMP-A-01, USB-A-01, BT-A-01, CAM-A-01, MIC-A-01, AUD-A-01')],[130,65,W-195]),
  H('Diversité documentaire'),
  T(['Type','Nombre','Apport au projet'],[(k,str(v),{'procedure':'Constats, actions et critères de contrôle ; comprend les tests de versions et d’injection.','manuel':'Organisation des deux parcs fictifs, équipements et renvois.','codes_alarme':'Codes locaux fictifs ; aucune erreur Windows inventée.','fiche_securite':'Préservation des données et contrôle des tickets.'}[k]) for k,v in C['types'].items()],[100,55,W-155]),
  H('Éléments multimodaux et OCR'),
  P('Les 36 documents comportent au moins un tableau ou schéma exploitable, indiqué avec sa page dans l’inventaire. Les deux procédures proc_impression_v1 et proc_impression_v2 sont des scans synthétiques : leurs pages sont des images, sans couche de texte. Elles permettent de préparer les tests OCR sans revendiquer une numérisation physique. Aucun résultat d’OCR n’est encore mesuré.'),
  H('Nature des documents'),
  P('Les textes et schémas sont des productions synthétiques originales. Microsoft et Mozilla servent de sources techniques de travail pour les fiches reprises. Aucun manuel complet, logo ou photographie propriétaire n’est redistribué. Le parc, ses règles locales et ses identifiants ne correspondent pas à une installation réelle.'))
 page('2. Corpus : contrôle et usage de l’IA',
  H('Admission : un contrôle humain reste indispensable'),
  P('L’assistant a contrôlé la structure, les références internes, la pagination et les éléments de test. Ces contrôles ne remplacent pas la relecture de l’équipe. Les 36 champs verifie_par sont encore vides. Le dossier est publié dans le dépôt GitHub public de mccrking ; son accès sans connexion a été vérifié. Les documents restent candidats, exclus de l’index opérationnel jusqu’à validation. Avant remise : vérifier chaque contenu, renseigner un prénom réel et les corrections effectives, puis valider les droits.'),
  H('Traçabilité et conditions de réutilisation'),
  P('inventaire.csv est encodé en UTF-8, séparé par des virgules, avec les 20 colonnes prescrites. Un fichier correspond à une ligne et porte son document_id en minuscules. prompts_corpus.md distingue les demandes utilisateur conservées, les instructions de révision et la nouvelle génération. sources_travail.csv conserve les URL et langues des références. licence=synthetique décrit le document produit ; ce champ n’attribue aucune licence libre aux publications des éditeurs.'),
  H('Analyse critique de l’assistance IA'),
  P('La première difficulté a été un cadrage incomplet : des fiches utiles au support informatique avaient été considérées comme suffisantes, avant lecture des consignes détaillées. Le corpus ne préparait alors ni l’OCR, ni les contradictions, ni l’injection, ni les groupes d’accès. La correction consiste à traiter les exigences L1 comme une liste d’admission, pas seulement à compter les fichiers.'),
  P('Les diagrammes initiaux perdaient leur sens à l’extraction ; ils ont été remplacés par des règles conditionnelles lisibles. Les identifiants des fiches et sources ont été séparés. Les menus français ont été rapprochés des pages officielles françaises sans affirmer qu’une version logicielle a été testée. Le cas Cloudflare a été retiré car son administration dépassait le parc retenu.'),
  P('L’historique exact de toutes les instructions initiales n’avait pas été sauvegardé. Il serait incorrect de fabriquer des prompts ou leurs dates. Le fichier de trace signale cette lacune et enregistre les nouvelles instructions. Enfin, une traduction officielle peut elle-même être automatique : son origine ne dispense pas de relire. L’équipe doit vérifier les points techniques et les droits avant de signer l’inventaire.'))
 page('3. Architecture cible',
  P('Le schéma décrit le système à construire, pas le serveur Docker déjà installé. Les choix d’outils sont des options de travail ; les versions, licences des outils et mesures de mémoire seront fixées à partir de la semaine 2.'),
  Architecture(W),
  H('Trois points de contrôle'),
  P('Accès : l’API établit les groupes à partir de l’identité ; le moteur applique le filtre avant recherche et reranking. Citations : avant réponse, les identifiants, pages, versions et passages sont contrôlés ; une preuve insuffisante entraîne une abstention. Action : un ticket ne peut être créé qu’avec une approbation liée au brouillon et vérifiée à nouveau par l’outil MCP.'),
  P('Les fichiers sources Mermaid se trouvent dans docs/diagrammes/. Ils décrivent aussi les retours vers l’orchestrateur et la branche d’approbation humaine. Les journaux de démonstration ne contiendront pas de données privées.'))
 page('3. Fiches des blocs : entrée et recherche',
  T(['Bloc et rôle','Entrées','Sorties','Outil envisagé'],[
   ('Interface : recueillir la demande et montrer les preuves','Question, image autorisée, sélection de l’équipement','Requête ; réponse ; accord ou refus sur un ticket','Interface web simple, outil à préciser'),
   ('API : vérifier identité et format','Session, requête, fichier image','Contexte autorisé, groupes, erreur de validation','API Python, par exemple FastAPI'),
   ('Orchestration : choisir la suite du traitement','Demande validée, description visuelle, preuves, état du ticket','Appels de recherche/MCP ; réponse ; abstention','Machine à états Python ; LangGraph envisagé'),
   ('Recherche : sélectionner les preuves autorisées','Question, équipement, groupes, versions','Passages et figures avec pages et scores internes','Recherche lexicale et vectorielle ; Qdrant envisagé')],[125,115,130,W-370]),
  H('Contraintes de conception'),
  P('Le client ne fournit pas lui-même ses droits. Les filtres viennent du contexte authentifié et doivent être appliqués avant que les passages entrent dans le contexte du modèle. Le titre et la catégorie facilitent la recherche, mais ne remplacent pas le contrôle de groupe ni la provenance de la preuve.'),
  P('Une procédure archivée peut rester consultable pour expliquer une contradiction. Elle ne doit pas remplacer silencieusement la version courante. Les champs version et usage_test servent à cette distinction, en complément du contenu explicite des deux procédures.'),
  H('Hypothèses à vérifier'),
  P('Le découpage par page du corpus antérieur est un point de départ, pas une taille optimale démontrée. Il faudra tester les limites entre tableau et explication, les recherches par code exact et les questions formulées autrement. Les demandes couvertes déjà présentes dans les fiches ne constituent pas un jeu d’évaluation indépendant.'))
 page('3. Fiches des blocs : vision, MCP et stockage',
  T(['Bloc et rôle','Entrées','Sorties','Outil envisagé'],[
   ('Vision-langage : interpréter une image sans certifier le diagnostic','Photo/capture autorisée ; question ; contexte du parc','Description ; indices ; équipement candidat ; incertitude','VLM local de taille compatible ; modèle à tester'),
   ('MCP : exposer les historiques et l’action ticket','Équipement autorisé ; brouillon approuvé ; clé de rejeu','Historique fictif ; identifiant du ticket ou refus','Serveur MCP local ; stockage fictif SQLite ou JSON'),
   ('Stockage : conserver les documents et les index','PDF/images ; inventaire ; passages ; groupes','Documents versionnés, métadonnées, index et journaux','Volume Docker ; index vectoriel envisagé ; Git pour les sources')],[125,115,130,W-370]),
  H('Lecture et écriture séparées'),
  P('get_history(equipement_id) lit un historique fictif après contrôle de l’équipement et des groupes. create_ticket(draft, approval, idempotency_key) est une écriture sensible. Un historique ne peut jamais autoriser une action. Une instruction présente dans un document ne peut pas fournir une approbation humaine.'),
  H('Ressources et solution de repli'),
  P('La VRAM disponible est limitée à environ 6 Gio sur le poste relevé. Il reste à mesurer le chargement, la mémoire de contexte et le coût des images pour le modèle choisi. Un modèle plus petit, une quantification adaptée ou une exécution CPU plus lente peuvent servir de repli. Aucun débit ni compatibilité n’est garanti avant essai.'),
  H('Questions ouvertes'),
  P('Quels formats d’image retenir ? Quel modèle gère correctement les tableaux français ? Quel OCR lit les scans sans confondre 30 et 60 ? Comment les références de figures seront-elles conservées ? Le choix final devra aussi vérifier les conditions d’utilisation des modèles et bibliothèques.'))
 page('3. Parcours d’une requête',
  H('Exemple : « Mon imprimante reste bloquée »'),
  T(['Étape','Traitement attendu et contrôle'],[
   ('1 - Identifier','L’API reconnaît un technicien des périphériques et récupère ses groupes autorisés. Elle valide la taille et le type de la photo.'),
   ('2 - Comprendre l’image','Le VLM décrit l’état visible et propose IMP-A-01 seulement si l’identification est étayée. Une photo ambiguë appelle une question.'),
   ('3 - Rechercher','La recherche filtre les groupes, puis consulte it23 et it24. La requête distingue état hors connexion et travail bloqué.'),
   ('4 - Compléter','Si utile, get_history consulte l’historique fictif de l’imprimante autorisée ; aucune action n’est déclenchée.'),
   ('5 - Répondre','L’orchestrateur cite le document, sa version et la page ; il sépare observation, hypothèse et action proposée.'),
   ('6 - Vérifier','Le contrôle confirme que la citation existe et soutient le conseil. Si les preuves manquent, la réponse le dit.'),
   ('7 - Préparer un ticket','Le technicien voit un brouillon, puis approuve ou refuse. L’écriture MCP reste bloquée tant que les conditions ne sont pas réunies.')],[100,W-100]),
  H('Cas limites à conserver'),
  P('Une image de voyant sans modèle ne suffit pas à déduire sa signification. Le manuel des périphériques interdit d’inventer une caractéristique commerciale. Une sortie audio silencieuse et un microphone muet sont deux fonctions différentes. Les fiches it14, it27 et it30 sont marquées ambigu pour préparer ce test.'),
  P('Si la note piégée est trouvée par un responsable, seule son information documentaire utile peut être citée. La tentative de créer un ticket sans approbation reste une donnée hostile. Le système ne doit pas transformer le texte source en instruction de contrôle.'))
 page('4. Flux d’ingestion et métadonnées',
  D(['Candidat relu et admis','Extraction / OCR','Passages et éléments'],'Puis : embeddings, indexation avec métadonnées et filtre d’accès.'),
  P('Le pipeline commence par l’admission, pas par les embeddings. Vérifier le fichier, les droits de réutilisation et l’inventaire. Les champs non signés restent exclus de l’index opérationnel. Les PDF texte sont extraits par page ; les scans sont envoyés à un OCR local, avec contrôle visuel des champs critiques.'),
  T(['Métadonnée','Exemple et fonction'],[
   ('document_id, version','it24 ; v3.0 (2026-11-01) : identifier exactement la preuve'),
   ('page, element_id','2 ; it24_p2_table1 : conserver le lien avec le tableau et l’image source'),
   ('famille, equipement_id','peripheriques_informatiques ; IMP-A-01 : limiter le contexte matériel'),
   ('groupes_acces','techniciens_peripheriques ; responsables : filtrer avant recherche'),
   ('format, langue, provenance','pdf_scanne ; fr ; synthetique : choisir l’OCR et exposer l’origine'),
   ('usage_test, statut_validation','contradictoire ; admis après signature réelle : isoler les tests et l’admission')],[150,W-150]),
  H('Conservation des preuves et des versions'),
  P('Conserver les coordonnées ou l’image d’un tableau pour vérifier les lectures OCR. Le texte de référence des scans sert au contrôle hors index ; il ne doit pas être injecté comme résultat d’OCR supposé. Une correction crée une nouvelle version et entraîne la réindexation des éléments concernés.'),
  P('Les en-têtes et pieds répétitifs sont exclus du texte recherché. Les identifiants, pages, versions et groupes restent des métadonnées. Le corpus antérieur et sa représentation JSONL ne doivent pas être ingérés en parallèle sans déduplication. Les scans et le document piégé restent identifiés dans l’inventaire.'))
 page('4. Flux de requête et modèle d’accès',
  H('Trois groupes fictifs'),
  T(['Groupe','Documents accessibles','Restriction'],[
   ('techniciens_postes','Famille des postes, sauf it22 réservé aux responsables','Aucun document des périphériques ; aucune clé BitLocker stockée'),
   ('techniciens_peripheriques','Famille des périphériques, sauf la note d’injection','Aucun document des postes sans autorisation supplémentaire'),
   ('responsables','Vue transversale des deux familles ; tests dédiés','La permission de lire n’autorise pas une création de ticket non approuvée')],[125,195,W-320]),
  H('Contrôle de bout en bout'),
  P('L’API déduit les groupes d’une identité fictive configurée côté serveur. L’orchestrateur transmet un filtre obligatoire à la recherche. Le contrôle doit aussi couvrir les caches, le reranking, les historiques MCP et les téléchargements directs. Une réponse ne doit pas laisser deviner le contenu d’un document exclu.'),
  H('Exemple de refus'),
  P('Un technicien des postes demande la procédure d’imprimante réservée aux périphériques : le moteur ne retourne pas cette preuve et la réponse explique que les sources autorisées ne suffisent pas. Un utilisateur appartenant à deux groupes reçoit l’union de leurs documents, après contrôle explicite de ses appartenances.'),
  H('Différence entre stockage actuel et cible sécurisée'),
  P('Le service Nginx actuel expose le corpus V2.2 sur 127.0.0.1:8080 et monte son volume en lecture seule. Il n’implémente ni authentification applicative ni séparation de groupes. La proposition L1 de 36 documents est conservée à part et n’est pas présentée comme déjà sécurisée par ce service.'),
  P('Les noms des membres figurent dans le rapport et le README. Les futures sessions de test utilisent des identités fictives ; les fichiers .env, clés et mots de passe sont exclus du dépôt. Les données utiles du corpus n’exigent aucun document personnel réel.'))
 page('4. Création de ticket et approbation',
  D(['Brouillon et preuves','Approbation explicite','Écriture MCP contrôlée'],'Une demande documentaire seule ne déclenche aucune écriture.'),
  H('Préparer'),
  P('Le brouillon contient l’équipement, le symptôme, les observations disponibles, les documents/pages utilisés et l’action demandée. Il ne contient aucun secret. Le technicien voit les champs exacts avant de décider. Une donnée inconnue n’est pas complétée par une intervention fictive présentée comme réelle.'),
  H('Approuver'),
  P('L’accord est lié à l’identité, à l’équipement et à une empreinte du contenu présenté. Il est enregistré côté serveur, possède une durée de validité à définir et ne peut pas provenir d’un passage de document. Toute modification du brouillon invalide l’accord et impose une nouvelle prévisualisation.'),
  H('Appeler MCP une seule fois utilement'),
  P('create_ticket revérifie les droits et l’accord. Une clé d’idempotence stable désigne la même demande approuvée ; une contrainte d’unicité conserve le résultat du premier appel. En cas de timeout, le système recherche ce résultat ou rejoue avec la même clé. Il ne change pas de clé pour forcer une deuxième création.'),
  T(['Situation','Résultat attendu'],[
   ('Absence ou refus d’accord','Aucun ticket créé ; conserver au plus le brouillon autorisé'),
   ('Brouillon changé après accord','Ancien accord rejeté ; nouvelle validation demandée'),
   ('Même demande rejouée','Même identifiant de ticket restitué ; aucun doublon'),
   ('Instruction dans la note piégée','Aucun effet sur les droits ou l’approbation')],[180,W-180]),
  P('Le journal conserve l’identifiant de demande, le statut d’approbation et l’identifiant du ticket fictif, sans clé privée ni contenu sensible. Ces mécanismes sont une cible de conception à implémenter et à tester.'))
 page('5. Analyse des risques',
  P('Échelle de travail : probabilité 1 faible, 2 moyenne, 3 forte ; impact 1 limité, 2 significatif, 3 majeur. Ces niveaux sont une estimation de conception, pas des fréquences mesurées. Les responsabilités ci-dessous sont proposées et doivent être confirmées par l’équipe.'),
  T(['Risque / catégorie','P','I','Mesure prévue','Responsable proposé'],[
   ('Hallucination ou citation non fondée / données','2','3','Contrôle des pages et des preuves ; abstention si insuffisant','Mehdi'),
   ('Fuite entre groupes / sécurité','2','3','Filtre avant recherche ; tests croisés et contrôle des caches','Ismail'),
   ('Ticket sans approbation / sécurité','2','3','Accord lié au contenu, revérifié côté outil MCP','Ismail'),
   ('Doublon de ticket / technique','2','2','Clé d’idempotence et unicité du résultat','Ismail'),
   ('Injection documentaire / sécurité','2','3','Sources traitées comme données ; note piégée de test','Ayman'),
   ('Erreur IA dans une fiche / données','2','3','Relecture signée, références et corrections par document','Ayman'),
   ('Droits de réutilisation incertains / données','2','3','Exclusion avant admission ; privilégier textes et schémas originaux','Ayman'),
   ('Mémoire GPU insuffisante / technique','3','2','Mesure S2 ; modèle plus petit ou repli CPU à tester','Mehdi'),
   ('Erreur OCR sur 30 / 60 / technique','2','2','Comparaison visuelle ; référence hors index ; abstention','Mehdi'),
   ('Retard ou rôle mal réparti / organisation','2','2','Jalon hebdomadaire, tâches courtes et suppléance','Toute l’équipe')],[125,20,20,205,W-370]),
  H('Priorités'),
  P('Bloquer en priorité les fuites et écritures non approuvées. La capacité GPU est incertaine mais ne justifie pas de supprimer les contrôles. La relecture et les droits des documents constituent un jalon d’admission avant la construction de l’index.'))
 page('6. Planning et répartition des rôles',
  H('Organisation proposée, à confirmer'),
  T(['Membre','Responsabilité principale','Suppléance'],[
   ('Mehdi Chmiti','Architecture, ingestion/OCR, stockage et mesures du poste','Revue du code avec Ismail'),
   ('Ismail Haddaoui','API, accès, serveur MCP et validation des tickets','Tests d’accès avec Ayman'),
   ('Ayman Zerhoun','Qualité du corpus, sources, prompts et scénarios d’évaluation','Relecture du rapport avec Mehdi')],[105,255,W-360]),
  H('Semaines 2 à 6'),
  T(['Semaine','Travail prévu','Preuve de fin de semaine'],[
   ('S2','Admettre le corpus relu ; OCR ; choix des outils et mesures mémoire','Inventaire signé, ingestion reproductible et essais du modèle consignés'),
   ('S3','Recherche documentaire et citations ; maintien des versions','Questions de contrôle avec preuves exactes et tests de refus'),
   ('S4','Vision-langage, historique MCP et parcours du ticket','Démonstration avec image ; action bloquée sans approbation'),
   ('S5','Définir les métriques ; tests indépendants et attaques documentaires','Résultats réels sur accès, OCR, contradictions, injection et idempotence'),
   ('S6','Corriger, documenter et présenter le prototype','Démonstration reproductible ; limites et résultats mesurés')],[55,235,W-290]),
  H('Suivi et contraintes'),
  P('Chaque membre confirme sa disponibilité hebdomadaire avant de figer la charge. Un point d’avancement rassemble les tâches finies, les blocages et le prochain essai. Les erreurs repérées par un autre membre sont consignées dans Git. La date et l’heure exactes du rendu restent celles communiquées sur Classroom ; aucune échéance n’est inventée ici.'),
  P('La répartition est une proposition de travail, pas une preuve d’accord déjà obtenu. Un retard sur le modèle vision ne doit pas empêcher les tests de corpus, d’accès et de tickets. Une solution plus légère doit être comparée sur le matériel disponible.'))
 page('6. État du dossier et préparation de la remise',
  H('Ce qui est produit et contrôlé'),
  P('Le rapport compte 15 pages : une page de garde et 14 pages de contenu, hors annexes. Le dossier contient 36 PDF de trois pages, un inventaire à 20 colonnes, les prompts disponibles, les sources de travail et les trois diagrammes Mermaid dans le dépôt local. Les scans sont sans texte sélectionnable. Les deux versions contradictoires et l’injection sont identifiées. Les noms des fichiers correspondent aux identifiants de l’inventaire.'),
  H('Ce qui empêche encore une remise conforme'),
  P('Le dossier est publié dans le dépôt public github.com/mccrking/maintidoc-l1-chmiti-haddaoui-zerhoun. Son URL réelle figure dans le fichier de lien. L’accès sans authentification a été vérifié ; l’équipe doit contrôler à nouveau ce lien au moment du dépôt. La relecture humaine et la validation des droits des documents restent à faire : verifie_par est vide. Le ZIP demeure une version de préparation ; aucun contrôle logiciel ne remplace cette validation.'),
  H('Dernière vérification par l’équipe'),
  T(['Point à terminer','Action requise'],[
   ('Documents et licences','Relire les 36 documents, vérifier les sources, renseigner le relecteur et les corrections réelles'),
   ('Prompts','Confirmer la trace disponible ; conserver la limite historique au lieu d’inventer des instructions'),
   ('GitHub','Accès public vérifié ; contrôler à nouveau le lien au moment du dépôt'),
   ('Rapport et README','Confirmer les rôles et les ressources ; actualiser les paragraphes de statut après réalisation'),
   ('ZIP final','Vérifier le nom L1_MaintiDoc_CHMITI-HADDAOUI-ZERHOUN.zip et ses quatre éléments racine')],[110,W-110]),
  H('Documents de référence'),
  P('Consignes du livrable 1, Pr. Mariam CHERRABI, 29 octobre 2026, pages 1 à 7 : contenu, inventaire, architecture et nommage. Sources techniques des fiches : Microsoft et Mozilla, références dans les PDF et sources_travail.csv. Le rapport ne prétend ni à une maintenance industrielle réelle ni à un prototype RAG déjà évalué.','small'))
 return pages
