from task import main
import init
import globals
import sys
from Services.YamlParserService import parse


if __name__ == '__main__':
    blob_meta_list = []
    container_client = init.blob_service_client.get_container_client(container=globals.BLOB_STORAGE_CONTAINER_NAME)
    blob_list = container_client.list_blobs()
    yaml_file = sys.argv[1]
    group_array = parse(yaml_file)
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
                init.redis_obj.set("last_doc_image", file)
            elif group == "video" or group == "audio":
                init.redis_obj.set("last_audio", file)
            main.delay(blob.name, group_array)
