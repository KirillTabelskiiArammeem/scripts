import psycopg2
import os
import atexit
from abc import ABC, abstractmethod

CON = None

class Field:
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
    def __init__(self, name, ttype, required, relation_table, column1, column2, odoo_model_name, table, number=None):
        self.name = name
        self.ttype = ttype
        self.required = required
        self.relation_table = relation_table
        self.column1 = column1
        self.column2 = column2
        self.number = number
        self.odoo_model_name = odoo_model_name
        self.table = table
        self.name_go = None
        self.type_go = None
        self.proto_type = None
        self.column_name = None
        self.join_table_query = None
        self.group_by = None
        self.set_go_field_name()
        self.set_proto_type()
        self.set_go_type()
        self.set_column_name()
        self.set_join_table()
        self.set_group_by()

    def set_go_field_name(self):
        if "_" not in self.name:
            self.name_go = self.name[0].upper() + self.name[1:]
        self.name_go = self.name.replace("_", " ").title().replace(" ", "")

    def set_proto_type(self):
        proto_type = self.ODOO_2_PROTO.get(self.ttype, "string")
        optional = "" if self.required else "optional "
        if not proto_type.startswith("repeated") and not self.required:
            proto_type = f'{optional}{proto_type}'
        self.proto_type = proto_type

    def set_go_type(self):
        type_go = self.ODOO_2_GO.get(self.ttype, "string")
        optional = "" if self.required else "*"
        if not type_go.startswith("[]") and not self.required:
            type_go = f'{optional}{type_go}'
        self.type_go = type_go

    def set_column_name(self):
        if self.ttype == "many2many":
            self.column_name = f"""array_agg("{self.relation_table}"."{self.column2}") as "{self.name}" """
        elif self.name == "external_id":
            self.column_name = f""" CONCAT("ir_model_data"."module", '.', "ir_model_data"."name") as "external_id" """
        else:
            self.column_name = f""" "{self.table}"."{self.name}" """

    def set_join_table(self):
        if self.ttype == "many2many":
            self.join_table_query = f"""LEFT JOIN {self.relation_table} ON "{self.relation_table}"."{self.column1}" = "{self.column1}" """
        elif self.name == "external_id":
            self.join_table_query = f"""LEFT JOIN ir_model_data ON "{self.table}"."id" = "ir_model_data"."res_id" AND "ir_model_data"."model" = '{self.odoo_model_name}'"""

    def set_group_by(self):
        if not self.ttype == "many2many":
            self.group_by = f""" "{self.table}"."{self.name}" """

        if self.name == "external_id":
            self.group_by = """CONCAT("ir_model_data"."module", '.', "ir_model_data"."name")"""

class BaseModel(ABC):

    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

    @abstractmethod
    def dump(self) -> str:
        pass


class ProtoModel(BaseModel):

    def dump(self) -> str:
        return f"message {self.name} {{\n" + "\n".join(f"\t{field.proto_type} {field.name_go} = {field.number};" for field in self.fields) + "\n}"


class GoModel(BaseModel):
    def dump(self) -> str:
        return f"type {self.name} struct {{\n" + "\n".join(f"\t{field.name_go} {field.type_go}" for field in self.fields) + "\n}"


class ConverterModelToReply(BaseModel):
    CONVERT_MAP = {
        "datetime": lambda model_name, value: f"timeToPb({model_name}.{value})",
        "default": lambda model_var, value: f"{model_var}.{value}",
    }
    def __init__(self, name, fields, reply_model_name):
        super().__init__(name, fields)
        self.reply_model_name = reply_model_name

    def dump(self) -> str:
        model_var = self.name.lower()
        fields_str = ",\n\t\t".join(f'{field.name_go}: {self.CONVERT_MAP.get(field.ttype, self.CONVERT_MAP["default"])(model_var, field.name_go)}' for field in self.fields)
        return (f"func {model_var}To{self.reply_model_name}({model_var} *models.{self.name}) *application.{self.reply_model_name} {{\n"
                f"\treturn &application.{self.reply_model_name}{{\n"
                f"\t\t{fields_str},\n"
                f"\t}}\n}}")




class SelectById(BaseModel):

    def dump(self) -> str:
        columns = ", ".join(field.column_name for field in self.fields)
        join_tables = "\n".join(set(field.join_table_query for field in self.fields if field.join_table_query))
        where = f"WHERE {self.fields[0].column_name} = ?"
        group_by = ", ".join(set(field.group_by for field in self.fields if field.group_by))
        if group_by:
            group_by = f"GROUP BY {group_by}"
        return f"SELECT \n\t{columns} \nFROM \n\t{self.name} \n{join_tables}\n{where} \n{group_by}"




def get_conn():
    global CON
    if CON:
        return CON
    conn = psycopg2.connect(
        dbname="odoo_am_helpdesk_12_prod_ro",
        user="k.tabelskii",
        password=os.getenv("ODOO_DB_PASSWORD"),
        host="gw-erp.net.amhub.org",
        port="5432",
    )
    atexit.register(conn.close)
    CON = conn
    return conn

def get_fields(odoo_model_name: str, table: str, add_external_id: bool) -> list[Field]:
    with get_conn().cursor() as cursor:
        cursor.execute(f"select name, ttype, required, relation_table, column1, column2  from ir_model_fields where model = '{odoo_model_name}' and store = true and name != 'id' order by id")
        prefix = [Field('id', 'integer', True, None, None, None, odoo_model_name, table)]
        if add_external_id:
            prefix.append(Field('external_id', 'char', False, None, None, None, odoo_model_name, table))
        fields = [*prefix, *(Field(*item, odoo_model_name, table) for item in cursor.fetchall() if item[1] != "one2many")]
        for i, field in enumerate(fields, 1):
            field.number = i
        return fields


def main():
    fields = get_fields("helpdesk.ticket", "helpdesk_ticket", True)
    proto = ProtoModel("GetTicketReply", fields).dump()
    model = GoModel("Ticket", fields).dump()
    conv = ConverterModelToReply("Ticket", fields, "GetTicketReply").dump()
    query = SelectById("helpdesk_ticket", fields).dump()
    print(query)
#     print(f"""
# #####################################################################
#     PROTO:
# {proto}
#     \n\n\n
#     MODEL:
# {model}
#     \n\n\n
#     CONVERTER:
# {conv}
#     \n\n\n
#     QUERY:
# {query}
# #     """)


if __name__ == '__main__':
    main()