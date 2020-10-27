from db_models.models.cache_model import Cache
from db_models.mongo_setup import global_init
import os
import shutil
from .kafka_parse_utils import send_to_kafka_topics
import init
import pathlib


def image_audio_to_db_and_add_to_kafka(group, file_name, file_to_save, extension, rmdir=False, to_rmdir=None):
    global_init()
    db_object = Cache()
    db_object.file_name = pathlib.Path(file_name).stem + "." + extension
    db_object.mime_type = extension
    db_object.is_doc_type = False
    with open(file_to_save, 'rb') as fd:
        db_object.file.put(fd)
    print("######################################")
    if group == "image":
        print("sending to kafka")
        photo_location = init.file_extract_obj.exif_to_location(file_to_save)
        if photo_location is not None:
            db_object.image_location = photo_location
        db_object.save()
        os.remove(file_to_save)
        send_to_kafka_topics(group=group, pk=db_object.pk)
    elif group == "audio" or group == "video":
        db_object.save()
        os.remove(file_to_save)
        send_to_kafka_topics(group=group, pk=db_object.pk)
    if rmdir:
        shutil.rmtree(to_rmdir)
