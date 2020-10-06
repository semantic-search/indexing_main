import uuid
from db_models.models.cache_model import Cache
from db_models.mongo_setup import global_init
import os
import init
import globals
import subprocess


def send_to_topic(topic, value):
    print("####################################")
    print(topic)
    subprocess.call(["python3", "task_utils/kafka_send.py", str(topic), str(value)])


def send_to_kafka_topics(group, pk):
    print("in send ################")
    print(group)
    print(pk)
    if group == "image" or group == "document":
        print("in image")
        print(globals.image_captioning_containers)
        if globals.image_captioning_containers is not None:
            print("in caption")
            for container in globals.image_captioning_containers:
                print(container)
                send_to_topic(topic=container, value=pk)

        if globals.ocr_containers is not None:
            for container in globals.ocr_containers:
                print(container)
                send_to_topic(topic=container, value=pk)
        if globals.object_detection_containers is not None:
            for container in globals.object_detection_containers:
                print(container)
                send_to_topic(topic=container, value=pk)
        if globals.scene_recognition_containers is not None:
            for container in globals.scene_recognition_containers:
                print(container)
                send_to_topic(topic=container, value=pk)
        if globals.image_recognition_containers is not None:
            for container in globals.image_recognition_containers:
                print(container)
                send_to_topic(topic=container, value=pk)
        if globals.image_search_containers is not None:
            for container in globals.image_search_containers:
                print(container)
                send_to_topic(topic=container, value=pk)

    elif group == "audio" or group == "video":
        if globals.sound_classification_containers is not None:
            for container in globals.sound_classification_containers:
                print(container)
                send_to_topic(topic=container, value=pk)
        if globals.audio_fingerprinting_containers is not None:
            for container in globals.audio_fingerprinting_containers:
                print(container)
                send_to_topic(topic=container, value=pk)
        if globals.speech_to_text_containers is not None:
            for container in globals.speech_to_text_containers:
                print(container)
                send_to_topic(topic=container, value=pk)


def image_audio_to_db_and_add_to_kafka(group, file_name, file_to_save, extension, rmdir=False, to_rmdir=None):
    global_init()
    db_object = Cache()
    db_object.file_name = file_name
    db_object.mime_type = extension
    db_object.is_doc_type = False
    with open(file_to_save, 'rb') as fd:
        db_object.file.put(fd)
    print("######################################")
    if group == "image":
        print("sending to kafka")
        send_to_kafka_topics(group=group, pk=db_object.pk)
        photo_location = init.file_extract_obj.exif_to_location(file_to_save)
        print("'''''''''''''''''''''''''''''''''''''''''")
        print(photo_location)
        print("*****************************************")
        print("'''''''''''''''''''''''''''''''''''''''''")
        if photo_location is not None:
            print("'''''''''''''''''''''''''''''''''''''''''")
            print("*****************************************")
            print("'''''''''''''''''''''''''''''''''''''''''")
            db_object.image_location = photo_location
        db_object.save()
    elif group == "audio" or group == "video":
        send_to_kafka_topics(group=group, pk=db_object.pk)
        db_object.save()
    if rmdir:
        pass


def download_blob(provider, blob_to_download):
    if provider == "Azure":
        blob_client = init.blob_service_client.get_blob_client(container=globals.BLOB_STORAGE_CONTAINER_NAME,
                                                               blob=blob_to_download)
        new_directory = "Downloads/" + str(uuid.uuid4()) + "/"
        os.mkdir(new_directory)
        download_file = new_directory + str(blob_to_download)
        with open(download_file, 'wb') as file_obj:
            file_obj.write(blob_client.download_blob().readall())
        downloaded_blob_info = {
            "file": download_file,
            "directory": new_directory
        }
        return downloaded_blob_info


file = "exif.jpg"
downloaded_blob_info = download_blob(
        provider=globals.STORAGE_PROVIDER,
        blob_to_download=file
    )
file_to_index = downloaded_blob_info["file"]
new_directory = downloaded_blob_info["directory"]
print(file_to_index)
print(new_directory)

image_audio_to_db_and_add_to_kafka(file_to_save=file_to_index,
                                   extension="jpg",
                                   file_name=file,
                                   rmdir=True,
                                   to_rmdir=new_directory,
                                   group="image"
                                   )