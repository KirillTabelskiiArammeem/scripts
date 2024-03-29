import atexit
import os
import zipfile
from subprocess import check_call
from psycopg2 import connect, sql, ProgrammingError
from functools import lru_cache
from zipfile import ZipFile

# fmt: off
TABLES_TO_DROP = [
'queue_job', 'queue_job_queue_jobs_to_done_rel', 'queue_job_queue_requeue_job_rel',
#'mail_activity', 'mail_channel_partner', 'mail_compose_message', 'mail_compose_message_ir_attachments_rel', 'mail_compose_message_res_partner_rel', 'mail_followers', 'mail_followers_mail_message_subtype_rel', 'mail_mail', 'mail_mail_res_partner_rel', 'mail_message', 'mail_message_mail_channel_rel', 'mail_message_res_partner_needaction_rel', 'mail_message_res_partner_needaction_rel_mail_resend_message_rel', 'mail_message_res_partner_rel', 'mail_message_res_partner_starred_rel', 'mail_resend_message', 'mail_resend_partner', 'mail_tracking_value', 'message_attachment_rel',
]

WEB_TABLES_TO_DROP = ['website_page']

MAIL_TABLES_TO_DROP = ['mail_activity', "mail_mail", "mail_mail_res_partner_rel",
"mail_message_res_partner_needaction_rel", 'mail_message_res_partner_needaction_rel_mail_resend_message_rel',
'mail_message_mail_channel_rel', 'mail_message_res_partner_rel', 'mail_followers_mail_message_subtype_rel',
'mail_message', 'mail_tracking_value', 'mail_channel_partner', 'mail_compose_message',  'mail_followers',
"mail_message_res_partner_starred_rel", "mail_resend_message", "message_attachment_rel", "survey_mail_compose_message"]

DP_TABLES_TO_DROP = [
    "aram_employee_kpi_statistic", "fleet_vehicle_assignation_log", "rep_onboarding_referral_link", "account_invoice",
    "account_partial_reconcile", "account_move_line", "add_remove_blocking_reason_wizard", "amd_earning_package",
    "amd_rep_cabinet_general_instruction", "storage_file", "amd_earning_tariff", "ir_logging", "ir_property", "amd_orders",
    "amd_calibration_bonus", "amd_motivation_tariff_calibration_table", "amd_motivation_tariff", "fleet_vehicle_odometer",
    "fleet_vehicle", "ir_cron"
]


# fmt: on
@lru_cache(10)
def get_connection():
    conn = connect(
        host="db", port=5432, user="odoo", password="odoo", database="dp"
    )
    atexit.register(conn.close)
    return conn


def run_query(query):
    print(query)
    conn = get_connection()
    with conn.cursor() as cursor:
        query = sql.SQL(query)
        cursor.execute(query)
        conn.commit()
        try:
            return cursor.fetchall()
        except ProgrammingError:
            return []


def get_all_tables():
    return [
        item[0]
        for item in run_query(
            "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public' ",
        )
    ]


def clean_tables():
    tables = ", ".join(TABLES_TO_DROP)
    return run_query(f"TRUNCATE TABLE {tables}")


def delete_from_tables(tables_list):
    query = ';\n'.join([f'DELETE FROM {table}' for table in tables_list])
    return run_query(query)


def clean_mail_tables():
    return delete_from_tables(MAIL_TABLES_TO_DROP)


def clean_web_tables():
    return delete_from_tables(WEB_TABLES_TO_DROP)


def clean_dp_tables():
    return delete_from_tables(DP_TABLES_TO_DROP)

def thin_out_ir_model_data():
    models = ", ".join(f"'{item.replace('_', '.')}'" for item in TABLES_TO_DROP + DP_TABLES_TO_DROP + WEB_TABLES_TO_DROP + MAIL_TABLES_TO_DROP)
    query = f"""
    DELETE FROM ir_model_data
    WHERE model IN ({models})
    """
    run_query(query)


def thin_out_ir_attachments():
    # query = """
    # DELETE FROM ir_attachment
    # WHERE res_model not in ('ir.ui.view', 'ir.ui.menu', 'ir.module.module')
    # """
    query = "DELETE FROM ir_attachment"
    run_query(query)


def thin_out_ir_translation():
    query = "DELETE FROM ir_translation"
    run_query(query)


def clean_view():
    query = """
        DELETE FROM report_layout;
        DELETE FROM ir_ui_view;
        DELETE FROM ir_model_data WHERE model = 'ir.ui.view';
    """
    run_query(query)


def thin_out_users():
    users_partners = run_query(
        "SELECT id, partner_id FROM res_users WHERE write_date <= '2023-07-01' and id not in (1, 2, 122, 212) "
    )
    users = set(str(item[0]) for item in users_partners)
    users = ", ".join(users) or "999999999"
    partners = set(str(item[1]) for item in users_partners)
    partners = ", ".join(partners) or "999999999"
    run_query(
        f"""
    DELETE FROM ir_cron WHERE user_id IN ({users});
    DELETE FROM website WHERE user_id IN ({users});
    DELETE FROM res_users WHERE id IN ({users});
    DELETE FROM res_partner WHERE id in ({partners});
    DELETE FROM ir_model_data WHERE res_id  IN ({users}) AND model = 'res.users';
    DELETE FROM ir_model_data WHERE res_id  IN ({partners}) AND model = 'res.partner';
    DELETE FROM ir_model_data WHERE  model = 'amc.invoice.bank.info';
    """
    )

    run_query(
        f"DELETE FROM res_company WHERE id NOT IN (SELECT company_id FROM res_users);"
    )
    partners = run_query(
        "SELECT id FROM res_partner WHERE id NOT IN (SELECT partner_id FROM res_users) AND id NOT IN (SELECT partner_id FROM  res_company) AND user_id IS NULL"
    )
    partners = set(str(item[0]) for item in partners)
    partners = ", ".join(partners) or "999999999"
    run_query(
        f"""
    DELETE FROM res_partner WHERE id IN ({partners});
    DELETE FROM ir_model_data WHERE res_id IN ({partners}) AND model = 'res.partner';
"""
    )


def backup(path="fixture.sql"):
    os.environ["PGPASSWORD"] = "odoo"
    check_call(
        f"pg_dump --file '{path}' --host '127.0.0.1' --port '5432' --username 'odoo' --format=p 'dp'",
        shell=True,
    )
    with ZipFile(
        f"{path}.zip", "w", compresslevel=9, compression=zipfile.ZIP_BZIP2
    ) as file:
        file.write(path)
    os.remove(path)


def main():
    clean_tables()
    clean_mail_tables()
    clean_web_tables()
    clean_dp_tables()
    thin_out_ir_model_data()
    thin_out_ir_attachments()
    thin_out_users()
    thin_out_ir_translation()
    backup()


if __name__ == "__main__":
    main()
