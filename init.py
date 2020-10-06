import redis
import globals
from azure.storage.blob import BlobServiceClient
from Services.FileConversionService import FileConvert
from Services.FileExtractionService import FileExtract
from Services.FileCheckService import FileCheck


# Redis initialize
redis_obj = redis.StrictRedis(
    host=globals.REDIS_HOSTNAME,
    port=globals.REDIS_PORT,
    password=globals.REDIS_PASSWORD,
    ssl=False
)


# azure blob storage client
blob_service_client = BlobServiceClient.from_connection_string(globals.CONNECTION_STRING)
# file services object
file_check_obj = FileCheck()
file_extract_obj = FileExtract()
file_convert_obj = FileConvert()

