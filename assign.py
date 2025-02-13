import atexit
import datetime
import logging
import os

from cachetools import cached
from confluent_kafka import DeserializingConsumer, KafkaError, SerializingProducer
from confluent_kafka.schema_registry import Schema, SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.schema_registry.error import SchemaRegistryError
from confluent_kafka.serialization import StringDeserializer, StringSerializer

from odoo import api, models

from odoo.addons.aram_kafka.models.exceptions import SchemaNotFoundException
from odoo.addons.aram_utils.models.exceptions import ToggleDisabledException
from odoo.addons.aram_utils.utils import check_toggle, with_attempts

user = self
self = self.env['aram.kafka']
logger = logging.getLogger("Kafka")

REQUEST_TIMEOUT_MS = int(os.getenv("KAFKA_REQUEST_TIMEOUT_MS", 30000))
bootstrap_servers = os.getenv("INTEGRATION_KAFKA_BOOTSTRAP_SERVERS", "broker:29092")
schema_registry = os.getenv(
    "INTEGRATION_KAFKA_SCHEMA_REGISTRY", "http://schema-registry:8081"
)
schema_registry_client = SchemaRegistryClient({"url": schema_registry})
message_max_bytes = os.getenv(
    "INTEGRATION_KAFKA_PRODUCER_MESSAGE_MAX_BYTES",
    1000012,
)
topic = 'HelpdeskUpdateUserStatus'
schema = self.get_schema_by_topic_name(topic)
avro_serializer = AvroSerializer(
            self.schema_registry_client,
            schema.schema,
            conf={
                "auto.register.schemas": False,
            },
        )
producer_conf = {
            "bootstrap.servers": self.bootstrap_servers,
            "key.serializer": StringSerializer("utf_8"),
            "value.serializer": avro_serializer,
            "message.max.bytes": int(self.message_max_bytes),
            "request.timeout.ms": REQUEST_TIMEOUT_MS,
            "socket.keepalive.enable": True,
            "socket.timeout.ms": REQUEST_TIMEOUT_MS,
            "logger": logger,
        }
producer = SerializingProducer(producer_conf)
producer.poll(0)
producer.produce(
            topic=topic,
            key='1',
            value={'user_id': 1, 'online': True, 'status_work': 1, 'update_user_time_online': False, 'update_average_rating': False},
            on_delivery=self.delivery_report,
        )
producer.flush()