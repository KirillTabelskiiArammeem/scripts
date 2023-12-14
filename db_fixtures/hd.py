import atexit
import os
import zipfile
from subprocess import check_call
from psycopg2 import connect, sql, ProgrammingError
from functools import lru_cache
from zipfile import ZipFile

# fmt: off
TABLES_TO_DROP = ['account_analytic_account', 'account_analytic_distribution', 'account_analytic_line', 'account_analytic_line', 'account_analytic_line_tag_rel', 'amh_agent_idle', 'amh_chat_conversations', 'amh_nontime_refund_missed_item_quantity', 'amh_nontime_refund_missed_item_quantity', 'amh_nontime_refund_missed_item_quantity_mixin', 'amh_rating', 'amh_refund_transaction', 'amh_refund_transaction_aram_send_transaction_to_be_wizard_rel', 'amh_ticket_reassign_from_to_users_count', 'amh_ticket_time_between_stages', 'amh_transaction', 'amh_user_assign_history', 'amh_users_time_online', 'aram_cancel_order_wizard', 'aram_cancel_order_wizard_aram_cancel_reason_rel', 'aram_confirmation_pos_off', 'aram_helpdesk_ticket_amt_helpdesk_ticket_rel', 'aram_helpdesk_ticket_helpdesk_ticket_rel', 'aram_send_transaction_to_be_wizard', 'helpdesk_tag_helpdesk_ticket_rel', 'helpdesk_ticket', 'helpdesk_ticket_missing_items', 'helpdesk_ticket_missing_options', 'ir_logging',
'mail_activity', 'mail_channel_partner', 'mail_compose_message', 'mail_compose_message_ir_attachments_rel', 'mail_compose_message_res_partner_rel', 'mail_followers', 'mail_followers_mail_message_subtype_rel', 'mail_mail', 'mail_mail_res_partner_rel', 'mail_message', 'mail_message_mail_channel_rel', 'mail_message_res_partner_needaction_rel', 'mail_message_res_partner_needaction_rel_mail_resend_message_rel', 'mail_message_res_partner_rel', 'mail_message_res_partner_starred_rel', 'mail_resend_message', 'mail_resend_partner', 'mail_tracking_value', 'message_attachment_rel',
'project_favorite_user_rel', 'project_project', 'project_tags_project_task_rel', 'project_task', 'project_task_type_rel', 'queue_job', 'queue_job_queue_jobs_to_done_rel', 'queue_job_queue_requeue_job_rel', 'rating_rating', 'recommended_action', 'recv_customer',
'recv_representative_rep_cohort_rel',
'amh_ticket_quick_create_ticket','recv_digital_order', 'recv_digital_order_line', 'recv_digital_order_state_history', 'recv_digital_product', 'recv_order', 'recv_order_ext', 'recv_order_line', 'recv_order_line_refund', 'recv_order_recv_representative_rel', 'recv_order_state_history', 'recv_product_attribute_value_transaction', 'recv_product_attribute_value_transaction_refund', 'recv_representative', 's3_files', "recv_subscription", "recv_customer_subscription", "aram_unhold_transaction_to_be_wizard", "amh_refund_transaction_aram_unhold_transaction_to_be_wizard_rel"]
# fmt: on


@lru_cache(10)
def get_connection():
    conn = connect(
        host="db", port=5432, user="odoo", password="odoo", database="helpdesk"
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


def thin_out_ir_model_data():
    models = ", ".join(f"'{item.replace('_', '.')}'" for item in TABLES_TO_DROP)
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
        "SELECT id, partner_id FROM res_users WHERE write_date <= '2023-07-01' and id not in (1, 2, 212) "
    )
    users = set(str(item[0]) for item in users_partners)
    users = ", ".join(users) or "999999999"
    partners = set(str(item[1]) for item in users_partners)
    partners = ", ".join(partners) or "999999999"
    run_query(
        f"""
    DELETE FROM amh_team WHERE supervisor_id IN ({users});
    DELETE FROM ir_cron WHERE user_id IN ({users});
    DELETE FROM website WHERE user_id IN ({users});
    DELETE FROM aram_autoassign_config WHERE agent IN ({users});
    DELETE FROM res_users WHERE id IN ({users});
    DELETE FROM res_partner WHERE id in ({partners});
    DELETE FROM ir_model_data WHERE res_id  IN ({users}) AND model = 'res.users';
    DELETE FROM ir_model_data WHERE res_id  IN ({partners}) AND model = 'res.partner';
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
    DELETE FROM ir_model_data WHERE res_id IN ({partners}) AND model = 'res_partner';
"""
    )


def backup(path="fixture.sql"):
    os.environ["PGPASSWORD"] = "odoo"
    check_call(
        f"pg_dump --file '{path}' --host '127.0.0.1' --port '5432' --username 'odoo' --format=p 'helpdesk'",
        shell=True,
    )
    with ZipFile(
        f"{path}.zip", "w", compresslevel=9, compression=zipfile.ZIP_BZIP2
    ) as file:
        file.write(path)
    os.remove(path)


def main():
    clean_tables()
    thin_out_ir_model_data()
    thin_out_ir_attachments()
    thin_out_users()
    thin_out_ir_translation()
    backup()


if __name__ == "__main__":
    main()
