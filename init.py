import logging
from logstash_async.handler import AsynchronousLogstashHandler
import globals
from azure.storage.blob import BlobServiceClient
from Services.FileConversionService import FileConvert
from Services.FileExtractionService import FileExtract
from Services.FileCheckService import FileCheck

# azure blob storage client
blob_service_client = BlobServiceClient.from_connection_string(globals.CONNECTION_STRING)
# file services object
file_check_obj = FileCheck()
file_extract_obj = FileExtract()
file_convert_obj = FileConvert()

# logger
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)

# Get you a test logger
logger = logging.getLogger('python-logstash-logger')
# Set it to whatever level you want - default will be info
logger.setLevel(logging.DEBUG)
# Create a handler for it
async_handler = AsynchronousLogstashHandler(
    globals.LOGGER_SERVER_HOST,
    int(globals.LOGGER_SERVER_PORT),
    database_path=None
)
# Add the handler to the logger
logger.addHandler(async_handler)


def send_log_msg(msg, error=False):
    msg = "INDEXING_MAIN " + msg
    if error:
        logger.error(msg)
    else:
        logger.info(msg)
