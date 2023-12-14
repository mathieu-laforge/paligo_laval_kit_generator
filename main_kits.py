from generate_pdf_kits.generate_kits import Generate_kits_publications
from generate_pdf_kits.pull_publications import Extractions_kits, Extraction_annexe_B
from generate_pdf_kits.paligo_publication_watcher import Paligo_publication_watcher

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class init_ui_text:
      def succes(self):
            print(f"{bcolors.OKGREEN}La fonction s'est terminées sans échec{bcolors.ENDC}")
            print("")
      
      def fail(self, e):
            print(f"{bcolors.FAIL}Erreur dans la fonction{bcolors.ENDC}")
            print("")
            print(e)
            print("")
      
      def main_program(self):
            print(f"{bcolors.HEADER}CONSOLE de Gestion de PALIGO{bcolors.ENDC}")
            print("")
            print(f"{bcolors.BOLD}_________________Fonctions manuelles_________________{bcolors.ENDC}")
            print("")
            print("")
            print("")

      def menu_principal(self):
            print(f"{bcolors.BOLD}Choisisser parmis les options suivantes: ")            
            print("")
            print(f"{bcolors.BOLD}1. {bcolors.ENDC}MISE À JOUR DE LA BASE DE DONNÉES")
            print("")
            print(f"{bcolors.BOLD}2. {bcolors.ENDC}CRÉATION ET MISE À JOUR DES PUBLICATIONS DES FICHES")
            print("        Utilise la base de données existantes, Appelle les tags de paligo selon la liste dans la config.py")
            print("        Appelle les tags de paligo selon la liste dans la config.py")
            print("        Crée, valide et met à jour les publications des fiches selon les tags")
            print("")
            print(f"{bcolors.BOLD}3. {bcolors.ENDC}PUBLICATION ET EXTRACTION DES KITS")
            print("")
            #print(f"{bcolors.BOLD}3. {bcolors.ENDC}Else")
            #print("")
            #print("")
      
      def generate_fiches(self):
            
            print(f"{bcolors.HEADER}GÉNÉRATION DES FICHES{bcolors.ENDC}")
            print("")
            print("lancement de la génération")
            print("")
            

      
      def extraction_kits(self):
            print(f"{bcolors.HEADER}GÉNÉRATION DES KITS{bcolors.ENDC}")
            print("")
            print("Permet de tirer les publications de la liste des kits et de générer des documents pdf.")
            print("")
            print("Choisir parmis les options suivantes: ")
            print("")
            print(f"{bcolors.BOLD}1. {bcolors.ENDC}FICHES ET EXTRAITS - Tirer les publications de la liste des kits.")
            print("")
            print(f"{bcolors.BOLD}2. {bcolors.ENDC}GRILLES D'EXCEPTION - créer un PDF par grille d'Exception.")
            print("")
            print(f"{bcolors.BOLD}3. {bcolors.ENDC}DOCUMENTS SPÉCIFIQUES - Permet de tirer la publication d'un ou plusieurs documents")
            print("")
            print(f"{bcolors.BOLD}X {bcolors.ENDC}Terminer et quitter")
            print("")

      
      def NOUVELLE_FONCTION(self):
            
            print("Définir les exceptions d'importation. Écrire les mots ou groupe de mots qui doivent être retiré de l'importatation.")
            print("")
            print("Choisir parmis les options suivantes: ")
            print("")
            print(f"{bcolors.BOLD}0. {bcolors.ENDC}Terminer")
            print("")
            print(f"{bcolors.BOLD}1. {bcolors.ENDC}Ajouter un élément")
            print("")
            print(f"{bcolors.BOLD}2. {bcolors.ENDC}Supprimer les exceptions")
            print("")
            print(f"{bcolors.BOLD}2. {bcolors.ENDC}Supprimer les exceptions")
            print("")








class Docubo_program:
      def __init__(self):
            """Main program to handle pdf kits generation and extraction from paligo.
            """            
            self.ui = init_ui_text()
            self.choice = None
            while self.choice != "x":

                  self.ui.main_program()   
            
                  self.menu_principal()
                  if self.choice.lower() == "x":
                        break

      def menu_principal(self):
            self.ui.menu_principal()      
                  
            self.choice = input("Entrer le numéro de l'option (1, 2, 3, etc.): ")
            while self.choice != "x":
                  if self.choice == "1":
                        try:
                              #Fiches et extraits
                              update_db = Paligo_publication_watcher()
                              update_db.run_bypass_pub_db()
                        except Exception as e:
                              self.ui.fail(e)      
                              self.menu_principal()
                        self.ui.succes()     
                        self.menu_principal()
                  
                  
                  if self.choice == "2":
                        try:
                              
                              self.ui.generate_fiches()
                              gen_k = Generate_kits_publications()
                              gen_k.run_kits_generator()
                              
                        except Exception as e:
                              print(e)
                        self.ui.succes()
                        self.ui.menu_principal()

                  if self.choice == "3":
                        self.extraction_kits()

                  """if self.choice == "3":      
                        pass"""
                  if self.choice.lower() == "x":
                        break      
                               
      def extraction_kits(self):
            self.ui.extraction_kits()
            self.choice = input("Entrer le numéro de l'option (1, 2, 3, etc.): ")
            while self.choice != "x":
                  if self.choice == "1":
                        try:
                              #Fiches et extraits
                              ext_k = Extractions_kits()
                              ext_k.run_kits_extraction()
                        except Exception as e:
                              self.ui.fail(e)      
                              self.menu_principal()
                        self.ui.succes()     
                        self.menu_principal()

                  if self.choice == "2":
                        try:
                              ext_annexe = Extraction_annexe_B()
                              ext_annexe.run_extraction_annexe_b()
                        except Exception as e:
                              self.ui.fail(e)      
                              self.menu_principal()
                        print(f"Total exceptions grids: {ext_annexe.exception_counter_total}")
                        self.ui.succes()     
                        self.menu_principal()

                  if self.choice == "3":      
                        try:
                              user_input = input("Give a single or multiple publications names (\", \" separated): ")
                              user_list = []
                              user_split = user_input.split(", ")
                              for i in user_split:
                                    user_list.append(i.strip()) 
                              ext_k = Extractions_kits(True, user_list)
                              ext_k.run_kits_extraction()
                        except Exception as e:
                              self.ui.fail(e)      
                              self.menu_principal()
                        self.ui.succes()     
                        self.menu_principal()

                  
                  """if self.choice == "4":      
                        pass"""
                  
                  if self.choice.lower() == "x":
                        break
          
            

if __name__ == "__main__":
    Docubo_program()
