import json

TYPE_KEYS = {'string', 'boolean', 'com.am.avro.catalog.product.AvroProductMediaType', 'long', 'com.am.avro.catalog.product.AvroProductNameLang', 'com.am.avro.catalog.pos.AvroPointOfSalesNameLang', 'com.am.avro.catalog.pos.Type',
             'com.am.avro.catalog.product.AvroProductPosPK'}

def parse(data):
    for key, value in data.items():

        if not isinstance(value, dict):
            data[key] = value
        elif TYPE_KEYS.intersection(value.keys()):
            for type_key in TYPE_KEYS.intersection(value.keys()):
                data[key] = value[type_key]
                if isinstance(data[key], dict):
                    parse(data[key])
        elif 'array' in value:

            for item in value['array']:
                if isinstance(item, dict):
                    parse(item)
            data[key] = value['array']
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    parse(item)

        else:
            parse(value)




messages = json.load(open('dev_files/fixtures/kafka_init_messages.json', 'r'))





for message in messages:
    message = message['message']
    parse(message)
    print(message)
    if 'array' in message:
        print(message)
print(json.dumps(messages))

