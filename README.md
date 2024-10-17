# Analyse de Correspondance CV vs Offre d'Emploi

Cette application Flask permet de comparer un CV en PDF avec une offre d'emploi en texte. Elle analyse la correspondance entre les compétences mentionnées dans le CV et celles requises dans l'offre, et renvoie un score de correspondance ainsi qu'une liste des compétences correspondantes et manquantes.

## Fonctionnalités

- **Téléchargement de CV en format PDF** : L'application extrait automatiquement le texte du fichier PDF soumis.
- **Saisie de l'offre d'emploi** : Vous pouvez copier-coller les parties importantes de l'offre, telles que les missions principales, l'environnement technique et le profil recherché.
- **Analyse de la correspondance** : Utilise le cosinus de similarité pour calculer un score de correspondance basé sur les compétences présentes dans le CV et l'offre d'emploi.
- **Retour de compétences manquantes** : L'application vous indique quelles compétences sont manquantes dans le CV et d'où elles proviennent dans l'offre d'emploi.
- **Affichage des résultats** : Les résultats incluent un score de correspondance, une liste de compétences correspondantes, et des conseils pour améliorer le CV.

## Structure du projet

- `app.py` : Contient la logique de l'application Flask, y compris les fonctions d'extraction de texte du PDF et d'analyse de similarité entre le CV et l'offre d'emploi.
- `templates/index.html` : Formulaire pour télécharger le CV et saisir l'offre d'emploi.
- `templates/result.html` : Page pour afficher les résultats de l'analyse, y compris le score de correspondance et les compétences.

## Technologies utilisées

- **Flask** : Framework web Python léger pour créer l'application.
- **PyPDF2** : Bibliothèque Python pour lire et extraire le texte des fichiers PDF.
- **spaCy** : Modèle linguistique utilisé pour le traitement du langage naturel (français).
- **scikit-learn** : Utilisé pour la vectorisation des textes et le calcul du cosinus de similarité.
- **Bootstrap** : Framework CSS utilisé pour le style des pages web.

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/tonpseudo/analyse-cv-vs-offre.git
2. Accédez au répertoire du projet :
   ```bash
   cd analyse-cv-vs-offre

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt

4. Lancez l'application :
   ```bash
   python app.py

5. Ouvrez votre navigateur et accédez à l'adresse suivante :
   ```bash
   http://127.0.0.1:5000/
