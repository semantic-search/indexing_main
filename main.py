from task import main
import init
import globals
import yaml


if __name__ == '__main__':
    container_client = init.blob_service_client.get_container_client(container=globals.BLOB_STORAGE_CONTAINER_NAME)
    blob_list = container_client.list_blobs()
    with open("config.yaml") as f:
        config_dict = yaml.safe_load(f)
    for blob in blob_list:
        print(blob.name)
        main.delay(blob.name, config_dict)
