from kafka import KafkaProducer
import sys
import json
import os


SEND_TOPIC_FULL = "IMAGE_RESULTS"
SEND_TOPIC_TEXT = "TEXT"
KAFKA_HOSTNAME = os.getenv("KAFKA_HOSTNAME")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME")
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")
print(KAFKA_HOSTNAME)
producer_obj = KafkaProducer(
    bootstrap_servers=[KAFKA_HOSTNAME + ':' + KAFKA_PORT],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism='PLAIN',
    sasl_plain_username=KAFKA_USERNAME,
    sasl_plain_password=KAFKA_PASSWORD
)


topic = sys.argv[1]
value = sys.argv[2]
print("***************in script 2***********************")
print(topic)
print(value)
producer_obj.send(topic, value=str(value))
producer_obj.flush()
print("sent message")
