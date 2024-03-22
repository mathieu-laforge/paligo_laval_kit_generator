from joblib import dump, load
from utils.file_access import file_access
import pandas as pd
import math

class AI_supervised_learning:
    def __init__ (self, input_text: list, model_name_path: str):
        """_summary_

        Args:
            input_text (list): the text to classify
            model_name_path (str): the model path without the extension. The program expects a csv and joblib files.
        """        
        self.model_name = model_name_path
        self.input_text = input_text
        
    def save_dataframe_to_csv(self, dataframe: pd.DataFrame, model_name: str):
        dataframe.to_csv(f"{model_name}.csv", index=False)
       
    def run_supervised_learning(self):
        
        
        for text in self.input_text:
            model_path = file_access(f"{self.model_name}", "joblib")
            pipeline = load(model_path)
            data_frame = pd.read_csv(f"{self.model_name}.csv")
            print("Le model utilisé contient: " + str(math.floor(data_frame.size/2)) + " elements traités")
            # Exemple de prédiction avec un nouveau texte non étiqueté
            predicted_label = pipeline.predict([text])
            probabilities = pipeline.predict_proba([text])
            
            predicted_prob = max(probabilities[0])
            
            certitude_percentage = round(predicted_prob * 100, 2)
            
            all_classes = pipeline.classes_
            #print(all_classes)
            # Obtention d'une annotation manuelle pour le texte prédit
            print("____________________________________________________________________________________________________________________")
            print(f"""
                    Texte traité:
                        {text}
                  
                    Prédiction:
                        {predicted_label[0]}
                    
                    Précision:
                        {str(certitude_percentage)} %
                  """)
            is_prediction_correct = input(f"""
                La prédiction est-elle exacte {predicted_label[0]} (o / n): """)
            if is_prediction_correct.lower() == "n":
                manual_label = ""
                while manual_label not in all_classes:
                    manual_label = input("Quelle est la prédiction souhaitée (titre, chapitre, section, sous-section, article, etc.): ")
                    if manual_label not in all_classes:
                        print("La prédiction n'existe pas dans le modèle actuel. Voulez-vous la créer?")
                        create_new_label = input("Créer (o / n): ")
                        if create_new_label == "o":
                            new_line = {"Text": text, "Label": manual_label }
                            new_df_train = pd.concat([data_frame, pd.DataFrame([new_line])], ignore_index=True)
                            self.save_dataframe_to_csv(new_df_train, self.model_name)
                            pipeline.fit(new_df_train["Text"].values.astype('U'), new_df_train["Label"].values.astype('U'))
                            dump(pipeline, f"{self.model_name}.joblib")
                            print("data added to pipeline")
                            break
                        if create_new_label != "o":
                            break
                    else:
                        new_line = {"Text": text, "Label": manual_label }
                        new_df_train = pd.concat([data_frame, pd.DataFrame([new_line])], ignore_index=True)
                        self.save_dataframe_to_csv(new_df_train, self.model_name)
                        pipeline.fit(new_df_train["Text"].values.astype('U'), new_df_train["Label"].values.astype('U'))
                        dump(pipeline, f"{self.model_name}.joblib")
                        
                        print("data added to pipeline")
            else:
                new_line = {"Text": text, "Label": predicted_label[0] }
            new_df_train = pd.concat([data_frame, pd.DataFrame([new_line])], ignore_index=True)
            self.save_dataframe_to_csv(new_df_train, self.model_name)
            pipeline.fit(new_df_train["Text"].values.astype('U'), new_df_train["Label"].values.astype('U'))
            dump(pipeline, f"{self.model_name}.joblib")
            print("data added to pipeline")
            """# Ajout du nouvel exemple annoté à l'ensemble de données d'entraînement
            df_train = df_train.append({"Label": manual_label, "Text": self.input_text}, ignore_index=True)
            
            # Réentraînement du modèle avec les nouvelles données
            self.pipeline.fit(df_train["Text"], df_train["Label"])
            
            # Option pour sortir de la boucle d'apprentissage active
            choice = input("Voulez-vous continuer à annoter de nouveaux exemples ? (oui/non): ")
            if choice.lower() != "oui":
                break"""
        return new_line