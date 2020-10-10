from task import main
import init
import globals
import sys
from Services.YamlParserService import parse
import pyfiglet
import requests


if __name__ == '__main__':
    print(pyfiglet.figlet_format(str(globals.STORAGE_PROVIDER) + " BULK FILE INDEXER"))
    blob_meta_list = []
    container_client = init.blob_service_client.get_container_client(container=globals.BLOB_STORAGE_CONTAINER_NAME)
    blob_list = container_client.list_blobs()
    yaml_file = sys.argv[1]
    group_array = parse(yaml_file)
    payload = dict()
    payload["client_id"] = 151515
    print(group_array)
    for blob in blob_list:
        print(blob.name)
        file = blob.name
        content_type = blob.content_settings["content_type"]
        print(content_type)
        mime_dict = init.file_check_obj.check_mime_type(extension=content_type)
        print(mime_dict)
        if mime_dict is None:
            pass
        else:
            group = mime_dict["group"]
            if group == "document" or group == "image" or group == "legacy_document":
                payload["last_file"] = "last_doc_image"
                payload["value"] = file
                """api call to dashboard api"""
                response = requests.request("POST", globals.DASHBOARD_URL,  data=payload)
            elif group == "video" or group == "audio":
                payload["last_file"] = "last_audio"
                payload["value"] = file
                """api call to dashbaord api"""
            main.delay(blob.name, group_array)
