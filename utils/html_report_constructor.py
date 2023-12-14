from utils.sqlite_db_management import SqLite_DB_manager
from utils.useTemplates import useTemplate
from bs4 import BeautifulSoup as Soup
from markdownify import markdownify as md
from paligo_client.paligo_validations.reports.subprocess_docs import serve_validations

class Report_constructor:
    def __init__(self):
        self.markdown_references_path = {
        "ceg_validations": "paligo_client\\paligo_validations\\reports\\docs\\ceg.md",
        "content_validation_results": "paligo_client\\paligo_validations\\reports\\docs\\contenu.md",
        "rules_validations": "paligo_client\\paligo_validations\\reports\\docs\\regles.md",
        "taxonomy_results": "paligo_client\\paligo_validations\\reports\docs\\taxonomies.md"   
    }
        
    def create_report(self, table_name: str):
        """Création d'un rapport html suite à la validation d'une règles

        Prend toutes les validations d'un même type de règles et les assembles dans un rapport html simple pour l'utilisateur

        Args:
            table_name (str): Le nom de la table contenant les rapports bruts de validation

        Returns:
            html_soup_str (str): Un string du html du rapport des validations
        """    
        html_template = useTemplate("paligo_client\\paligo_validations\\reports_templates\\report_template.html")
        template_results = SqLite_DB_manager("db/validations.db", table_name)
        grid_template_part = template_results.fetch_all_data()
        html_soup = Soup(html_template, "lxml")
        html_body = html_soup.body
        stack_table_html = []
        for item in grid_template_part:
            html_part = item[3]
            stack_table_html.append(html_part)
            html_part_soup = Soup(html_part, "lxml")
            
            html_part_soup.body.unwrap()
            html_part_soup.html.unwrap()
            
            html_body.append(html_part_soup)
        html_soup_str = str(html_soup)
        all_table_reports = "".join(stack_table_html)
        self.html_report_to_markdown(all_table_reports, table_name)
        return html_soup_str

    def html_report_to_markdown(self, html_soup: str, table_name: str):
        file_path = self.markdown_references_path[table_name]
        convert_html = md(html_soup, heading_style ="ATX")
        with open(file_path, "w", encoding="utf8") as f:
            f.write(convert_html)
            f.close()
           
        
        """html_soup = Soup(html_soup, "lxml")
        find_h1 = html_soup.find_all("h1")
        find_h2 = html_soup.find_all("h2")
        find_p = html_soup.find_all("p")
        find_tables = html_soup.find_all("table")
        
        for i in find_h1:
            i.insert(0, "## ")
            i.insert_after("\n")
            print(i)
            i.unwrap()
        
        for i in find_h2:
            i.insert(0, "### ")
            i.insert_after("\n")
            i.unwrap()
        
        for i in find_p:
            i.insert_after("\n")
            i.unwrap()
            
        for i in find_tables:
            tr = i.find_all("tr")
            th = i.find_all("th")
            for header in th:
                header.insert(0, "| ")
                header.insert_after(" |\n")
            spacing = "|"+":-----:|"*len(th)+"\n"
            markdown_table_builder = f"{spacing}"
            print(spacing)
        
        print(html_soup)"""
        
    def update_md_docs(self):
        serve_validations()