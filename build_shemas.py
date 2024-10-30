
import glob
import json
DIR = '/home/kirill/aram/devops/kafka-topics-configs/schema-registry/_schemas/backend'
schemas_files = glob.glob(f'{DIR}/*/*.avsc')
print(schemas_files)

output = {

}

for schemas_file in schemas_files:
    with open(schemas_file) as f:
        schema = json.load(f)
        topic = schema['name']
        output[topic] = schema

with open('schemas.json', 'w') as f:
    json.dump(output, f, indent=4)
