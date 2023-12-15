publication_schema = {
    "publication_name": "cdu_publication",
    "children": [
        {
            "doc_name": ""
        }
    ]
}

from utils.sqlite_db_management import SqLite_DB_manager
from utils.json_files import save_data_to_json
from operator import itemgetter
from nested_lookup import nested_lookup
from urllib.parse import quote
import config as cfg
from xlsxwriter.workbook import Workbook



class Publication_schema_builder:
    def __init__(self, pub_table:str, publication_name: str, consultation_url_accronym: str):
        self.pub_table = pub_table
        self.publication_name = publication_name
        self.path_interne =f"""{cfg.fe_interne_PROD}/consultation/{consultation_url_accronym}"""
        self.path_externe =f"""{cfg.fe_externe_PROD}/consultation/{consultation_url_accronym}"""
        
        self.sql_db_table = SqLite_DB_manager("db/paligo.db", self.pub_table)
        self.all_data = self.sql_db_table.fetch_all_data()
        self.full_link_list = []
        self.schema = {}
        
    def create_schema(self):
        self.init_schema()
        max_depth = self.check_max_data_depth()
        print(max_depth)
        self.schematize_data(max_depth)
    
    def init_schema(self):
        self.schema.update({"publication_name": self.publication_name, "children": []})
        print(self.schema)
    
    def check_max_data_depth(self):
        depth_list = []
        for row in self.all_data:
            depth = int(row[5])
            depth_list.append(depth)
        max_depth = max(depth_list)
        return max_depth
        
    def transform_and_quote(self, value:str):
        """if value.startswith("CHAPITRE 1 IMPLANT"):
            print("there")"""
        value = str(value).lower()
        value = value.replace(" ", "-")
        value = value.replace("'", "-")
        value = value.replace("’", "-")
        value = value.replace("`", "-")
        value = quote(value)
        return value
    
    def combine_path(self, path_list:list, uuid:str):
        final_path = ""
        for i in path_list:
            final_path+=i+"/"
        final_path+=f"#{uuid}"
        return final_path
                   
    def export_list_to_xlsx(self, data_list: list):
        workbook = Workbook(f"production/mire_mobile/{self.publication_name}_link_list.xlsx")
        ws = workbook.add_worksheet(name=self.publication_name)
        for i, row in enumerate(data_list):
            for j, value in enumerate(row):
                ws.write(i+1, j, row[value])
        for col, key in enumerate(data_list[0]):
            ws.write(0, col, key)
        workbook.close()
    
    def schematize_data(self, max_depth):
        for i in range(max_depth):
            
            curent_depth = i+1
            same_depth = self.sql_db_table.fetch_all_data(parameters= f"WHERE depth LIKE '{curent_depth}'")
            if curent_depth == 1:
                for row in same_depth:
                    fork_id = int(row[1])
                    uuid = row[2]
                    parent = int(row[3])
                    position = int(row[4])
                    depth = int(row[5])
                    doc_id = int(row[6])
                    doc_name = row[7]
                    doc_taxonomies = row[8]
                    doc_content = row[9]
                    num_figures = row[10]
                    figures_data = row[11]
                    children = itemgetter("children"*curent_depth)(self.schema)
                    first_path = self.transform_and_quote(doc_name)
                    path_externe = self.combine_path([self.path_externe, first_path], uuid)
                    path_interne = self.combine_path([self.path_externe, first_path], uuid)
                    children.append({"name": doc_name, "fork_id": int(fork_id), "uuid": uuid, "parent_fork_id": parent, "position": position, "depth": depth, "doc_id": doc_id, "doc_name": doc_name, "doc_taxonomies": doc_taxonomies, "doc_content": doc_content, "num_figures": num_figures, "figures_data": figures_data, "path_interne": path_interne, "path_externe": path_externe, "children": []})
                    self.full_link_list.append({"name": doc_name, "fork_id": int(fork_id), "uuid": uuid, "parent_fork_id": parent, "position": position, "depth": depth, "doc_id": doc_id, "doc_name": doc_name, "doc_taxonomies": doc_taxonomies, "doc_content": doc_content, "num_figures": num_figures, "figures_data": figures_data, "path_interne": path_interne, "path_externe": path_externe})
            if curent_depth == 2:
                same_depth = self.sql_db_table.fetch_all_data(parameters= f"WHERE depth LIKE '{curent_depth}'")
                for row in same_depth:
                    fork_id = int(row[1])
                    uuid = row[2]
                    parent = int(row[3])
                    position = int(row[4])
                    depth = int(row[5])
                    doc_id = int(row[6])
                    doc_name = row[7]
                    doc_taxonomies = row[8]
                    doc_content = row[9]
                    num_figures = row[10]
                    figures_data = row[11]
                    
                    get_parent_object = [x for x in self.schema["children"] if x["fork_id"] == parent][0]
                    first_path = self.transform_and_quote(get_parent_object["name"])
                    second_path = self.transform_and_quote(doc_name)
                    path_externe = self.combine_path([self.path_externe, first_path, second_path], uuid)
                    path_interne = self.combine_path([self.path_externe, first_path, second_path], uuid)
                    get_parent_object["children"].append({"name": doc_name, "fork_id": int(fork_id), "uuid": uuid, "parent_fork_id": parent, "position": position, "depth": depth, "doc_id": doc_id, "doc_name": doc_name, "doc_taxonomies": doc_taxonomies, "doc_content": doc_content, "num_figures": num_figures, "figures_data": figures_data, "path_interne": path_interne, "path_externe": path_externe, "children": []})
                    self.full_link_list.append({"name": doc_name, "fork_id": int(fork_id), "uuid": uuid, "parent_fork_id": parent, "position": position, "depth": depth, "doc_id": doc_id, "doc_name": doc_name, "doc_taxonomies": doc_taxonomies, "doc_content": doc_content, "num_figures": num_figures, "figures_data": figures_data, "path_interne": path_interne, "path_externe": path_externe})
            if curent_depth == 3:
                same_depth = self.sql_db_table.fetch_all_data(parameters= f"WHERE depth LIKE '{curent_depth}'")
                for row in same_depth:
                    fork_id = int(row[1])
                    uuid = row[2]
                    parent = int(row[3])
                    position = int(row[4])
                    depth = int(row[5])
                    doc_id = int(row[6])
                    doc_name = row[7]
                    doc_taxonomies = row[8]
                    doc_content = row[9]
                    num_figures = row[10]
                    figures_data = row[11]
                    for items in self.schema["children"]:
                        if len(items["children"]) != 0:
                            
                            depth_2_parent = items["children"]
                            
                            get_parent_object = [x for x in depth_2_parent if x["fork_id"] == parent]
                            
                            if len(get_parent_object):
                                first_path = self.transform_and_quote(items["name"])
                                second_path = self.transform_and_quote(get_parent_object[0]["name"])
                                path_externe = self.combine_path([self.path_externe, first_path, second_path], uuid)
                                path_interne = self.combine_path([self.path_externe, first_path, second_path], uuid)
                                get_parent_object[0]["children"].append({"name": doc_name, "fork_id": int(fork_id), "uuid": uuid, "parent_fork_id": parent, "position": position, "depth": depth, "doc_id": doc_id, "doc_name": doc_name, "doc_taxonomies": doc_taxonomies, "doc_content": doc_content, "num_figures": num_figures, "figures_data": figures_data, "path_interne": path_interne, "path_externe": path_externe, "children": []})        
                                self.full_link_list.append({"name": doc_name, "fork_id": int(fork_id), "uuid": uuid, "parent_fork_id": parent, "position": position, "depth": depth, "doc_id": doc_id, "doc_name": doc_name, "doc_taxonomies": doc_taxonomies, "doc_content": doc_content, "num_figures": num_figures, "figures_data": figures_data, "path_interne": path_interne, "path_externe": path_externe})
            if curent_depth == 4:
                same_depth = self.sql_db_table.fetch_all_data(parameters= f"WHERE depth LIKE '{curent_depth}'")
                for row in same_depth:
                    fork_id = int(row[1])
                    uuid = row[2]
                    parent = int(row[3])
                    position = int(row[4])
                    depth = int(row[5])
                    doc_id = int(row[6])
                    doc_name = row[7]
                    doc_taxonomies = row[8]
                    doc_content = row[9]
                    num_figures = row[10]
                    figures_data = row[11]
                    for title in self.schema["children"]:
                        if len(title["children"]) != 0:
                            for chapter in title["children"]:
                                depth_3_parent = chapter["children"]
                                get_parent_object = [x for x in depth_3_parent if x["fork_id"] == parent]
                                if len(get_parent_object):
                                    first_path = self.transform_and_quote(title["name"])
                                    second_path = self.transform_and_quote(chapter["name"])
                                    path_externe = self.combine_path([self.path_externe, first_path, second_path], uuid)
                                    path_interne = self.combine_path([self.path_externe, first_path, second_path], uuid)
                                    get_parent_object[0]["children"].append({"name": doc_name, "fork_id": int(fork_id), "uuid": uuid, "parent_fork_id": parent, "position": position, "depth": depth, "doc_id": doc_id, "doc_name": doc_name, "doc_taxonomies": doc_taxonomies, "doc_content": doc_content, "num_figures": num_figures, "figures_data": figures_data, "path_interne": path_interne, "path_externe": path_externe, "children": []})        
                                    self.full_link_list.append({"name": doc_name, "fork_id": int(fork_id), "uuid": uuid, "parent_fork_id": parent, "position": position, "depth": depth, "doc_id": doc_id, "doc_name": doc_name, "doc_taxonomies": doc_taxonomies, "doc_content": doc_content, "num_figures": num_figures, "figures_data": figures_data, "path_interne": path_interne, "path_externe": path_externe})
            if curent_depth == 5:
                same_depth = self.sql_db_table.fetch_all_data(parameters= f"WHERE depth LIKE '{curent_depth}'")
                for row in same_depth:
                    fork_id = int(row[1])
                    uuid = row[2]
                    parent = int(row[3])
                    position = int(row[4])
                    depth = int(row[5])
                    doc_id = int(row[6])
                    doc_name = row[7]
                    doc_taxonomies = row[8]
                    doc_content = row[9]
                    num_figures = row[10]
                    figures_data = row[11]
                    for title in self.schema["children"]:
                        if len(items["children"]) != 0:
                            for chapter in title["children"]:
                                if len(chapter["children"]) != 0:
                                    for section in chapter["children"]:
                                        depth_4_parent = section["children"]
                                        get_parent_object = [x for x in depth_4_parent if x["fork_id"] == parent]
                                        if len(get_parent_object):
                                            first_path = self.transform_and_quote(title["name"])
                                            second_path = self.transform_and_quote(chapter["name"])
                                            path_externe = self.combine_path([self.path_externe, first_path, second_path], uuid)
                                            path_interne = self.combine_path([self.path_externe, first_path, second_path], uuid)
                                            get_parent_object[0]["children"].append({"name": doc_name, "fork_id": int(fork_id), "uuid": uuid, "parent_fork_id": parent, "position": position, "depth": depth, "doc_id": doc_id, "doc_name": doc_name, "doc_taxonomies": doc_taxonomies, "doc_content": doc_content, "num_figures": num_figures, "figures_data": figures_data, "path_interne": path_interne, "path_externe": path_externe, "children": []})        
                                            self.full_link_list.append({"name": doc_name, "fork_id": int(fork_id), "uuid": uuid, "parent_fork_id": parent, "position": position, "depth": depth, "doc_id": doc_id, "doc_name": doc_name, "doc_taxonomies": doc_taxonomies, "doc_content": doc_content, "num_figures": num_figures, "figures_data": figures_data, "path_interne": path_interne, "path_externe": path_externe})
        print("Schéma de la publication complété!")
        save_data_to_json(self.schema, f"production/schema/{self.publication_name}_schema.json")
        save_data_to_json(self.full_link_list, f"production/mire_mobile/{self.publication_name}_link_list.json")
        self.export_list_to_xlsx(self.full_link_list)
        

if __name__ == "__main__":
    schema = Publication_schema_builder("cdu_publication", "Code de l'urbanisme", "cdu")
    schema.create_schema()