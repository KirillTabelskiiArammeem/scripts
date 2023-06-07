import atexit
import os
from types import MappingProxyType
from typing import Iterable, List, Literal

import pandas
from cachetools import cached
from dotenv import load_dotenv
from postgres import Postgres
from psycopg2 import errors

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_MCP_PROD_DATABASE = os.getenv("DB_MCP_PROD_DATABASE")
DB_MCP_SAND_DATABASE = os.getenv("DB_MCP_SAND_DATABASE")
DB_CRM_PROD_DATABASE = os.getenv("DB_CRM_PROD_DATABASE")
DB_CRM_SAND_DATABASE = os.getenv("DB_CRM_SAND_DATABASE")
DB_DP_PROD_DATABASE = os.getenv("DB_DP_PROD_DATABASE")
DB_DP_SAND_DATABASE = os.getenv("DB_DP_SAND_DATABASE")
DB_HELPDESK_PROD_DATABASE = os.getenv("DB_HELPDESK_PROD_DATABASE")
DB_HELPDESK_SAND_DATABASE = os.getenv("DB_HELPDESK_SAND_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

PG_DSN_PROD_MCP = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_MCP_PROD_DATABASE}"
)
PG_DSN_SAND_MCP = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_MCP_SAND_DATABASE}"
)
PG_DSN_PROD_CRM = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_CRM_PROD_DATABASE}"
)
PG_DSN_SAND_CRM = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_CRM_SAND_DATABASE}"
)
PG_DSN_PROD_DP = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_DP_PROD_DATABASE}"
)
PG_DSN_SAND_DP = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_DP_SAND_DATABASE}"
)

PG_DSN_PROD_HELPDESK = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_HELPDESK_PROD_DATABASE}"
)
PG_DSN_SAND_HELPDESK = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_HELPDESK_SAND_DATABASE}"
)

MAX_REF_ROWS = 30

DSN_MAP = MappingProxyType(
    {
        "mcp": MappingProxyType({"prod": PG_DSN_PROD_MCP, "sand": PG_DSN_SAND_MCP}),
        "crm": MappingProxyType({"prod": PG_DSN_PROD_CRM, "sand": PG_DSN_SAND_CRM}),
        "dp": MappingProxyType({"prod": PG_DSN_PROD_DP, "sand": PG_DSN_SAND_DP}),
        "helpdesk": MappingProxyType({"prod": PG_DSN_PROD_DP, "sand": PG_DSN_SAND_DP}),
    }
)

SERVICES_TYPE = Literal["mcp", "crm", "dp", 'helpdesk']
ENVS_TYPE = Literal["sand", "prod"]


@cached({})
def get_conn(service: SERVICES_TYPE, env: ENVS_TYPE) -> Postgres:
    conn = Postgres(DSN_MAP[service][env], readonly=(env == "prod"))
    atexit.register(conn.pool.clear)
    return conn


GET_FIELDS = """
select 
    model, 
    ARRAY_AGG("name") as names
from ir_model_fields 
group by model
"""

GET_MODELS = """
select model, count(*) as c
from ir_model_data
group by model 
having count(*) < %(max_ref_rows)s
order by count(*) 
"""


GET_RECORDS = """
select 
    imd.id as imd_id,
    imd.module as module,
    imd.model as model,
    imd.res_id as rec_id,
    imd.name as xml_id, 
    mt.name as org_name
from ir_model_data imd 
left join {model_table} mt on mt.id = imd.res_id
where imd.model = %(model)s
"""

GET_RECORDS_NO_NAME = """
select 
    imd.id as imd_id,
    imd.module as module,
    imd.model as model,
    imd.res_id as rec_id,
    imd.name as xml_id, 
    'no_name' as org_name
from ir_model_data imd 
left join {model_table} mt on mt.id = imd.res_id
where imd.model = %(model)s
"""


FORCE_NO_MAME = ('ir.cron', 'website.page', 'amc.pricing.table', 'amc.slot')

def get_models(service: SERVICES_TYPE) -> Iterable[str]:
    models = get_conn(service, "sand").all(GET_MODELS, max_ref_rows=MAX_REF_ROWS)
    return [model.model for model in models if model.model != "ir_model_data"]


def get_fields(service: SERVICES_TYPE) -> dict:
    fields = get_conn(service, "sand").all(GET_FIELDS)

    fields = {field.model: set(field.names) for field in fields}
    for field in FORCE_NO_MAME:
        fields[field] = set()
    return fields


def get_records(conn: Postgres, model: str, names: bool = True) -> List[dict]:
    query = GET_RECORDS if names else GET_RECORDS_NO_NAME
    table = model.replace(".", "_")
    try:
        records = conn.all(
            query.format(
                model_table=table,
            ),
            model=model,
        )
    except errors.UndefinedTable:
        print(f"{model=} {table=}. Table does not exist")
        records = []
    return [record._asdict() for record in records]


def get_records_df(
    service: SERVICES_TYPE, env: ENVS_TYPE, model: str, names: bool
) -> pandas.DataFrame:
    df = pandas.DataFrame(get_records(get_conn(service, env), model, names))
    if df.empty:
        df = pandas.DataFrame(
            columns=["imd_id", "module", "model", "rec_id", "xml_id", "org_name"]
        )
    return df


SERVICE: SERVICES_TYPE = "helpdesk"


def main():
    fields = get_fields(SERVICE)
    models = get_models(SERVICE)
    for model in models:
        print(model)
        if model not in fields:
            print(f'{model=} not in fields')
            continue
        names = "name" in fields[model]
        sand_df = get_records_df(SERVICE, "sand", model, names)
        prod_df = get_records_df(SERVICE, "prod", model, names)

        if names:
            compare_name = sand_df.merge(
                prod_df, how="outer", on=["org_name"], suffixes=("_sand", "_prod")
            )
            diff_name = compare_name[
                compare_name["xml_id_sand"] != compare_name["xml_id_prod"]
            ]
        else:
            diff_name = pandas.DataFrame()

        compare_xml_id = sand_df.merge(
            prod_df, how="outer", on=["xml_id"], suffixes=("_sand", "_prod")
        )
        diff_xml_id = compare_xml_id[
            compare_xml_id["org_name_sand"] != compare_xml_id["org_name_prod"]
        ]

        if not diff_name.empty or not diff_xml_id.empty:
            print(model)
            if not diff_name.empty:
                diff_name.to_csv(os.path.join("csv", SERVICE, f"diff_name_{model}.csv"))
            if not diff_xml_id.empty:
                diff_xml_id.to_csv(
                    os.path.join("csv", SERVICE, f"diff_xml_id_{model}.csv")
                )


if __name__ == "__main__":
    main()
