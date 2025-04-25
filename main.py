from generate_pdf_kits.generate_kits import Generate_kits_publications
from paligo_publications.pull_publications import Extractions_kits, Extraction_annexe_B
from paligo_publications.paligo_publication_watcher import Paligo_publication_watcher
from paligo_publication_schema.publication_schema_builder import Publication_schema_builder
from paligo_index_automation.automate_glossary import Automate_glossary
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
            print(f"{bcolors.BOLD}1. {bcolors.ENDC}{bcolors.OKGREEN}MISE À JOUR DE LA BASE DE DONNÉES{bcolors.ENDC}")
            print(f"        {bcolors.WARNING}   IMPORTANT les fonctions 2 et 3 ont besoin d'une BD à jour{bcolors.ENDC} ")
            print("        Créer une BD sqlite3 avec les publications CDU et autres Reg")
            print("")
            print(f"{bcolors.BOLD}2. {bcolors.ENDC}{bcolors.OKGREEN}MISE À JOUR DES PUBLICATIONS DES FICHES{bcolors.ENDC}")
            print("")
            print(f"        {bcolors.WARNING}   ICI on explique comment faire des kits... Mais la mise à jour Automatisée{bcolors.ENDC} ")
            print(f"        {bcolors.WARNING}   c'est juste pour les fiches d'article sans titre, chapitre, etc.{bcolors.ENDC} ")
            print("        Il faut s'assurer d'avoir créer vos publications à partir d'un chapitre ou une section d'un règlement.")
            print("        Il faut s'assurer de créer un tag au bon endroit pour créer une fiche d'article")
            print("        La publication doit avoit des publish settings sauvgardés pour une sortie en pdf plus tard  ")
            print("        ET CHAQUE PUBLICATION À FAIRE doit être inscrite dans le tableau du topic Liste de kits PDF. ")
            print("        Le publication name doit être identique à celui que vous avez donner en sauvegardant les publish settings")
            print("")
            
            print(f"{bcolors.BOLD}3. {bcolors.ENDC}{bcolors.OKGREEN}PUBLIER ET EXTRAIRE (PDF){bcolors.ENDC}")
            print("")
            print("        Extraire toutes les publications selon la liste de kits PDF dans Paligo")
            print("        Les documents seront sauvegardés dans un folder nommé production.")
            print("        C'est la création du dossier Bundle de règlements comptoir.")
            print("")
            
            print(f"{bcolors.WARNING}Pour changer le token d'accès à Paligo il faut aller dans Config.py{bcolors.ENDC}")
            
            
            
            
            """print(f"{bcolors.BOLD}4. {bcolors.ENDC}{bcolors.OKGREEN}GENERATION DES SCHEMAS et LISTE DES LIENS (MIRE MOBILE){bcolors.ENDC}")
            print("        Créer les schemas de publication à partir des publications extraites de Paligo.")
            print("        Créer un ficher excel des liens vers le règlement")
            print("")
            
            print(f"{bcolors.BOLD}5. {bcolors.ENDC}{bcolors.OKGREEN}GLOSSAIRE DU CDU{bcolors.ENDC}")
            print("        Automatisation du glossaire pour le CDU (seulement pour l'instant)")
            
            print("")
            
            print(f"{bcolors.BOLD}X {bcolors.ENDC}{bcolors.OKGREEN}Terminer et quitter{bcolors.ENDC}")
            print("")
            #print(f"{bcolors.BOLD}3. {bcolors.ENDC}Else")
            #print("")
            #print("")"""
      
      def generate_fiches(self):
            
            print(f"{bcolors.HEADER}GÉNÉRATION DES FICHES{bcolors.ENDC}")
            print("")
            print(f"{bcolors.WARNING}lancement de la génération{bcolors.ENDC}")
            print("")
            

      
      def extraction_kits(self):
            print(f"{bcolors.HEADER}GÉNÉRATION DES KITS{bcolors.ENDC}")
            print("")
            print("Permet de tirer les publications de la liste des kits et de générer des documents pdf.")
            print("")
            print("Choisir parmis les options suivantes: ")
            print("")
            print(f"{bcolors.BOLD}1. {bcolors.ENDC}Extraction et convertion PDF des Extraits, Fiches et Grilles d'exceptions")
            print("")
            """print(f"{bcolors.BOLD}2. {bcolors.ENDC}GRILLES D'EXCEPTION - Les grilles c'est long! En as-tu vraiment besoin??")
            print("")"""
            """print(f"{bcolors.BOLD}3. {bcolors.ENDC}COMBINAISON DE 1. ET 2.")
            print("")
            print(f"{bcolors.BOLD}4. {bcolors.ENDC}DOCUMENTS SPÉCIFIQUES - Permet de tirer la publication d'un ou plusieurs documents")
            print("")"""
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

      def schema_generator_ui(self):
            print(f"{bcolors.HEADER}Lancement... Schema Generator{bcolors.ENDC}")
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
            self.choice = None      
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
                        self.menu_principal()

                  if self.choice == "3":
                        try:
                              
                              ext_k = Extractions_kits()
                              ext_k.run_kits_extraction()
                              ext_annexe = Extraction_annexe_B()
                              ext_annexe.run_extraction_annexe_b()
                        except Exception as e:
                              self.ui.fail(e)      
                              self.menu_principal()
                        self.ui.succes()     
                        self.menu_principal()

                  if self.choice == "4":
                        self.schema_generator()
                        self.menu_principal()
                  
                  if self.choice == "5":            
                        try:
                              #Fiches et extraits
                              atm = Automate_glossary("cdu_publication", 10381520)
                              atm.find_matching_words()
                        except Exception as e:
                              self.ui.fail(e)      
                              self.menu_principal()
                        self.ui.succes()     
                        self.menu_principal()
                        
                  
                  
                  if self.choice.lower() == "x":
                        self.menu_principal()    
                               
      """def extraction_kits(self):
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
                              ext_annexe = Extraction_annexe_B()
                              ext_annexe.run_extraction_annexe_b()
                              ext_k = Extractions_kits()
                              ext_k.run_kits_extraction()
                        except Exception as e:
                              self.ui.fail(e)      
                              self.menu_principal()
                        self.ui.succes()     
                        self.menu_principal()
                        
                  if self.choice == "4":
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

                  
                  if self.choice == "4":      
                        pass
                  
                  if self.choice.lower() == "x":
                        break"""  
                          
      def schema_generator(self):
            self.ui.schema_generator_ui()
            schema = Publication_schema_builder("cdu_publication", "Code de l'urbanisme", "cdu")
            schema.create_schema()
            schema2 = Publication_schema_builder("autres_règlements", "Autres règlements", "autres")
            schema2.create_schema()
            print("Schemas terminés!")   

if __name__ == "__main__":
    
      Docubo_program()
