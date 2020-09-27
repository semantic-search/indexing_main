from task import main
import init


container_client= init.blob_service_client.get_container_client(container="test")
blob_list = container_client.list_blobs()
for blob in blob_list:
    print(blob.name)
    main.delay(blob.name)