import psycopg2
import os
import atexit
model_name = "helpdesk.ticket"

CON = None

ODOO_2_PROTO = {
    "many2one": 'int32',
    "one2many": 'repeated int32',
    "char": 'string',
    "text": 'string',
    "integer": 'int32',
    "float": 'float',
    "boolean": 'bool',
    "datetime": "google.protobuf.Timestamp",
    "many2many": 'repeated int32',
}

ODOO_2_GO = {
    "many2one": 'int32',
    "one2many": '[]int32',
    "char": 'string',
    "text": 'string',
    "integer": 'int32',
    "float": 'float32',
    "boolean": 'bool',
    "datetime": "time.Time",
    "many2many": '[]int32',
}

def get_conn():
    global CON
    if CON:
        return CON
    conn = psycopg2.connect(
        dbname="odoo_am_helpdesk_12_sand",
        user="k.tabelskii",
        password=os.getenv("ODOO_DB_PASSWORD"),
        host="gw-erp-stg.net.amhub.org",
        port="5432",
    )
    atexit.register(conn.close)
    CON = conn
    return conn

def get_fields(model_name):
    with get_conn().cursor() as cursor:
        cursor.execute(f"select name, ttype, required from ir_model_fields imf where model = '{model_name}' and store = true and name != 'id' order by id")
        return cursor.fetchall()

def field_name_to_go(name):
    return name.replace("_", " ").title().replace(" ", "")

def generate_proto(name, external_id, fields):
    rows = [
        f"message {name} {{",
        f"\tstring id = 1;",
    ]
    i = 1
    if external_id:
        i += 1
        rows.append(f"\toptional string external_id = {i};")

    for field in fields:
        if field[1] == "one2many":
            continue
        i += 1
        optional = "" if field[2] else "optional "
        field_type = ODOO_2_PROTO.get(field[1], "string")
        if not field_type.startswith("repeated") and not field[2]:
            field_type = f'{optional}{field_type}'
        rows.append(f"\t{field_type} {field[0]} = {i};")
    rows.append("}")

    return '\n'.join(rows)


def generate_model(name, external_id, fields):
    rows = [
        f"type {name} struct {{",
        f"\tId int32",
    ]
    if external_id:
        rows.append(f"\tExternalId *string")
    for field in fields:
        if field[1] == "one2many":
            continue
        field_type = ODOO_2_GO.get(field[1], "string")
        optional = "" if field[2] else "*"
        if not field_type.startswith("[]") and not field[2]:
            field_type = f'{optional}{field_type}'
        field_name = field_name_to_go(field[0])
        rows.append(f"\t{field_name} {field_type}")
    rows.append("}")
    return '\n'.join(rows)


def main():
    fields = get_fields(model_name)
    proto = generate_proto("GetTicketReply", True, fields)
    model = generate_model("Ticket", True, fields)
    print(proto)
    print(model)


if __name__ == '__main__':
    main()