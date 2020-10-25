import init
import os
import shutil
from pathlib import Path
from task_worker.celery import celery_app
from task_utils.download_file_from_storage import download_blob
from task_utils.image_or_audio_add_to_db import image_audio_to_db_and_add_to_kafka
from task_utils.document_add_to_db import doc_to_db_and_add_to_kafka
from task_utils.populator import populate_lists
from task_utils.remove_file import remove_api
import globals
import pathlib


@celery_app.task()
def main(file, group_array, api_mode=False):
    populate_lists(group_array)
    if api_mode:
        file_to_index = file["file"]
        new_directory = file["directory"]
        file = Path(file_to_index).name
    else:
        downloaded_blob_info = download_blob(
            provider=globals.STORAGE_PROVIDER,
            blob_to_download=file
        )
        file_to_index = downloaded_blob_info["file"]
        new_directory = downloaded_blob_info["directory"]
    mime_dict = init.file_check_obj.check_mime_type(file=file_to_index)
    if mime_dict is not None:
        extension = mime_dict["extension"]
        group = mime_dict["group"]
        if group == "document":
            if extension == "pdf":
                check_if_encrypt = init.file_check_obj.check_pdf_encrypted(file_to_index)
                if check_if_encrypt:
                    remove_api(file, "last_doc_image")
                    init.send_log_msg("ENCRYPTED PDF " + file + " of type last_doc_image")
                    shutil.rmtree(new_directory)
                else:
                    text = init.file_extract_obj.extract_text_pdf(file_to_index)
                    images_dict = init.file_extract_obj.extract_images_pdf(file_to_index)
                    if len(images_dict["images"]) == 0:
                        contains_images = False
                    else:
                        contains_images = True
                    doc_to_db_and_add_to_kafka(text=text,
                                               file_name=file,
                                               file_to_save=file_to_index,
                                               extension=extension,
                                               images_dict=images_dict,
                                               contains_images=contains_images,
                                               file_dir=new_directory
                                               )
            elif extension == "docx" or \
                    extension == "pptx" or \
                    extension == "xlsx" or \
                    extension == "odt" or \
                    extension == "epub":
                text = init.file_extract_obj.extract_text_docs(file_to_index)
                images_dict = init.file_extract_obj.extract_images_docs(file_to_index, extension, file_name=file)
                if len(images_dict["images"]) == 0:
                    contains_images = False
                else:
                    contains_images = True
                doc_to_db_and_add_to_kafka(text=text,
                                           file_name=file,
                                           file_to_save=file_to_index,
                                           extension=extension,
                                           images_dict=images_dict,
                                           contains_images=contains_images,
                                           file_dir=new_directory
                                           )

        elif group == "legacy_document":
            converted_file = init.file_convert_obj.convert_doc(file=file_to_index, target_extension=extension + "x")
            if converted_file is not None:
                file_name = Path(converted_file).name
                images_dict = init.file_extract_obj.extract_images_docs(
                    file=converted_file,
                    extension=extension+"x",
                    file_name=file_name
                )
                text = init.file_extract_obj.extract_text_docs(converted_file)
                os.remove(converted_file)
                if len(images_dict["images"]) == 0:
                    contains_images = False
                else:
                    contains_images = True
                doc_to_db_and_add_to_kafka(text=text,
                                           file_name=file,
                                           file_to_save=file_to_index,
                                           extension=extension,
                                           images_dict=images_dict,
                                           contains_images=contains_images,
                                           file_dir=new_directory
                                           )
        elif group == "audio":
            target_file = init.file_convert_obj.convert_audio(source_format=extension, file=file_to_index)
            shutil.rmtree(new_directory)
            image_audio_to_db_and_add_to_kafka(file_to_save=target_file,
                                               extension="wav",
                                               file_name=file,
                                               group=group
                                               )
        elif group == "image":
            if extension == "jpg" or extension == "png":
                image_audio_to_db_and_add_to_kafka(file_to_save=file_to_index,
                                                   extension=extension,
                                                   file_name=file,
                                                   rmdir=True,
                                                   to_rmdir=new_directory,
                                                   group=group
                                                   )
            elif extension == "svg":
                target_file = init.file_convert_obj.convert_svg(file=file_to_index)
                shutil.rmtree(new_directory)
                image_audio_to_db_and_add_to_kafka(file_to_save=target_file,
                                                   extension="png",
                                                   file_name=file,
                                                   group=group
                                                   )
        elif group == "video":
            if init.file_check_obj.check_video_audio(file_to_index):
                target_file = init.file_convert_obj.convert_video(source_format=extension, file=file_to_index)
                shutil.rmtree(new_directory)
                image_audio_to_db_and_add_to_kafka(file_to_save=target_file,
                                                   extension="wav",
                                                   file_name=file,
                                                   group=group
                                                   )
            else:
                remove_api(file, "last_audio_file")
                init.send_log_msg("VIDEO WITHOUT AUDIO " + file + " of type last_audio_file")
                shutil.rmtree(new_directory)
    else:
        fake_extension = pathlib.Path(file).suffix
        print("fake extension")
        if fake_extension in globals.FAKE_DOC_IMAGE_EXTENSIONS:
            remove_api(file, "last_doc_image")
            init.send_log_msg("FAKE_FILE " + file + " of type last_doc_image")
        elif fake_extension in globals.FAKE_AUDIO_EXTENSIONS:
            remove_api(file, "last_audio_file")
            init.send_log_msg("FAKE_FILE " + file + " of type last_audio_file")
        shutil.rmtree(new_directory)
