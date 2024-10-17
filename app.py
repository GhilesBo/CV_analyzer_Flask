from flask import Flask, render_template, request
import PyPDF2
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Charger le modèle linguistique français
nlp = spacy.load("fr_core_news_sm")

# Fonction pour extraire le texte d'un fichier PDF
def extraire_texte_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    texte = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        texte += page.extract_text()
    return texte

# Fonction pour trouver l'origine des compétences dans le texte de l'offre d'emploi
def trouver_origine_competence(competence, job_description):
    phrases = [sent.text for sent in nlp(job_description).sents if competence in sent.text.lower()]
    if phrases:
        return phrases[0]  # Retourner la première phrase contenant la compétence
    return ""

# Fonction pour analyser la correspondance entre le CV et l'offre d'emploi
def analyse_cv_contre_offre(cv_text, job_description):
    # Prétraiter les textes
    cv_doc = nlp(cv_text)
    job_description_doc = nlp(job_description)

    # Extraire les tokens
    cv_tokens = [token.lemma_.lower() for token in cv_doc if not token.is_stop and not token.is_punct]
    job_description_tokens = [token.lemma_.lower() for token in job_description_doc if not token.is_stop and not token.is_punct]

    # Convertir en texte prêt pour le vectoriseur
    cv_clean = ' '.join(cv_tokens)
    job_description_clean = ' '.join(job_description_tokens)

    # Vectoriser les textes et calculer la similarité
    vectorizer = CountVectorizer().fit_transform([cv_clean, job_description_clean])
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors)

    # Calculer le pourcentage de correspondance
    match_percentage = cosine_sim[0][1] * 100

    # Extraire les compétences manquantes et leur origine
    cv_set = set(cv_tokens)
    job_set = set(job_description_tokens)
    competences_manquantes = job_set - cv_set

    competences_info = [
        {'competence': competence, 'origine': trouver_origine_competence(competence, job_description)}
        for competence in competences_manquantes
    ]

    # Extraire les compétences qui ont bien matché
    competences_match = cv_set.intersection(job_set)

    resultats = {
        'score': round(match_percentage, 2),
        'competences_manquantes': competences_info,
        'competences_match': list(competences_match)
    }
    return resultats

# Route pour afficher la page d'accueil et télécharger les fichiers
@app.route('/')
def index():
    return render_template('index.html')

# Route pour traiter le formulaire de soumission
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Récupérer le fichier PDF (CV) téléchargé et l'offre d'emploi
        cv_file = request.files['cv']
        job_description = request.form['job_description']

        # Extraire le texte du CV à partir du fichier PDF
        cv_text = extraire_texte_pdf(cv_file)

        # Analyser la correspondance entre le CV et l'offre d'emploi
        resultats = analyse_cv_contre_offre(cv_text, job_description)

        # Afficher le résultat sur la même page
        return render_template('result.html', 
                               score=resultats['score'], 
                               competences_manquantes=resultats['competences_manquantes'], 
                               competences_match=resultats['competences_match'])

if __name__ == '__main__':
    app.run(debug=True)
