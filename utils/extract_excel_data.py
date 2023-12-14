import pandas
from utils.file_access import file_access

def extract_excel_data(file_path):
    
    json_data = pandas.read_excel(file_path).to_json()
    #print(json_data)
    return json_data



if __name__ == "__main__":
    extract_excel_data("tableau_annexe_b.xlsx")