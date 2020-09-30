from db_models.models.cache_model import Cache
from db_models.models.file_model import FilesModel
import shutil
from db_models.mongo_setup import global_init
from .kafka_parse_utils import send_to_kafka_topics


def doc_to_db_and_add_to_kafka(text, file_name, file_dir, file_to_save, extension, images_dict, contains_images):
    global_init()
    db_object = Cache()
    image_db_list = []
    images_list = images_dict["images"]
    db_object.file_name = file_name
    db_object.is_doc_type = True
    db_object.mime_type = extension
    """saving pdf to db"""
    with open(file_to_save, 'rb') as fd:
        db_object.file.put(fd)
    if contains_images:
        """Saving images to db"""
        for image in images_list:
            print(image)
            with open(image, 'rb') as fd:
                image_db_list.append(FilesModel(file=fd))
        db_object.files = image_db_list
        db_object.contains_images = True
    else:
        db_object.contains_images = False
    db_object.text = text
    db_object.save()
    shutil.rmtree(images_dict["images_folder"])
    shutil.rmtree(file_dir)
    send_to_kafka_topics(group="document", pk=db_object.pk)
