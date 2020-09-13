# downloads image from mongo db
from db_models.mongo_setup import global_init
from db_models.models.cache_model import Cache


global_init()

test = Cache.objects.get(pk="5f539d8dd9e279c786ec9a8a")
file = "budlite.jpg"
print(test.mime_type)
"""For downloading single image or audio"""
with open(file, 'wb') as file_to_save:
    file_to_save.write(test.file.read())
"""For downloading all images of pdf"""
#i = 0
# for image in test.files:
#     file = str(i) + ".jpg"
#     with open(file, 'wb') as file_to_save:
#         file_to_save.write(image.file.read())
#     i = i +1