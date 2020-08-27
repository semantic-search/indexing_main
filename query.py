# downloads image from mongo db
from mongo_setup import global_init
from models.cache_model import Cache
from models.file_model import *

global_init()

test = Cache.objects.get(pk="5f4753624bb125ff64aed716")
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
#         file_to_save.write(image.files.read())
#     i = i +1