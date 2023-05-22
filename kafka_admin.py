import os
from confluent_kafka.admin import AdminClient, NewTopic


client = AdminClient({'bootstrap.servers':  os.getenv("INTEGRATION_KAFKA_BOOTSTRAP_SERVERS")})

topics = client.list_topics().topics

crm_topics = {key: value for key, value in topics.items() if key.startswith("CRM")}

topics_to_delete = list(crm_topics.keys())
topics_to_create = [NewTopic(topic_name, num_partitions=len(topic_meta.partitions), replication_factor=3) for topic_name, topic_meta in crm_topics.items()]

client.delete_topics(topics_to_delete)
client.create_topics(topics_to_create)


topics2 = client.list_topics().topics
crm_topics2 = {key: value for key, value in topics.items() if key.startswith("CRM")}
