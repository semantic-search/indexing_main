import redis
from kafka import KafkaConsumer
from kafka import KafkaProducer
import globals
import json
from azure.storage.blob import BlobServiceClient
from db_models.models.cache_model import Cache
from Services.FileConversionService import FileConvert
from Services.FileExtractionService import FileExtract
from Services.FileCheckService import FileCheck

# Redis initialize
redis_obj = redis.StrictRedis(
    host=globals.REDIS_HOSTNAME,
    port=globals.REDIS_PORT,
    password=globals.REDIS_PASSWORD,
    ssl=True
)

# # Kafka initialize
# consumer_obj = KafkaConsumer(
#     globals.RECEIVE_TOPIC,
#     bootstrap_servers=[globals.KAFKA_HOSTNAME + ':' + globals.KAFKA_PORT],
#     auto_offset_reset="earliest",
#     enable_auto_commit=True,
#     group_id="my-group",
#     value_deserializer=lambda x: json.loads(x.decode("utf-8")),
#     security_protocol="SASL_PLAINTEXT",
#     sasl_mechanism='PLAIN',
#     sasl_plain_username=globals.KAFKA_USERNAME,
#     sasl_plain_password=globals.KAFKA_PASSWORD
# )
#
# producer_obj = KafkaProducer(
#     bootstrap_servers=[globals.KAFKA_HOSTNAME + ':' + globals.KAFKA_PORT],
#     value_serializer=lambda x: json.dumps(x).encode("utf-8"),
#     security_protocol="SASL_PLAINTEXT",
#     sasl_mechanism='PLAIN',
#     sasl_plain_username=globals.KAFKA_USERNAME,
#     sasl_plain_password=globals.KAFKA_PASSWORD
# )
# azure blob storage client
blob_service_client = BlobServiceClient.from_connection_string(globals.CONNECTION_STRING)


file_check_obj = FileCheck()
file_extract_obj = FileExtract()
file_convert_obj = FileConvert()

