import email
import datetime
import pytz
import csv
import re


tag = re.compile(r'<.*?>', flags=re.DOTALL)

utc=pytz.UTC

date_to = datetime.datetime(2024, 3, 6,  8, 32).timestamp()
date_from = datetime.datetime(2024, 3, 6,  3, 11).timestamp()


server = env['fetchmail.server'].browse(23)
mail = server.connect()

status, messages = mail.select('INBOX')

total_messages = int(messages[0])

messages_to_check = []

for i in range(total_messages, 0, -1):
    res, msg = mail.fetch(str(i), "(RFC822)")
    message = email.message_from_bytes(msg[0][1])
    date_str = message['Date']
    if date_str.endswith(' (GMT)'):
        date_str = date_str.replace(' (GMT)', '')
    elif date_str.endswith(' (UTC)'):
        date_str = date_str.replace(' (UTC)', '')
    elif date_str.endswith(' (BST)'):
        date_str = date_str.replace(' (BST)', '')
    elif date_str.endswith(' (AST)'):
        date_str = date_str.replace(' (AST)', '')
    elif date_str.endswith(' (PST)'):
        date_str = date_str.replace(' (PST)', '')
    try:
        date = datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    except:
        print(date_str)
        messages_to_check.append(message)
        continue
    date = date.astimezone(utc)
    date_timestamp = date.timestamp()
    if date_timestamp > date_to:
        continue
    if date_timestamp < date_from:
        continue
    print(date, date.fromtimestamp(date_timestamp))
    messages_to_check.append([i, message])

def make_unread(mail, message):
    mail.store(message, '-FLAGS', '\Seen')

def prepare_message(message):
    body = ''
    if message.is_multipart():
        for part in message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    body = part.get_payload(decode=True).decode('"windows-1256"')
                break
    else:
        body = message.get_payload(decode=True).decode()
    body = tag.sub('', body)
    subject = message['Subject']
    date = message['Date']
    sender = message['From']
    return {
        'date': date,
        'subject': subject,
        'body': body,
        'sender': sender
    }

mesgaes_dict = [prepare_message(m) for m in messages_to_check]


file = open('/tmp/messages.csv', 'w')
writer = csv.DictWriter(file, fieldnames=['date', 'sender', 'subject', 'body'])

writer.writerows(mesgaes_dict)

file.close()

res, msg =  mail.fetch('343348', "(RFC822)")
message = email.message_from_bytes(msg[0][1])
flasgs = message['flags']


for message in messages_to_check:
    email = message[1]['From']
    if 'y.khattab@toyou.io' in email or 'Lace.DeJesus@landmarkgroup.com' in email:
        continue
    make_unread(mail, str(message[0]))
    server._cr.commit()
