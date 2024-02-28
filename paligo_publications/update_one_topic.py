import config as cfg
from concurrent.futures import ThreadPoolExecutor
from utils.file_access import file_access
from utils.app_settings import app_settings
from utils.sqlite_db_management import SqLite_DB_manager
from utils.date import Last_change_date
from utils.sqlite_db_management import SqLite_DB_manager
from paligo_publications.topic_media_object_finder import Topic_media_objects_finder as MF

"""{"id": fork_id,"uuid": fork_uuid, "parent": _parent, "position": _position, "depth": _depth, "document": {"id": doc_id, "name": doc_name,"taxonomies": doc_taxonomy, "content": doc_content}"""

