import os
import re
import psycopg2
import base64

IMG_REGEX = re.compile(r'<img src="data:image/[^;]+;base64,[^"]+"[^>]*>')
EXTENSION_REGEX = re.compile(r'image/([^;]+);base64')
BASE64_REGEX = re.compile(r'base64,([^"]+)')


PASSWORD = os.getenv('PG_PASSWORD')
TICKET_ID = 41322263
conn = psycopg2.connect(
    dbname='odoo_am_helpdesk_12_prod',
    user='k.tabelskii',
    password=PASSWORD,
    host='gw-erp.net.amhub.org')

cur = conn.cursor()
# cur = env.cr
cur.execute(f'SELECT description FROM helpdesk_ticket WHERE id = {TICKET_ID}')
description = cur.fetchone()[0]
with open('ticket_description.txt', 'w') as f:
    f.write(description)

#description = open('ticket_description.txt').read()
conn.commit()
# env.cr.commit()
for i, img in enumerate(IMG_REGEX.findall(description)):
    base64_data = BASE64_REGEX.search(img).groups()[0]
    img_bytes = base64.b64decode(base64_data)
    extension = EXTENSION_REGEX.search(img).groups()[0]
    with open(f'img_{i}.{extension}', 'wb') as f:
        f.write(img_bytes)
description = IMG_REGEX.sub("", description)

# cur.execute(f'UPDATE helpdesk_ticket SET description = %s WHERE id = {TICKET_ID}', (description,))
# env.cr.commit()
# conn.commit()
# conn.close()
