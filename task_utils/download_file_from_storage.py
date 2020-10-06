import os
import init
import globals
import uuid


def download_blob(provider, blob_to_download):
    if provider == "Azure":
        blob_client = init.blob_service_client.get_blob_client(container=globals.BLOB_STORAGE_CONTAINER_NAME,
                                                               blob=blob_to_download)
        new_directory = "Downloads/" + str(uuid.uuid4()) + "/"
        os.mkdir(new_directory)
        download_file = new_directory + str(blob_to_download)
        with open(download_file, 'wb') as file_obj:
            file_obj.write(blob_client.download_blob().readall())
        downloaded_blob_info = {
            "file": download_file,
            "directory": new_directory
        }
        return downloaded_blob_info
