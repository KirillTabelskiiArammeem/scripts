from confluent_kafka import TopicPartition

topic = 'BeOrders'
group_id = 'test_be_orders_hd_sand'
consumer = self.env['aram.kafka'].get_consumer(group_id)

topic = TopicPartition(topic, 2, 950109)

consumer.assign([topic])
consumer.seek(topic)
message = consumer.poll()

import os
from confluent_kafka import Consumer
from confluent_kafka import TopicPartition

group_id = 'test_be_orders_hd_sand'
consumer_conf = {
            "bootstrap.servers": os.getenv(
                "INTEGRATION_KAFKA_BOOTSTRAP_SERVERS", "broker:29092"
            ),
            "group.id": group_id,
        }

consumer = Consumer(consumer_conf)
topic = TopicPartition('BeOrders', 2, 950109)

consumer.assign([topic])
consumer.seek(topic)
message = consumer.poll()