import globals
from kafka import KafkaProducer
import sys
import json

producer_obj = KafkaProducer(
    bootstrap_servers=[globals.KAFKA_HOSTNAME + ':' + globals.KAFKA_PORT],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism='PLAIN',
    sasl_plain_username=globals.KAFKA_USERNAME,
    sasl_plain_password=globals.KAFKA_PASSWORD
)



topic = sys.argv[1]
value = sys.argv[2]
print("***************in script 2***********************")
print(topic)
print(value)
producer_obj.send(topic, value=str(value))
producer_obj.flush()
print("sent message")
