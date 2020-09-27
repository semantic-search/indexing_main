import globals
import init
import uuid
import os
from db_models.models.file_model import FilesModel
from db_models.mongo_setup import global_init
from db_models.models.cache_model import Cache
import shutil
from pathlib import Path
from task_worker.celery import celery_app


def doc_to_db_and_add_to_kafka(text, file_name, file_dir, file_to_save, extension, images_dict, contains_images):
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


def image_audio_to_db_and_add_to_kafka(group, file_name, file_to_save, extension, rmdir=False, to_rmdir=None):
    db_object = Cache()
    db_object.file_name = file_name
    db_object.mime_type = extension
    db_object.is_doc_type = False
    with open(file_to_save, 'rb') as fd:
        db_object.file.put(fd)
    db_object.save()
    os.remove(file_to_save)
    if rmdir:
        shutil.rmtree(to_rmdir)
    if group == "image":
        send_to_kafka_topics(group=group, pk=db_object.pk)
    elif group == "audio" or group == "video":
        send_to_kafka_topics(group=group, pk=db_object.pk)



def send_to_kafka_topics(group, pk):
    if group == "image" or group == "document":
        if globals.image_captioning_containers is not None:
            for container in globals.image_captioning_containers:
                future = init.producer_obj.send(container, value=str(pk))
                future.get(timeout=60)

        if globals.ocr_containers is not None:
            for container in globals.ocr_containers:
                future = init.producer_obj.send(container, value=str(pk))
                future.get(timeout=60)
        if globals.object_detection_containers is not None:
            for container in globals.object_detection_containers:
                future = init.producer_obj.send(container, value=str(pk))
                future.get(timeout=60)
        if globals.scene_recognition_containers is not None:
            for container in globals.scene_recognition_containers:
                future = init.producer_obj.send(container, value=str(pk))
                future.get(timeout=60)
        if globals.image_recognition_containers is not None:
            for container in globals.image_recognition_containers:
                future = init.producer_obj.send(container, value=str(pk))
                future.get(timeout=60)
        if globals.image_search_containers is not None:
            for container in globals.image_search_containers:
                future = init.producer_obj.send(container, value=str(pk))
                future.get(timeout=60)

    elif group == "audio" or group == "video":
        if globals.sound_classification_containers is not None:
            for container in globals.sound_classification_containers:
                future = init.producer_obj.send(container, value=str(pk))
                future.get(timeout=60)
        if globals.audio_fingerprinting_containers is not None:
            for container in globals.audio_fingerprinting_containers:
                future = init.producer_obj.send(container, value=str(pk))
                future.get(timeout=60)
        if globals.speech_to_text_containers is not None:
            for container in globals.speech_to_text_containers:
                future = init.producer_obj.send(container, value=str(pk))
                future.get(timeout=60)

@celery_app.task()
def main(file):
    global_init()
    blob_client = init.blob_service_client.get_blob_client(container=globals.BLOB_STORAGE_CONTAINER_NAME, blob=file)
    new_directory = "Downloads/" + str(uuid.uuid4()) + "/"
    os.mkdir(new_directory)
    download_file = new_directory + str(file)
    with open(download_file, 'wb') as file_obj:
        file_obj.write(blob_client.download_blob().readall())
    mime_dict = init.file_check_obj.check_mime_type(download_file)
    if mime_dict is not None:
        extension = mime_dict["extension"]
        group = mime_dict["group"]
        if group == "document":
            if extension == "pdf":
                check_if_encrypt = init.file_check_obj.check_pdf_encrypted(download_file)
                if check_if_encrypt:
                    shutil.rmtree(new_directory)
                else:
                    text = init.file_extract_obj.extract_text_pdf(download_file)
                    images_dict = init.file_extract_obj.extract_images_pdf(download_file)
                    if len(images_dict["images"]) == 0:
                        contains_images = False
                    else:
                        contains_images = True
                    doc_to_db_and_add_to_kafka(text=text,
                                               file_name=file,
                                               file_to_save=download_file,
                                               extension=extension,
                                               images_dict=images_dict,
                                               contains_images=contains_images,
                                               file_dir=new_directory
                                               )
            elif extension == "docx" or extension == "pptx" or extension == "xlsx" or extension == "odt" or  extension =="epub":
                text = init.file_extract_obj.extract_text_docs(download_file)
                images_dict = init.file_extract_obj.extract_images_docs(download_file, extension, file_name=file)
                if len(images_dict["images"]) == 0:
                    contains_images = False
                else:
                    contains_images = True
                doc_to_db_and_add_to_kafka(text=text,
                                           file_name=file,
                                           file_to_save=download_file,
                                           extension=extension,
                                           images_dict=images_dict,
                                           contains_images=contains_images,
                                           file_dir=new_directory
                                           )

        elif group == "legacy_document":
            converted_file = init.file_convert_obj.convert_doc(file=download_file, target_extension=extension+"x")
            file_name = Path(converted_file).name
            images_dict = init.file_extract_obj.extract_images_docs(file=converted_file, extension=extension+"x", file_name=file_name)
            text = init.file_extract_obj.extract_text_docs(converted_file)
            os.remove(converted_file)
            if len(images_dict["images"]) == 0:
                contains_images = False
            else:
                contains_images = True
            doc_to_db_and_add_to_kafka(text=text,
                                       file_name=file,
                                       file_to_save=download_file,
                                       extension=extension,
                                       images_dict=images_dict,
                                       contains_images=contains_images,
                                       file_dir=new_directory
                                       )
        elif group == "audio":
            target_file = init.file_convert_obj.convert_audio(source_format=extension, file=download_file)
            shutil.rmtree(new_directory)
            image_audio_to_db_and_add_to_kafka(file_to_save=target_file,
                                               extension="wav",
                                               file_name=file
                                               )
        elif group == "image":
            if extension == "jpg" or extension == "png":
                image_audio_to_db_and_add_to_kafka(file_to_save=download_file,
                                                   extension=extension,
                                                   file_name=file,
                                                   rmdir=True,
                                                   to_rmdir=new_directory,
                                                   group=group
                                                   )
            elif extension == "svg":
                target_file = init.file_convert_obj.convert_svg(file=download_file)
                shutil.rmtree(new_directory)
                image_audio_to_db_and_add_to_kafka(file_to_save=target_file,
                                                   extension="png",
                                                   file_name=file,
                                                   group=group
                                                   )
        elif group == "video":
            target_file = init.file_convert_obj.convert_video(source_format=extension, file=download_file)
            shutil.rmtree(new_directory)
            image_audio_to_db_and_add_to_kafka(file_to_save=target_file,
                                               extension="wav",
                                               file_name=file,
                                               group=group
                                               )
    else:
        shutil.rmtree(new_directory)
