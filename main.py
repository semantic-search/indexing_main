from task import main
import init
import globals
from Services.YamlParserService import parse
import os


if __name__ == '__main__':
    container_client = init.blob_service_client.get_container_client(container=globals.BLOB_STORAGE_CONTAINER_NAME)
    blob_list = container_client.list_blobs()
    parse(os.path.abspath("config.yaml"))
    for blob in blob_list:
        print(blob.name)
        main.delay(blob.name)
