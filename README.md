# MaintiDoc

Projet du module IA générative multimodale - EMSI 2026.

## Équipe

- Mehdi Chmiti
- Ismail Haddaoui
- Ayman Zerhoun

## Objectif

Aider les techniciens à retrouver une procédure, comprendre un problème et préparer un ticket à partir de documents et d’images. Les réponses doivent citer leurs sources et la création d’un ticket nécessite l’accord du technicien.

Deux familles sont étudiées : les postes Windows et les périphériques informatiques.

## Livrable 1

- `L1_MaintiDoc_CHMITI-HADDAOUI-ZERHOUN_Rapport.pdf` : cadrage, architecture, flux de données, risques et planning, en 15 pages, dont une page de garde.
- `L1_MaintiDoc_CHMITI-HADDAOUI-ZERHOUN_LienGitHub.txt` : lien du dépôt.
- `README.md` : présentation du projet.
- `L1_MaintiDoc_CHMITI-HADDAOUI-ZERHOUN_Corpus/` : documents, inventaire et prompts utilisés.

Le corpus comprend 36 documents : procédures, manuels, codes locaux et fiche de sécurité. Il contient aussi deux scans synthétiques pour l’OCR, deux versions contradictoires et un document piégé pour les tests.

## Organisation du dépôt

```text
maintidoc/
├── README.md
├── .gitignore
├── corpus/
│   ├── inventaire.csv
│   ├── prompts_corpus.md
│   ├── sources_travail.csv
│   ├── documents/
│   │   ├── famille_1/
│   │   └── famille_2/
│   └── images/
├── docs/
│   ├── diagrammes/
│   └── L1_MaintiDoc_CHMITI-HADDAOUI-ZERHOUN_Rapport.pdf
└── scripts/
```

L’inventaire décrit chaque document, sa provenance, sa version et ses groupes d’accès. Le suivi des relectures se trouve dans `corpus/STATUT_VALIDATION.md` et dans la colonne `verifie_par` de l’inventaire.

Dépôt : https://github.com/mccrking/maintidoc-l1-chmiti-haddaoui-zerhoun
