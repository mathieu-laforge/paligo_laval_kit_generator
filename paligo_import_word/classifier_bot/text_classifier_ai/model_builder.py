import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from utils.sqlite_db_management import SqLite_DB_manager
import pickle
from joblib import dump, load
from utils.file_access import file_access

class Generate_Calssifier_Model:
    def __init__(self, training_db_path: str, training_table: str):
        self.training_db = training_db_path
        self.training_table = training_table
        
    def fetch_training_data(self):
        connect_db = SqLite_DB_manager(self.training_db, self.training_table)
        data = connect_db.fetch_all_data()
        train_data = []
        for row in data:
            train_data.append(row[2:])
        return train_data    

    # Exemple de données d'entraînement
    """train_data = [
        ("Titre 1", "Ce texte est un exemple de titre."),
        ("Article 1", "Ceci est un exemple de contenu d'article."),
        ("Article 1", "Un autre exemple de contenu d'article."),
        ("Titre 2", "Voici un autre exemple de titre."),
        ("Article 2", "Ceci est un exemple de contenu pour l'article 2."),
        ("Paragraphe", "Ceci est un exemple de paragraphe dans le règlement.")
    ]"""

    def start_training_process(self, model_name: str):
        # Conversion des données en DataFrame
        
        
        df_train = pd.DataFrame(self.fetch_training_data(), columns=["Label", "Text"])
        self.save_dataframe_to_csv(df_train, model_name)
        print("Training Dataframe saved!")
        # Création du pipeline de classification
        
        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer()),  # Extraction des caractéristiques du texte avec TF-IDF
            ("clf", CalibratedClassifierCV(LinearSVC(dual=True)))  # Classificateur basé sur SVM linéaire
        ])

        # Entraînement du modèle
        pipeline.fit(df_train["Text"], df_train["Label"])
        dump(pipeline, f"text_classifier_ai/text_classifier_data/{model_name}.joblib")
        print("Training model saved!")
        
    def save_dataframe_to_csv(self, dataframe: pd.DataFrame, model_name: str):
        dataframe.to_csv(f"text_classifier_ai/text_classifier_data/{model_name}.csv", index=False)