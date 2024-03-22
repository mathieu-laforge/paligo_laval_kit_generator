import unittest
from paligo_rebuild_versionning.find_versions import Find_topic_versions

class TestStructureData(unittest.TestCase):

    def test_xml_string_v1(self):
        input_xml = """
        
        <section role="titre" version="5.0" xinfo:resource="UUID-8331f403-48d1-7433-e659-dfc7bd8dd4a5" xinfo:resource-id="5259006" xinfo:resource-title="Code de l'urbanisme" xinfo:resource-titlelabel="" xinfo:resource-type="component fork" xinfo:version-major="2" xinfo:version-minor="2" xml:id="UUID-8331f403-48d1-7433-e659-dfc7bd8dd4a5" dir="ltr" xml:lang="fr" xinfo:origin="UUID-6b10868f-7bf0-92c6-22b7-22a4459fb90d" xinfo:origin-id="5259000" xinfo:time-modified="1681497647" xinfo:time-created="1647655027" xinfo:linktype="ResourceLink">

            \n<title>\n<emphasis role=\"bold\">CODE DE L'URBANISME</emphasis>\n</title>\n<mediaobject>\n<imageobject>\n<imagedata fileref=\"image/uuid-6a55d7c8-5a31-15cb-0d58-6b3e4d907598.svg\" xinfo:image=\"5258999\" xinfo:image-description=\"\" xinfo:image-filename=\"page_presentation_cdu_code_urbanisme.svg\" xinfo:image-title=\"img-00_00_00_00_01_frontPageCdu.svg\"/>\n</imageobject>\n</mediaobject>\n
        </section>
        """
        expected_output = [
            {
                "content": "\n<title>\n<emphasis role=\"bold\">CODE DE L'URBANISME</emphasis>\n</title>\n<mediaobject>\n<imageobject>\n<imagedata fileref=\"image/uuid-6a55d7c8-5a31-15cb-0d58-6b3e4d907598.svg\" xinfo:image=\"5258999\" xinfo:image-description=\"\" xinfo:image-filename=\"page_presentation_cdu_code_urbanisme.svg\" xinfo:image-title=\"img-00_00_00_00_01_frontPageCdu.svg\"/>\n</imageobject>\n</mediaobject>\n",
                "attributes": {
                    "role": "titre",
                    "version": "5.0",
                    "xinfo:resource": "UUID-8331f403-48d1-7433-e659-dfc7bd8dd4a5",
                    "fork_id": "5259006",
                    "xinfo:resource-id": "5259006",
                    "xinfo:resource-title": "Code de l'urbanisme",
                    "xinfo:resource-titlelabel": "",
                    "xinfo:resource-type": "component fork",
                    "xinfo:version-major": "2",
                    "xinfo:version-minor": "2",
                    "xml:id": "UUID-8331f403-48d1-7433-e659-dfc7bd8dd4a5",
                    "dir": "ltr",
                    "xml:lang": "fr",
                    "xinfo:origin": "UUID-6b10868f-7bf0-92c6-22b7-22a4459fb90d",
                    "xinfo:origin-id": "5259000",
                    "xinfo:time-modified": "1681497647",
                    "xinfo:time-created": "1647655027",
                    "xinfo:linktype": "ResourceLink"
                }
            }
        ]
        structure_data = Find_topic_versions()
        output = structure_data.xml_string_v1(input_xml)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()