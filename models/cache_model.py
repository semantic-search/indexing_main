import mongoengine
import datetime
from .file_model import *


class Cache(mongoengine.Document):
    """Main model"""
    file_name = mongoengine.StringField(required=True)
    """Name of the file (blob name)"""
    file = mongoengine.FileField(required=True)
    """Original File"""
    mime_type = mongoengine.StringField(required=True)
    """Mime types can be ["jpeg","jpg", "png", "wav","pdf", "docx", "pptx", "xlsx", "epub"] """
    files = mongoengine.EmbeddedDocumentListField(FilesModel)
    date = mongoengine.DateTimeField(default=datetime.datetime.now)
    meta = {
        'db_alias': 'core',
        'collection': 'cache'
    }
