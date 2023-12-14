import json

def save_data_to_json(data, fileOutput: str):
    """Création d'un fichier JSON
    
    Permet de sauvegarder un fichier JSON à partir des réponses de requêtes ou toutes autres
    informations sous forme de string.

    Args:
        data (str): L'information à sauvegarder
        fileOutput (str): le nom du fichier .json ex: fichier_123.json
    """    
    with open(f"{fileOutput}", "w+", encoding="utf8") as f:
        f.write(json.dumps(data, ensure_ascii=False))
    f.close()

def json_dump(data, fileOutput):
    with open(f"{fileOutput}", "w+") as f:
        f.write(json.dumps(data, ensure_ascii=True))
    f.close()

def read_data_from_json(fileInput: str):
    """Lecture de fichier JSON

    Args:
        fileInput (str): le nom du fichier .json ex: fichier_123.json

    Returns:
        data (str): Le contenu du dossier en JSON strings
    """    
    f = open(fileInput)
    data = json.load(f)
    f.close()
    return data