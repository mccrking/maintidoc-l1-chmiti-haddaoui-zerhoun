# Prompts du corpus MaintiDoc

Domaine : maintenance des postes informatiques et des périphériques informatiques.

Ce journal distingue les demandes exactes de l’utilisateur des consignes reformulées. Les dates exactes de P01 à P03 ne sont pas consignées. La création des compléments du L1 date du 1er novembre 2026.

## P01 — Choisir le domaine

Demande exacte de l’utilisateur :

> choisi un autre domaine et evite la repetition pour faciliter le systeme de rag

Cette demande a conduit au choix de l’assistance informatique, avec des problèmes distincts pour limiter les répétitions.

## P02 — Conserver les 30 cas

Réponse exacte de l’utilisateur :

> Conserver les 30 cas et expliciter ce périmètre (recommandé)

Ce choix concernait la révision du corpus initial. L’adaptation aux consignes du L1 a ensuite porté le corpus à 36 documents.

## P03 — Améliorer les fiches

Synthèse des retours de l’utilisateur, reformulée ; ce texte n’est pas une citation exacte :

> Remplacer les schémas peu exploitables par des règles « si… alors… ». Distinguer les identifiants des fiches et ceux des sources. Retirer les notes destinées au constructeur du corpus. Préciser le périmètre technique, supprimer la mention « build à relever » et utiliser les références officielles françaises lorsqu’elles existent.

## P05 — Créer les sept documents complémentaires

Date : 1er novembre 2026.

Consigne de génération appliquée, reformulée ; ce texte n’est pas une citation exacte d’une demande de l’utilisateur :

> Créer sept documents synthétiques originaux en français, de trois pages chacun : un tableau de codes locaux fictifs, un manuel des postes, un manuel des périphériques, une fiche de sécurité des données, deux versions contradictoires d’une procédure d’impression et une note contenant une injection de prompt destinée aux tests.
>
> Transformer les deux procédures d’impression en scans synthétiques pour préparer les tests OCR. Indiquer que les délais de 30 et 60 secondes sont des règles locales fictives et que la version 2 remplace la version 1. Ajouter des tableaux ou schémas lisibles. Ne pas inventer d’incident réel, de résultat terrain ou de spécification constructeur. L’injection doit rester du contenu documentaire de test, sans être exécutée.

Documents concernés :

- `it09`
- `manuel_postes`
- `manuel_peripheriques`
- `sec_donnees`
- `proc_impression_v1`
- `proc_impression_v2`
- `note_service_test`
