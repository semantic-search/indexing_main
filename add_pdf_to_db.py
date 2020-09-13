# Use to add images from pdf to db
from db_models.mongo_setup import global_init
from db_models.models.file_model import FilesModel
import shutil
import init

global_init()



image_db_list = []
if __name__ == '__main__':
    """Download a file from azure"""
    file = "text_+_images.pdf"
    blob_client = init.blob_service_client.get_blob_client(container="test", blob=file)
    with open(file, 'wb') as pdf:
        pdf.write(blob_client.download_blob().readall())
    """Check if file is encrypted or not"""
    if init.file_check_obj.check_pdf_encrypted(file):
        print("encrypted pdf")
    else:
        text_images_dict = init.file_extract_obj.extract_text_and_images(file)
        text = text_images_dict["text"]
        images = text_images_dict["images"]
        images_folder = text_images_dict["images_folder"]
        """saving pdf to db"""
        with open(file, 'rb') as fd:
            init.cache_model_obj.file.put(fd)
        init.cache_model_obj.file_name = file
        init.cache_model_obj.mime_type = "pdf"
        """saving images to db"""
        for image in images:
            print(image)
            with open(image, 'rb') as fd:
                image_db_list.append(FilesModel(file=fd))
        print(image_db_list)
        """Removing image folder"""
        shutil.rmtree(images_folder)
        init.cache_model_obj.files = image_db_list
        init.cache_model_obj.is_doc_type = True
        init.cache_model_obj.save()

    primary_key_pdf = init.cache_model_obj.pk

