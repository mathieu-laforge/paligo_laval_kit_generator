from joblib import dump, load
from utils.file_access import file_access
from sklearn.metrics import accuracy_score

class Run_structure_classification_AI:
    def __init__(self, model_name: str, input_text: str):
        self.model_name = model_name
        self.input_text = input_text
        self.model_path = file_access(f"data_sets/{self.model_name}.joblib")
        pipeline = load(self.model_path)
        
        predicted_label = pipeline.predict([self.input_text])[0]
        accuracy = accuracy_score(self.pipeline.predict([self.input_text]))
        print(accuracy)
        print("Predicted Label:", predicted_label)