from utils.app_settings import app_settings
from paligo_client.paligo_requests.paligo_requests import Paligo_request
from bs4 import BeautifulSoup as Soup
import time
import zipfile, io
import os
import shutil
import glob
from utils.file_access import file_access
from urllib.parse import quote
import PyPDF2
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
import fitz

class Extraction_annexe_B:
    def __init__(self):
        self.grid_f_path = "paligo_client\\generate_pdf_kits\\Bundle de règlement CDU\\Grilles d'exceptions"
        self.path_list = [x for x in glob.glob(f"{self.grid_f_path}\\**\\*.pdf") if x.split('\\')[-1].startswith("Grilles")]
        #print(self.path_list)
        
        
    def run_extraction_annexe_b(self):
        for path in self.path_list:    
            bookmarks_ref = self.split_exception_grids(path, 0)
            self.generate_pdf(bookmarks_ref)
    
    def split_exception_grids(self, input_pdf, level):
        self.pdf_reader = PyPDF2.PdfReader(input_pdf)
        
        bookmarks = self.pdf_reader.outline
        page_splitter_ref = []
        for index, bookmark in enumerate(bookmarks):
            if isinstance(bookmark, list):
                if index >= level:
                    
                    ref_index = 0
                    for i, b in enumerate(bookmark):
                        if not isinstance(b, list):
                            ref_index +=1
                            start_page = self.pdf_reader.get_page_number(b.page)+1
                            if ref_index != 1:
                                previous_end_page = start_page - 1
                                page_splitter_ref[ref_index-2]["end"] = previous_end_page
                            pdf_name = b.title
                            end = 0
                            page_splitter_ref.append({"name": pdf_name, "start": start_page, "end": end})
        
        page_splitter_ref[-1]["end"] = len(self.pdf_reader.pages)
        return page_splitter_ref
        
    def generate_pdf(self, bookmarks_ref: list):
        print("Séparation des grilles d'exception et enregistrement...")
        exception_num = 0
        for grid in bookmarks_ref:
            name = grid["name"]
            pdf_writer = PyPDF2.PdfWriter()
            for page in range(int(grid["start"])-1, int(grid["end"])):
                pdf_writer.add_page(self.pdf_reader.pages[page])
            
            with open(f"{self.grid_f_path}\\{name}_exception.pdf", 'wb') as output_file:
                print(f"{name}")
                exception_num +=1
                pdf_writer.write(output_file)
        print(f"{str(len(exception_num))} éléments sauvegardés.")        
        
            



   

class Pull_publication:
    def __init__(self, prod_id: str, save_path: str, output_file_name: str, prod_name:str):
        self.prod_id = prod_id
        self.save_path = save_path
        self.output_file_name = output_file_name
        self.prod_name = prod_name
        self.paligo_r = Paligo_request("prod")
        self.production = app_settings("prod_paligo_request", "request", "production")[0][1]
        
        
    def publish_and_extract(self):
        response = self.paligo_r.start_publishing(self.production, self.prod_id)
        #print(response)
        production_id = response["id"]
        print("Production: " + self.prod_name)
        print("waiting for production to end: ")
        print("elapsed time: ")
        production = self.paligo_r.list_single_production(self.production, production_id)
        #print(production)
        timer = 0
        while production["url"] == "":
            time.sleep(3)
            production = self.paligo_r.list_single_production(self.production, production_id)
            timer+=3
            print("time: "+str(timer)+ " seconds")
        production_url = production["url"]
        print("Production: " + self.prod_name + " finished!")
        #print(production_url)
        load_zipfile = self.paligo_r.outputs_from_url(production_url)
        
        z = zipfile.ZipFile(io.BytesIO(load_zipfile))
        file_list = z.namelist()
        folder_name = str(file_list[0]).replace("/", "")
        #print(file_list)
        path = file_access("paligo_client\\generate_pdf_kits\\zip_files_for_kits", None)
        z.extractall(path)
        pdf_zip_path = glob.glob(path+f"\\{folder_name}\\out\\*.pdf")
        
        destination_path = file_access(f"paligo_client\\generate_pdf_kits\\{self.save_path}", None)
        #print(pdf_zip_path)
        new_path = os.path.join(destination_path, self.output_file_name + ".pdf")
        
        if not os.path.exists(destination_path):
            print("Creating path")
            os.makedirs(destination_path)
        if os.path.exists(new_path):
            print("replacing existing file")
            os.remove(new_path)
        os.rename(pdf_zip_path[0], new_path)
        
        files = glob.glob(path+"\\*")
        for f in files:
            shutil.rmtree(f)
            print("tmp zip file destroyed!")
        #production_status = [x for x in production if x["id"] == production_id]
        
        
class Extractions_kits:
    def __init__(self, single_document: bool = False, multi_document: list | None = []):
        self.multi_document = multi_document
        self.single_document = single_document
        self.paligo_r = Paligo_request("prod")
        self.doc_url = app_settings("prod_paligo_request", "request", "document")[0][1]
        self.pub_url = app_settings("prod_paligo_request", "request", "publish")[0][1]
        #self.pub_list_table = self.get_kits_publication_list_table()
        #self.paligo_publication_settings = self.get_pub_settings_list()
        
    def run_kits_extraction(self):    
        publish_list = self.validate_publish_settings(pub_settings=self.get_pub_settings_list(), pub_table=self.get_kits_publication_list_table())
        if publish_list is not None:
            for pub in publish_list:
                prod_name = pub["name"]
                prod_id = pub["id"]
                path = pub["path"]
                pdf_name = pub["pdf_name"]
                pull_pub = Pull_publication(prod_id, path, pdf_name, prod_name)
                pull_pub.publish_and_extract()
                
        else:
            print("There is no valid data to publish and extract")
        
    def get_pub_settings_list(self):
        """_summary_

        Returns:
            _type_: _description_
        """        
        responses = self.paligo_r.list_publish_settings(self.pub_url)
        pub_list = []
        for response in responses:
            pub_list.extend(response["publishsettings"])
        return pub_list
        
    def validate_publish_settings(self, pub_settings: list, pub_table: list):
        """Filter threw publish settings to isolate the kits from the paligo kits table.
        
        Only the kits state in the table will be published and save to file.

        Args:
            pub_settings (list): all paligo saved publish settings in batch publish section
            pub_table (list): The paligo topic's table of kits to publish

        Returns:
            filter_settings (list): A list of the publish settings to produce.
        """        
        #print(pub_settings)
        #print(pub_table)
        if self.single_document == False:
            filter_settings = [x for x in pub_settings if str(x["name"]) in [x["publication_settings_name"] for x in pub_table]]
            kits_not_in_settings = [x["publication_settings_name"] for x in pub_table if str(x["publication_settings_name"]) not in [x["name"] for x in pub_settings]]
            for k in kits_not_in_settings:
                if k is not None:
                    print("This publication settings is not in the kits table topic: "+ str(k))
        else:
            if isinstance(self.multi_document, list) and len(self.multi_document) > 0:
                filter_settings = [x for x in pub_settings if str(x["name"]) in self.multi_document]
        full_kits_settings = []
        ## Merge publication setings informations
        if isinstance(filter_settings, list) and len(filter_settings) > 0:
            for kit in filter_settings:
                name = kit["name"]
                _id = kit["id"]
                resource = kit["resource"]
                table_settings = [x for x in pub_table if x["publication_settings_name"] == name][0]
                if len(table_settings) > 0:
                #print(table_settings)
                    path = table_settings["path"]
                    pdf_name = table_settings["pdf_name"]
                    full_kits_settings.append({"id": _id, "name": name, "resource": resource, "path": path, "pdf_name": pdf_name})
                else:
                    raise IndexError("Table settings path and pdf_name out of range")
            return full_kits_settings
        else:
            return None  

    def get_kits_publication_list_table(self):
        kits_table_id = 41345173
        response = self.paligo_r.get_document_by_ids(self.doc_url, kits_table_id, True)
        if response["content"] is not None:
            content_soup = Soup(response["content"], 'xml')
            table_headers = content_soup.find_all("th")
            headers = []
            for th in table_headers:
                th:Soup
                headers.append(th.para.string)
                
            table_rows = content_soup.tbody.find_all("tr")
            
            all_rows = []
            for row in table_rows:
                row:Soup
                table_cells = row.find_all("td")
                row_data = {}
                for index, td in enumerate(table_cells):
                    td:Soup
                    cell_data = td.para.string
                    row_data.update({str(headers[index]): cell_data})
                all_rows.append(row_data)
        return all_rows

if __name__ == "__main__":
    
    
    #worker = pdf_kits_publish_worker()
    #worker.create_publishing_list()
    grid = Extraction_annexe_B()
    # Replace 'input.pdf' with your PDF file's name
    input_pdf = 'paligo_client\\generate_pdf_kits\\pdf_test\\grid_test.pdf'
    # Replace 'output_file_prefix' with the prefix you want for the output files
    output_file_prefix = 'paligo_client\\generate_pdf_kits\\pdf_test\\'
    # Set the level at which you want to split (e.g., 2 for the second level)
    split_level = 0

    grid.run_extraction_annexe_b()
    #grid.split_pdf_by_bookmark("paligo_client\\generate_pdf_kits\\pdf_test\\test")