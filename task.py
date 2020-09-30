import init
import os
import shutil
from pathlib import Path
from task_worker.celery import celery_app
from task_utils.download_file_from_storage import azure_blob_storage_download
from task_utils.image_or_audio_add_to_db import image_audio_to_db_and_add_to_kafka
from task_utils.document_add_to_db import doc_to_db_and_add_to_kafka
from task_utils.populator import populate_lists


@celery_app.task()
def main(file, group_array):
    populate_lists(group_array)
    downloaded_blob_info = azure_blob_storage_download(file)
    download_file = downloaded_blob_info["file"]
    new_directory = downloaded_blob_info["directory"]
    mime_dict = init.file_check_obj.check_mime_type(file=download_file)
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
            elif extension == "docx" or \
                    extension == "pptx" or \
                    extension == "xlsx" or \
                    extension == "odt" or \
                    extension == "epub":
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
                                               file_name=file,
                                               group=group
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
            if init.file_check_obj.check_video_audio(download_file):
                target_file = init.file_convert_obj.convert_video(source_format=extension, file=download_file)
                shutil.rmtree(new_directory)
                image_audio_to_db_and_add_to_kafka(file_to_save=target_file,
                                                   extension="wav",
                                                   file_name=file,
                                                   group=group
                                                   )
            else:
                shutil.rmtree(new_directory)
    else:
        shutil.rmtree(new_directory)
