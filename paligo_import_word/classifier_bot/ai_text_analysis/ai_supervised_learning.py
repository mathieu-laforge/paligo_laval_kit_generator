from joblib import dump, load
from utils.file_access import file_access
from sklearn.metrics import accuracy_score

class AI_supervised_learning:
    def __init__ (self, input_text: list, model_name: str):
        self.model_name = model_name
        self.input_text = input_text
        self.model_path = file_access(f"data_sets/{self.model_name}", "joblib")
        self.pipeline = load(self.model_path)
        
    def run_supervised_learning(self):
        for text in self.input_text:
            while True:
            
                # Exemple de prédiction avec un nouveau texte non étiqueté
                predicted_label = self.pipeline.predict([text])
                probabilities = self.pipeline.predict_proba([text])
                
                predicted_prob = max(probabilities[0])
                
                certitude_percentage = round(predicted_prob * 100, 2)
                
                all_classes = self.pipeline.classes_
                print(all_classes)
                # Obtention d'une annotation manuelle pour le texte prédit
                print("Texte traité: " + text)
                print("****************************************************************")
                print("Prédiction: " + predicted_label[0])
                print("Précision de la prédiction: " + certitude_percentage + " %")
                is_prediction_correct = input("La prédiction est-elle exacte '" + predicted_label[0] + "' (o / n): ")
                if is_prediction_correct.lower() != "n":
                    while manual_label not in all_classes:
                        manual_label = input("Quelle est la prédiction souhaitée (titre, chapitre, section, sous-section, article, etc.): ")
                        if manual_label not in all_classes:
                            print("La prédiction n'existe pas dans le modèle actuel. Voulez-vous la créer?")
                            create_new_label = input("Créer (o / n): ")
                            if create_new_label == "o":
                                
                """# Ajout du nouvel exemple annoté à l'ensemble de données d'entraînement
                df_train = df_train.append({"Label": manual_label, "Text": self.input_text}, ignore_index=True)
                
                # Réentraînement du modèle avec les nouvelles données
                self.pipeline.fit(df_train["Text"], df_train["Label"])
                
                # Option pour sortir de la boucle d'apprentissage active
                choice = input("Voulez-vous continuer à annoter de nouveaux exemples ? (oui/non): ")
                if choice.lower() != "oui":
                    break"""