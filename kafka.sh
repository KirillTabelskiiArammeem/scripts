docker-compose up -d zookeeper
sleep 5
docker-compose up -d broker
sleep 5

docker-compose up -d schema-registry
sleep 1

docker-compose up -d kafka-ui
sleep 1
