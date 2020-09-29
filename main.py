from task import main
import init
import globals
import sys
from Services.YamlParserService import parse


if __name__ == '__main__':
    container_client = init.blob_service_client.get_container_client(container=globals.BLOB_STORAGE_CONTAINER_NAME)
    blob_list = container_client.list_blobs()
    yaml_file = sys.argv[1]
    group_array = parse(yaml_file)
    for blob in blob_list:
        print(blob.name)
        main.delay(blob.name, group_array)
