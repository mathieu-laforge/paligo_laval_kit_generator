###Exemple à travailler

import spacy

# Chargement du modèle linguistique de spaCy
nlp = spacy.load("fr_dep_news_trf")

# Fonction pour séparer le texte en phrases
def split_sentences(text):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    return sentences

# Exemple de texte
text = "Ceci est une phrase. Et voici une autre phrase. Une troisième phrase est présente."

# Séparation du texte en phrases
sentences = split_sentences(text)

# Affichage des phrases
for sentence in sentences:
    print(sentence)