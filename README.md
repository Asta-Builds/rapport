# Rapport PFE — ProvisionHub (IAM Middleware)

Rapport de Projet de Fin d'Études sur **ProvisionHub**, un middleware IAM d'orchestration de provisioning pour l'entreprise OCP.

## Structure du projet

```
├── latex/              # Sources LaTeX du rapport
│   ├── main.tex        # Point d'entrée
│   ├── preamble.tex    # Packages et configuration
│   ├── chapters/       # 6 chapitres du rapport
│   │   ├── chapter1.tex  # Introduction
│   │   ├── chapter2.tex  # Contexte et Problématique
│   │   ├── chapter3.tex  # Analyse et Conception
│   │   ├── chapter4.tex  # Réalisation et Implémentation
│   │   ├── chapter5.tex  # Tests et Validation
│   │   └── chapter6.tex  # Conclusion et Perspectives
│   └── frontmatter/    # Préliminaires (dédicace, remerciements, résumé, etc.)
├── pfe_report/         # Copie de travail générée par l'outil Local Overleaf
├── build/              # Sorties de compilation (PDF, logs, fichiers aux)
├── local_overleaf.py   # App Streamlit pour éditer et compiler le rapport
├── compile_now.py      # Script de compilation simplifié
├── fix_pdf.py          # Script de compilation avec nettoyage préalable
├── abdelilahdahoupfe.md # Documentation technique de ProvisionHub
├── skilles.md          # Spécifications et guide de rédaction académique
└── test.tex / test.pdf # Tests LaTeX divers
```

## Prérequis

- **MikTeX** ou **TeX Live** (moteur `pdflatex`)
- **Python 3.10+**
- Paquets Python : `streamlit`

```bash
pip install streamlit
```

## Compiler le rapport

### Option 1 — Script rapide
```bash
python compile_now.py
```

### Option 2 — Avec nettoyage préalable
```bash
python fix_pdf.py
```

### Option 3 — Application Local Overleaf (éditeur + visualisation)
```bash
streamlit run local_overleaf.py
```
Ouvre une interface web avec éditeur LaTeX et aperçu PDF.

### Option 4 — Compilation manuelle
```bash
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex   # deuxième passe pour les références
```

## État d'avancement

| Chapitre | Contenu |
|----------|---------|
| Ch1 — Introduction | À rédiger |
| Ch2 — Contexte et Problématique | Rédigé |
| Ch3 — Analyse et Conception | À rédiger |
| Ch4 — Réalisation et Implémentation | À rédiger |
| Ch5 — Tests et Validation | À rédiger |
| Ch6 — Conclusion et Perspectives | À rédiger |

Le rapport est rédigé en **LaTeX modulaire**, en français, format académique (report, 12pt, A4).
