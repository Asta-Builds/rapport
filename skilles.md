# 🎓 Spécifications pour la Rédaction du Rapport de PFE (LaTeX)

Ce document définit les compétences, les standards et la structure requis pour la génération d'un rapport de Projet de Fin d'Études (PFE) de haute qualité académique.

## 🌐 1. Exigences Générales

- **Langue :** Français (Niveau académique, soutenu, précis).
- **Format :** LaTeX (Structure modulaire).
- **Volume cible :** 80+ pages.
- **Ton :** Impartial, technique, et analytique. Utilisation du "nous" de modestie ou de la forme passive.

---

## 🛠️ 2. Compétences Techniques LaTeX

Pour garantir la compilation sans erreur et la maintenabilité, les standards suivants sont imposés :

### A. Modularité (Fichiers Divisés)

Le projet ne doit **jamais** être un fichier unique. La structure doit être :

- `main.tex` : Point d'entrée unique.
- `preamble.tex` : Configuration des packages et commandes personnalisées.
- `/chapters/` : Un fichier `.tex` par chapitre (ex: `ch1_intro.tex`).
- `/frontmatter/` : Page de garde, remerciements, résumé, sommaire.
- `/figures/` : Dossiers organisés par chapitre pour les images.
- `references.bib` : Gestion bibliographique via BibLaTeX.

### B. Maîtrise des Packages

L'IA doit savoir utiliser et configurer :

- `babel [french]` : Pour la typographie française.
- `geometry` : Pour les marges académiques.
- `hyperref` : Pour les liens cliquables et le sommaire.
- `graphicx` et `float` : Pour le placement précis des figures (`[H]`).
- `algorithm2e` ou `listings` : Pour le pseudo-code et le code source.
- `booktabs` : Pour des tableaux professionnels.

---

## 📐 3. Structure Académique du Rapport (Plan Type)

Le contenu doit être généré selon l'ordre logique suivant :

### I. Frontmatter (Éléments Préliminaires)

- **Page de Garde :** Logos, titres, noms des encadrants, année universitaire.
- **Remerciements :** Formulations professionnelles.
- **Résumé / Abstract :** Version française et anglaise avec mots-clés.
- **Table des Matières :** Générée automatiquement.
- **Liste des Figures et Liste des Tableaux.**

### II. Corps du Rapport (Les Chapitres)

1. **Introduction Générale :**
   - Contexte du projet.
   - Problématique (le "Pourquoi").
   - Objectifs visés.
   - Structure du rapport (annonce du plan).
2. **État de l'Art (Étude Théorique) :**
   - Analyse des concepts clés.
   - Comparaison des technologies existantes.
   - Justification du choix technique.
3. **Analyse et Spécifications (Cahier des Charges) :**
   - Besoins fonctionnels.
   - Besoins non-fonctionnels.
   - Diagrammes de cas d'utilisation (UML).
4. **Conception (Architecture) :**
   - Architecture globale du système.
   - Conception détaillée (Diagrammes de classes, Séquences, MCD/MLD).
   - Choix des patterns de conception.
5. **Réalisation et Implémentation :**
   - Environnement de développement.
   - Présentation des modules principaux.
   - Extraits de code critiques et explications.
6. **Tests et Résultats :**
   - Stratégie de test.
   - Scénarios de tests et résultats obtenus.
   - Analyse critique des performances.

### III. Backmatter (Éléments Finaux)

- **Conclusion Générale :** Bilan du travail, objectifs atteints et perspectives d'évolution.
- **Bibliographie :** Citations normalisées (style IEEE ou APA).
- **Annexes :** Documents complémentaires, guides d'installation.

---

## ✍️ 4. Standards de Rédaction et Qualité

### A. Vocabulaire Technique

L'IA doit utiliser les termes appropriés en français :

- *❌ "The system does..." $\rightarrow$ ✅ "Le système permet de..."*
- *❌ "I used a loop..." $\rightarrow$ ✅ "L'implémentation s'appuie sur une structure itérative..."*
- *❌ "Bad performance" $\rightarrow$ ✅ "Une dégradation des performances a été observée..."*

### B. Gestion des Citations

Chaque affirmation technique doit être soutenue par une citation :

- Utilisation systématique de `\cite{label}`.
- Interdiction d'inventer des sources (Hallucinations).

### C. Flux Logique

Chaque chapitre doit se terminer par une **conclusion partielle** et une **transition** vers le chapitre suivant pour assurer la fluidité de la lecture.

---

## 🔄 5. Workflow de Production (Pipeline API)

1. **Planification :** Génération du plan détaillé $\rightarrow$ Validation humaine.
2. **Squelette :** Création de la structure de dossiers et du `main.tex`.
3. **Rédaction Itérative :** Génération chapitre par chapitre $\rightarrow$ Révision $\rightarrow$ Correction.
4. **Compilation :** Test de compilation LaTeX $\rightarrow$ Correction des erreurs de syntaxe.
5. **Finalisation :** Génération de la bibliographie et indexation.

***

### How to use this `skills.md` with your API

When you start your Python script, send this file as the **System Prompt** (or the first message).
