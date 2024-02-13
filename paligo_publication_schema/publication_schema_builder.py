from xlsxwriter.workbook import Workbook
import config as cfg
from urllib.parse import quote
from nested_lookup import nested_lookup
from operator import itemgetter
from utils.json_files import save_data_to_json
from utils.sqlite_db_management import SqLite_DB_manager
from bs4 import BeautifulSoup as Soup

publication_schema = {
    "publication_name": "cdu_publication",
    "children": [
        {
            "doc_name": ""
        }
    ]
}

class Content_meta:
    def __init__(self, content):
        self.content = Soup(content, "xml")
        if "xinfo:version" in self.content.section.attrs:
            self.version  = int(self.content.section["xinfo:version"])
        else:
            self.version = None
        if "role" in self.content.section.attrs:
            self.roles = self.content.section["role"]
        else:
            self.roles = None
        
    
class Data_structure:
    """Parse the metadata of a topic
    """    
    def __init__(self, row_data):
        """Initialize the data structure

        Args:
            row_data (tuple): The tuple returned from a Sqlite3 query
        """        
        self.fork_id = int(row_data[1])
        self.uuid = row_data[2]
        self.parent = int(row_data[3])
        self.position = int(row_data[4])
        self.depth = int(row_data[5])
        self.doc_id = int(row_data[6])
        self.doc_name = row_data[7]
        self.doc_taxonomies = row_data[8]
        self.doc_content = row_data[9]
        self.num_figures = row_data[10]
        self.figures_data = row_data[11]
        self.c_meta = Content_meta(self.doc_content)
        

    def to_dict(self):
        """Create a dictionnary from data row

        Returns:
            (dict): Return a dictionnary of parsed meta informations
        """        
        

        return {"uuid": self.uuid, "doc_id": self.doc_id, "doc_name": self.doc_name, "role": self.c_meta.roles, "version": self.c_meta.version ,"num_figures": self.num_figures, "fork_id": self.fork_id, "path_interne": "", "path_externe": "", "children": []}


class Publication_schema_builder:
    def __init__(self, pub_table: str, publication_name: str, consultation_url_accronym: str):
        """Initialize the publication schema

        Args:
            pub_table (str): Name of the table in the Sqlite DB
            publication_name (str): Name of the publication
            consultation_url_accronym (str): accronym from info-reglements web site paths to articles (cdu or autres)
        """        
        self.pub_table = pub_table
        self.publication_name = publication_name
        self.path_interne = f"""{cfg.fe_interne_PROD}/consultation/{consultation_url_accronym}"""
        self.path_externe = f"""{cfg.fe_externe_PROD}/consultation/{consultation_url_accronym}"""

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
        self.schema.update(
            {"publication_name": self.publication_name, "children": []})
        print(self.schema)

    def check_max_data_depth(self):
        depth_list = []
        for row in self.all_data:
            depth = int(row[5])
            depth_list.append(depth)
        max_depth = max(depth_list)
        return max_depth

    def transform_and_quote(self, value: str):
        """if value.startswith("CHAPITRE 1 IMPLANT"):
            print("there")"""
        value = str(value).lower()
        value = value.replace(" ", "-")
        value = value.replace("'", "-")
        value = value.replace("’", "-")
        value = value.replace("`", "-")
        value = quote(value)
        return value

    def combine_path(self, path_list: list, uuid: str):
        final_path = ""
        for i in path_list:
            final_path += i+"/"
        final_path += f"#{uuid}"
        return final_path

    def export_list_to_xlsx(self, data_list: list):
        workbook = Workbook(
            f"production/mire_mobile/{self.publication_name}_link_list.xlsx")
        ws = workbook.add_worksheet(name=self.publication_name)
        for i, row in enumerate(data_list):
            for j, value in enumerate(row):
                if value != "children":
                    ws.write(i+1, j, row[value])
        for col, key in enumerate(data_list[0]):
            ws.write(0, col, key)
        workbook.close()

    def schematize_data(self, max_depth):
        for i in range(max_depth):

            curent_depth = i+1
            same_depth = self.sql_db_table.fetch_all_data(
                parameters=f"WHERE depth LIKE '{curent_depth}'")
            if curent_depth == 1:
                for row in same_depth:
                    self.data_structure = Data_structure(row)
                    data_dict = self.data_structure.to_dict()
                    
                    # get the location for this topic
                    children = itemgetter("children"*curent_depth)(self.schema)
                    
                    # create path
                    first_path = self.transform_and_quote(data_dict["doc_name"])
                    data_dict["path_externe"] = self.combine_path(
                        [self.path_externe, first_path], data_dict["uuid"])
                    data_dict["path_interne"] = self.combine_path(
                        [self.path_externe, first_path], data_dict["uuid"])
                    
                    children.append(data_dict)
                    self.full_link_list.append(data_dict)
                    
            if curent_depth == 2:
                same_depth = self.sql_db_table.fetch_all_data(
                    parameters=f"WHERE depth LIKE '{curent_depth}'")
                for row in same_depth:
                    self.data_structure = Data_structure(row)
                    data_dict = self.data_structure.to_dict()
                    # get the location for this topic
                    get_parent_object = [
                        x for x in self.schema["children"] if x["fork_id"] == self.data_structure.parent][0]
                    
                    # create path within chapter
                    first_path = self.transform_and_quote(
                        get_parent_object["doc_name"])
                    second_path = self.transform_and_quote(self.data_structure.doc_name)
                    data_dict["path_externe"] = self.combine_path(
                        [self.path_externe, first_path, second_path], self.data_structure.uuid)
                    data_dict["path_interne"] = self.combine_path(
                        [self.path_externe, first_path, second_path], self.data_structure.uuid)
                    get_parent_object["children"].append(data_dict)
                    self.full_link_list.append(data_dict)
            if curent_depth == 3:
                same_depth = self.sql_db_table.fetch_all_data(
                    parameters=f"WHERE depth LIKE '{curent_depth}'")
                for row in same_depth:
                    self.data_structure = Data_structure(row)
                    data_dict = self.data_structure.to_dict()
                    
                    for items in self.schema["children"]:
                        if len(items["children"]) != 0:

                            depth_2_parent = items["children"]

                            get_parent_object = [
                                x for x in depth_2_parent if x["fork_id"] == self.data_structure.parent]

                            if len(get_parent_object):
                                first_path = self.transform_and_quote(
                                    items["doc_name"])
                                second_path = self.transform_and_quote(
                                    get_parent_object[0]["doc_name"])
                                data_dict["path_externe"] = self.combine_path(
                                    [self.path_externe, first_path, second_path], self.data_structure.uuid)
                                data_dict["path_interne"] = self.combine_path(
                                    [self.path_externe, first_path, second_path], self.data_structure.uuid)
                                get_parent_object[0]["children"].append(data_dict)
                                self.full_link_list.append(data_dict)
            if curent_depth == 4:
                same_depth = self.sql_db_table.fetch_all_data(
                    parameters=f"WHERE depth LIKE '{curent_depth}'")
                for row in same_depth:
                    self.data_structure = Data_structure(row)
                    data_dict = self.data_structure.to_dict()
                    
                    for title in self.schema["children"]:
                        if len(title["children"]) != 0:
                            for chapter in title["children"]:
                                depth_3_parent = chapter["children"]
                                get_parent_object = [
                                    x for x in depth_3_parent if x["fork_id"] == self.data_structure.parent]
                                if len(get_parent_object):
                                    first_path = self.transform_and_quote(
                                        title["doc_name"])
                                    second_path = self.transform_and_quote(
                                        chapter["doc_name"])
                                    data_dict["path_externe"] = self.combine_path(
                                        [self.path_externe, first_path, second_path], self.data_structure.uuid)
                                    data_dict["path_interne"] = self.combine_path(
                                        [self.path_externe, first_path, second_path], self.data_structure.uuid)
                                    get_parent_object[0]["children"].append(data_dict)
                                    self.full_link_list.append(data_dict)
            if curent_depth == 5:
                same_depth = self.sql_db_table.fetch_all_data(
                    parameters=f"WHERE depth LIKE '{curent_depth}'")
                for row in same_depth:
                    self.data_structure = Data_structure(row)
                    data_dict = self.data_structure.to_dict()
                    for title in self.schema["children"]:
                        if len(items["children"]) != 0:
                            for chapter in title["children"]:
                                if len(chapter["children"]) != 0:
                                    for section in chapter["children"]:
                                        depth_4_parent = section["children"]
                                        get_parent_object = [
                                            x for x in depth_4_parent if x["fork_id"] == self.data_structure.parent]
                                        if len(get_parent_object):
                                            first_path = self.transform_and_quote(
                                                title["doc_name"])
                                            second_path = self.transform_and_quote(
                                                chapter["doc_name"])
                                            data_dict["path_externe"] = self.combine_path(
                                                [self.path_externe, first_path, second_path], self.data_structure.uuid)
                                            data_dict["path_interne"] = self.combine_path(
                                                [self.path_externe, first_path, second_path], self.data_structure.uuid)
                                            get_parent_object[0]["children"].append(data_dict)
                                            self.full_link_list.append(data_dict)
        print("Schéma de la publication complété!")
        save_data_to_json(
            self.schema, f"production/schema/{self.publication_name}_schema.json")
        save_data_to_json(
            self.full_link_list, f"production/mire_mobile/{self.publication_name}_link_list.json")
        self.export_list_to_xlsx(self.full_link_list)


if __name__ == "__main__":
    schema = Publication_schema_builder(
        "cdu_publication", "Code de l'urbanisme", "cdu")
    schema.create_schema()
