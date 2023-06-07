import atexit
import os
from typing import Iterable, Literal, List
from types import MappingProxyType

import pandas
from cachetools import cached

from postgres import Postgres
from dotenv import load_dotenv


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_MCP_PROD_DATABASE = os.getenv("DB_MCP_PROD_DATABASE")
DB_MCP_SAND_DATABASE = os.getenv("DB_MCP_SAND_DATABASE")
DB_CRM_PROD_DATABASE = os.getenv("DB_CRM_PROD_DATABASE")
DB_CRM_SAND_DATABASE = os.getenv("DB_CRM_SAND_DATABASE")
DB_DP_PROD_DATABASE = os.getenv("DB_DP_PROD_DATABASE")
DB_DP_SAND_DATABASE = os.getenv("DB_DP_SAND_DATABASE")
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

MAX_REF_ROWS = 30

DSN_MAP = MappingProxyType(
    {
        "mcp": MappingProxyType({"prod": PG_DSN_PROD_MCP, "sand": PG_DSN_SAND_MCP}),
        "crm": MappingProxyType({"prod": PG_DSN_PROD_CRM, "sand": PG_DSN_SAND_CRM}),
        "dp": MappingProxyType({"prod": PG_DSN_PROD_DP, "sand": PG_DSN_SAND_DP}),
    }
)

SERVICES_TYPE = Literal["mcp", "crm", "dp"]
ENVS_TYPE = Literal["sand", "prod"]


@cached({})
def get_conn(service: SERVICES_TYPE, env: ENVS_TYPE) -> Postgres:
    conn = Postgres(DSN_MAP[service][env], readonly=(env == "prod"))
    atexit.register(conn.pool.clear)
    return conn


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


def get_models(service: SERVICES_TYPE) -> Iterable[str]:
    models = get_conn(service, "sand").all(GET_MODELS, max_ref_rows=MAX_REF_ROWS)
    return [
        model.model
        for model in models
        if model.model
        not in {
            "mail.message",
            "resource.calendar",
            "digest.digest",
            "digest.tip",
            "website.page",
            "ir.actions.act_url",
            "utm.campaign",
            "ir.actions.report",
            "mail.alias",
            "report.layout",
            "utm.source",
            "ir.actions.client",
            "utm.medium",
            "ir.actions.act_window.view",
            "ir.config_parameter",
            "ir.cron",
            "ir.actions.server",
            "amc.pricing.table",
            "survey.survey",
            "maintenance.team",
            "amc.slot",
            "survey.page",
            "amc.charges.section",
            "auth.oauth.provider",
            "maintenance.stage",
            "amc.res.partner.role",
            "amc.res.patner.role",
            "amc.category.price.group",
            "amc.operation.area.price.group",
            "survey.question",
            "account.fiscal.position.tax.template",
            "amc.partner.charge.type",
            "survey.label",
        }
    ]


def get_records(conn: Postgres, model: str) -> List[dict]:
    table = model.replace(".", "_")
    return [
        record._asdict()
        for record in conn.all(
            GET_RECORDS.format(
                model_table=table,
            ),
            model=model,
        )
    ]


def get_records_df(
    service: SERVICES_TYPE, env: ENVS_TYPE, model: str
) -> pandas.DataFrame:
    return pandas.DataFrame(get_records(get_conn(service, env), model))


SERVICE: SERVICES_TYPE = "dp"


def main():
    models = get_models(SERVICE)
    for model in models:
        sand_df = get_records_df(SERVICE, "sand", model)
        prod_df = get_records_df(SERVICE, "prod", model)
        compare_name = sand_df.merge(
            prod_df, how="outer", on=["org_name"], suffixes=("_sand", "_prod")
        )
        diff_name = compare_name[
            compare_name["xml_id_sand"] != compare_name["xml_id_prod"]
        ]

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
