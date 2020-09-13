# Use to add a single image or audio to db
from db_models.mongo_setup import global_init
from db_models.models.cache_model import Cache


if __name__ == '__main__':
    global_init()

    cache_model_obj = Cache()

    """for image files"""
    cache_model_obj.file_name = 'budlite.jpg'
    cache_model_obj.mime_type = "jpg"
    cache_model_obj.is_doc_type = False
    with open('test_files/image1.jpg', 'rb') as fd:
        cache_model_obj.file.put(fd)
    cache_model_obj.save()
#     """for audio files"""
#     cache_model_obj.file_name = 'out.wav'
#     cache_model_obj.mime_type = "wav"
#     with open('mongo-package/test_files/out.wav', 'rb') as fd:
#         file_obj = FileModel(files=fd)
#     cache_model_obj.file = file_obj
#     cache_model_obj.save()
    primary_key_pdf = cache_model_obj.pk

