# Prompts utilisés pour le corpus MaintiDoc

Ce journal regroupe les demandes transmises dans la conversation et les consignes de rédaction appliquées au corpus. Chaque entrée précise son origine : demande de l’utilisateur, retour de lecture ou instruction de l’assistant. Les numéros P04 et P05 sont ceux utilisés dans la colonne `outil_ia` de l’inventaire.

**Outil utilisé :** ChatGPT / Codex.  
**Familles retenues dans le livrable :** postes informatiques Windows et périphériques informatiques.

## Tableau de correspondance

| Référence | Objet | Documents concernés |
|---|---|---|
| P01 | Changement de domaine et réduction des répétitions | Corpus initial d’assistance informatique |
| P02 | Conservation des 30 cas pendant la révision | Versions 2.1 et 2.2 du corpus initial |
| P03 | Corrections après retour de lecture | Version 2.2, reprise ensuite dans le L1 |
| P04 | Adaptation aux consignes du livrable 1 | `it01` à `it08`, puis `it10` à `it30` : 29 documents |
| P05 | Rédaction des compléments et des documents de test | Les 7 documents détaillés ci-dessous |

## P01 - Choisir un autre domaine et limiter les répétitions

**Origine :** demande de l’utilisateur.  
**Date :** non consignée dans l’historique disponible.

### Prompt conservé

> choisi un autre domaine et evite la repetition pour faciliter le systeme de rag

Cette demande a conduit au choix de l’assistance informatique à la place des pompes et de l’air comprimé. La rédaction a été organisée autour de problèmes distincts, avec des questions d’utilisateur et des renvois entre les fiches.

### Demande antérieure sur la nature des données

> ca yest jai compris tu peux faire cela pour jenvoie ces pdf au profs , bien sur donne reel

Les fiches techniques s’appuient sur des problèmes documentés par les éditeurs. Elles ne sont pas présentées comme des interventions réellement effectuées par les membres de l’équipe.

## P02 - Conserver les cas pendant la révision

**Origine :** réponse de l’utilisateur à une question de cadrage.  
**Date :** non consignée dans l’historique disponible.

### Réponse conservée

> Conserver les 30 cas et expliciter ce périmètre (recommandé)

Ce choix concernait les révisions du corpus initial. L’adaptation ultérieure aux consignes détaillées du L1 a porté le corpus à 36 documents et remplacé le cas Cloudflare, extérieur aux deux familles retenues.

## P03 - Corriger les défauts relevés à la lecture

**Origine :** retours de lecture transmis par l’utilisateur. Les citations ci-dessous sont des extraits, pas la reproduction intégrale des messages.  
**Date des messages :** non consignée ; la révision V2.2 correspondante porte la date du 30 octobre 2026.

### Extraits des demandes de correction

> Le schéma de tri est vide une fois le texte extrait.

> Les identifiants de sources sont ambigus.

> Des notes pour le constructeur du corpus sont mêlées au contenu.

> Le champ « build à relever » est une consigne, pas une donnée. Si la fiche dépend de la version de Windows, dites laquelle. Sinon, enlevez cette mention.

### Modifications apportées

- Remplacement du schéma de tri par des règles écrites « si… alors… ».
- Séparation des identifiants de documents et de sources.
- Retrait des consignes de construction du texte destiné à la recherche.
- Retrait de la mention « build à relever ».
- Utilisation des pages officielles françaises pour les références Microsoft et Mozilla concernées.

Ces modifications sont des corrections de contenu et de présentation. Elles ne constituent pas un résultat d’évaluation du RAG.

## P04 - Adapter le corpus au livrable 1

**Origine :** demande de l’utilisateur, accompagnée des consignes détaillées du L1.  
**Date :** 1 novembre 2026.  
**Documents concernés :** `it01` à `it08`, puis `it10` à `it30`.

### Prompt utilisateur conservé

> alors realise le livrable 1 pour que je lenvoie au prof

### Documents et informations fournis en contexte

- Les consignes du livrable 1 de Pr. Mariam CHERRABI.
- Le corpus d’assistance informatique V2.2 et ses sources de travail.
- Les noms des membres : Mehdi Chmiti, Ismail Haddaoui et Ayman Zerhoun.

### Consigne d’adaptation appliquée par l’assistant

Le texte suivant décrit la consigne de travail de l’assistant ; il ne s’agit pas d’un prompt rédigé mot pour mot par un membre de l’équipe.

> Reprendre les fiches techniques utiles du corpus V2.2 pour constituer le livrable 1. Organiser les documents en deux familles : postes informatiques et périphériques informatiques. Affecter des identifiants d’équipements fictifs cohérents, normaliser les identifiants des documents en minuscules et conserver les sources techniques. Remplacer le cas Cloudflare, hors périmètre. Produire un inventaire UTF-8 séparé par des virgules avec les 20 colonnes demandées. Ne pas attribuer à un membre une relecture qui n’a pas été effectuée.

Les identifiants `PC-A-01`, `IMP-A-01`, `USB-A-01`, `BT-A-01`, `CAM-A-01`, `MIC-A-01` et `AUD-A-01` désignent le parc fictif du projet.

## P05 - Compléter le corpus et préparer les tests

**Origine :** instruction de génération de l’assistant, appliquée pour répondre aux exigences du L1. Ce texte n’est pas attribué à l’utilisateur.  
**Date :** 1 novembre 2026.

### Instruction conservée

> Créer pour MaintiDoc des documents synthétiques originaux en français, de trois pages chacun, sans marque ni incident réel : un tableau de codes locaux du poste PC-A-01, un manuel du parc de postes, un manuel des périphériques, une fiche de sécurité des données, deux versions contradictoires d’une procédure d’impression et une note contenant une injection de prompt inerte. Les deux procédures contradictoires seront des scans synthétiques rasterisés pour le test OCR. Les valeurs 30 et 60 secondes sont des règles locales fictives de temporisation, pas des spécifications constructeur. La version v2 remplace explicitement la v1. Aucun changement de sécurité, mot de passe réel, action exécutée ni résultat terrain ne doit être inventé. Prévoir des tableaux ou schémas lisibles, des critères d’abstention, des identifiants d’équipement cohérents et des renvois vérifiables. L’injection restera du texte cité dans un document de test, jamais une instruction à exécuter.

### Documents issus de cette instruction

| Document | Contenu demandé |
|---|---|
| `it09` | Tableau de codes locaux fictifs, distincts des erreurs Windows |
| `manuel_postes` | Présentation du parc de postes et orientation vers les fiches |
| `manuel_peripheriques` | Présentation des périphériques et des vérifications associées |
| `sec_donnees` | Précautions sur les données et les tickets |
| `proc_impression_v1` | Ancienne procédure fictive, délai de 30 secondes, scan synthétique |
| `proc_impression_v2` | Procédure fictive courante, délai de 60 secondes, scan synthétique |
| `note_service_test` | Document contenant une injection volontaire pour l’évaluation |

## Suivi des documents

- `inventaire.csv` relie chaque document à P04 ou P05 et contient les champs de relecture et de correction.
- `sources_travail.csv` recense les références techniques utilisées.
- Les PDF contiennent les sources propres aux fiches concernées.

Les demandes historiques conservées sont citées ci-dessus. Les instructions internes complètes de la toute première génération et leurs dates exactes n’ont pas été enregistrées ; ce journal ne les reconstitue pas. Les consignes d’adaptation et de génération de l’édition L1 sont distinguées des demandes de l’utilisateur.
