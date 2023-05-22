import os

import pandas
from psycopg2 import connect, sql, ProgrammingError
from csv import DictWriter
from functools import lru_cache
import atexit

password = os.getenv("PASSWORD")
prod_db = "odoo_am_helpdesk_12_prod_ro"
preprod_db = "odoo_am_helpdesk_12_preprod"

@lru_cache(10)
def get_connection(database):
    conn = connect(
        host="gw-erp.net.amhub.org", port=5432, user="k.tabelskii", password=password, database=database
    )
    atexit.register(conn.close)
    return conn


def run_query(query, database):
    print(query)
    conn = get_connection(database)
    with conn.cursor() as cursor:
        query = sql.SQL(query)
        cursor.execute(query)
        conn.commit()
        try:
            return cursor.fetchall()
        except ProgrammingError as er:
            print(er)
            return []

def table_filter(table_name):
    if table_name.startswith("ir_"):
        return False
    if table_name.startswith("queue"):
        return False
    if table_name.startswith("mail_"):
        return False
    return table_name not in {"ir_model_data", "helpdesk_ticket", "recv_order", "recv_order_line", "recv_subscription"}
def get_dictionary_tables(database):

    all_tables = run_query(
        "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public' ",
        database,
    )
    all_tables = (table[0] for table in all_tables)
    for table_name in filter(table_filter, all_tables):
        table_data = run_query(f"SELECT count(*) FROM {table_name}", database)
        if 0 < table_data[0][0] < 1000:
            yield table_name


DICTS = [
    'amh_autorefund_case', 'amh_channel', 'amh_city', 'amh_confirm_resend_voucher_code_message_wizard', 'amh_initiator',
    'amh_initiator_helpdesk_ticket_type_rel', 'amh_nontime_compensation', 'amh_nontime_refund_reason',
    'amh_nontime_refund_reason_scenario', 'amh_order_state', 'amh_order_state_aram_cancel_reason_rel',
    'amh_order_state_helpdesk_ticket_type_rel', 'amh_order_type', 'amh_order_type_amh_ticket_type_group_rel',
    'amh_order_type_helpdesk_ticket_type_rel', 'amh_quality_reason', 'amh_quality_reason_recommended_message_rel',
    'amh_refund_transaction_aram_send_transaction_to_be_wizard_rel', 'amh_responsibility',
    'amh_responsibility_description', 'amh_service_type', 'amh_service_type_aram_cancel_reason_rel', 'amh_team',
    'amh_team_res_users_rel', 'amh_ticket_assign_multiple_tickets', 'amh_ticket_confirm_wizard',
    'amh_ticket_move_to_stage_tickets', 'amh_ticket_type_group', 'amh_transaction_balance_type', 'amh_transaction_reason',
    'amh_transaction_reason_amh_transaction_type_rel', 'amh_transaction_type', 'amh_user_last_assign', 'amwc_reason',
    'aram_agent_status', 'aram_autoassign_config', 'aram_autoassign_config_aram_ticket_priority_rel',
    'aram_autoassign_config_customer_tier_rel', 'aram_cancel_order_wizard', 'aram_cancel_reason',
    'aram_chat_bot_cancel_key', 'aram_chat_bot_cancel_reason', 'aram_customer_language',
    'aram_helpdesk_ticket_amt_helpdesk_ticket_rel', 'aram_helpdesk_ticket_helpdesk_ticket_rel', 'aram_merchant',
    'aram_send_transaction_to_be_wizard', 'aram_ticket_priority', 'base_import_import', 'base_import_mapping',
    'customer_scenario', 'customer_scenario_settings', 'customer_tier', 'customer_tier_settings', 'digest_digest',
    'digest_tip', 'digest_tip_res_users_rel', 'document_page', 'document_page_history', 'fault', 'fault_item',
    'fault_type', 'forum_forum', 'forum_post_reason', 'gamification_badge', 'gamification_badge_user',
    'gamification_challenge', 'gamification_challenge_line', 'gamification_goal', 'gamification_goal_definition',
    'helpdesk_account_manager_resolution', 'helpdesk_action_taken', 'helpdesk_stage', 'helpdesk_team',
    'helpdesk_team_res_users_rel', 'helpdesk_team_slack_channel_rel', 'helpdesk_ticket_type', 'hr_department',
    'hr_employee', 'iap_account', 'im_livechat_channel', 'im_livechat_channel_im_user', 'message_type',
    'muk_autovacuum_rules', 'order_type_names_order_status_rel', 'project_favorite_user_rel', 'project_project',
    'project_tags', 'project_tags_project_task_rel', 'project_task', 'project_task_type', 'project_task_type_rel',
    'recommended_message', 'recv_customer_subscription', 'refund_case',
    'refund_reason_scenario_compensate_customer', 'refund_reason_scenario_deduct_merchant',
    'refund_reason_scenario_penalty_rep', 'refund_user', 'rel_channel_groups', 'rel_upload_groups', 'report_layout',
    'report_paperformat', 'res_bank', 'res_company', 'res_country', 'res_country_group', 'res_country_res_country_group_rel',
    'res_country_state', 'res_currency', 'res_groups', 'res_groups_implied_rel', 'res_lang', 'res_partner_industry', 'res_partner_title',
    'res_users_slack_channel_rel', 'resource_calendar', 'resource_calendar_attendance', 'resource_resource', 'rfm_group', 'rule_group_rel',
    's3_files', 'slack_channel', 'slide_channel', 'team_config_customer_language', 'team_stage_rel', 'uom_category', 'uom_uom',
    'utm_campaign', 'utm_medium', 'utm_source', 'web_tour_tour', 'webhook', 'webhook_address', 'website', 'website_lang_rel', 'website_menu',
    'website_page'
]

def aggregate_xml_id(data):
    data = sorted([str(item) for item in data if item])
    return ','.join(data)

report = open('diff_dicts/report.csv', 'w')
atexit.register(report.close)
report_writer = DictWriter(report, fieldnames=['id','table', 'name', 'column', 'prod', 'preprod'])
report_writer.writeheader()


models = [item[0] for item in run_query('SELECT model FROM ir_model', prod_db)]
table_model = {model.replace('.', '_'): model for model in models}
relations = {item[0] for item in run_query('SELECT name FROM ir_model_relation', prod_db)}

for table in DICTS:
    model = table_model.get(table, 'no_model')
    query = (
        f"SELECT main_table.*, '' as module , ''  as xml_id "
        f"FROM {table} as main_table "
    ) if table in relations else (
        f"SELECT main_table.*, ird.module as module, ird.name  as xml_id "
        f"FROM {table} as main_table "
        f"LEFT JOIN ir_model_data as ird "
        f"ON main_table.id = ird.res_id and "
        f"ird.model = '{model}' "
    )
    prod_df = pandas.read_sql(query, get_connection(prod_db))
    preprod_df = pandas.read_sql(query, get_connection(preprod_db))


    columns_to_drop = list({"create_uid", "create_date", "write_date", "write_uid", 'module'}.intersection(set(prod_df.columns)))
    for df in (prod_df, preprod_df):
        df['xml_id'] = df['module'] + '.' + df['xml_id']
        df.drop(columns=columns_to_drop, inplace=True)

    common_columns = list(set(prod_df.columns).intersection(set(preprod_df.columns)))

    for column in common_columns:
        for df in (prod_df, preprod_df):
            df[column] = df[column].apply(str)

    columns_to_group = list(set(common_columns) - {'xml_id'})
    columns_to_merge = common_columns.copy()
    prod_df = prod_df.fillna('')
    preprod_df = preprod_df.fillna('')
    prod_df = prod_df.groupby(columns_to_group).agg({'xml_id': aggregate_xml_id}).reset_index()
    preprod_df = preprod_df.groupby(columns_to_group).agg({'xml_id': aggregate_xml_id}).reset_index()
    if 'name' in columns_to_merge:
        columns_to_merge = ['name', 'id']
    prod_df["database"] = "prod"
    preprod_df["database"] = "preprod"

    compare_df = pandas.merge(prod_df, preprod_df, how="outer", on=columns_to_merge, suffixes=("_prod", "_preprod"))
    for column in compare_df.columns:
        compare_df[column] = compare_df[column].apply(str)
        compare_df[column] = compare_df[column].replace("nan", '')
        compare_df[column] = compare_df[column].replace("None", '')
        compare_df[column] = compare_df[column].replace("False", '')

    columns_to_check = [column[:-5] for column in compare_df.columns if column.endswith("_prod") and column != "database_prod"]

    def filter_rows(row):
        is_diff = False
        for column in columns_to_check:
            prod_column = f'{column}_prod'
            preprod_column = f'{column}_preprod'
            if row[prod_column] != row[preprod_column]:
                print(f"Table {table} column {column} is different. Prod: {row[prod_column]}, Preprod: {row[preprod_column]}")
                report_writer.writerow({
                    'table': table,
                    'id': row['id'] if 'id' in columns_to_merge else '',
                    'name': row['name'] if 'name' in columns_to_merge else '',
                    'column': column,
                    'prod': row[prod_column],
                    'preprod': row[preprod_column],

                })
                is_diff = True
        return is_diff


    compare_df['diff'] = compare_df.apply(filter_rows, axis=1)
    compare_df = compare_df[compare_df['diff'] == True]

    if not compare_df.empty:
        print(f"Table {table} is different")
        print(compare_df)
        compare_df.to_csv(f"diff_dicts/{table}.csv", index=False)
        print('-'*100)