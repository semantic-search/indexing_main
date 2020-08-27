import mongoengine


class FilesModel(mongoengine.EmbeddedDocument):
    files = mongoengine.FileField()
