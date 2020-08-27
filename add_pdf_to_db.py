# Use to add images from pdf to db
from mongo_setup import global_init
from models.cache_model import Cache
from models.file_model import *
import shutil
from Services.PdfUtils import PdfUtils
from azure.storage.blob import BlobServiceClient
import os
global_init()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
cache_model_obj = Cache()
pdf_utils_obj = PdfUtils()
image_db_list = []
if __name__ == '__main__':
    """Download a file from azure"""
    file = "text_+_images.pdf"
    blob_client = blob_service_client.get_blob_client(container="test", blob=file)
    with open(file, 'wb') as pdf:
        pdf.write(blob_client.download_blob().readall())
    """Check if file is encrypted or not"""
    if pdf_utils_obj.check(file):
        print("encrypted pdf")
    else:
        text_images_dict = pdf_utils_obj.extract_text_and_images(file)
        text = text_images_dict["text"]
        images = text_images_dict["images"]
        images_folder = text_images_dict["images_folder"]
        """saving pdf to db"""
        with open(file, 'rb') as fd:
            cache_model_obj.file.put(fd)
        cache_model_obj.file_name = file
        cache_model_obj.mime_type = "pdf"
        """saving images to db"""
        for image in images:
            print(image)
            with open(image, 'rb') as fd:
                image_db_list.append(FilesModel(files=fd))
        print(image_db_list)
        """Removing image folder"""
        shutil.rmtree(images_folder)
        cache_model_obj.files = image_db_list
        cache_model_obj.save()

    primary_key_pdf = cache_model_obj.pk

