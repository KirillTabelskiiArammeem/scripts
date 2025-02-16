odoo  shell -c /etc/odoo/odoo.conf --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER}  --no-http
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  -u aram_base  -i aram_vault,aram_celery --stop-after-init --no-http
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  --no-http --stop-after-init -u aram_api_client_backend
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  --no-http --stop-after-init -u aram_agent_status
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  --no-http --stop-after-init -u aram_base,aram_sip
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}   --no-http --stop-after-init -i aram_ops_orm
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  -i aram_attachment_s3 --no-http --stop-after-init
supervisorctl stop all
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  -u aram_base --stop-after-init --no-http
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  -u web --stop-after-init --no-http
su odoo --preserve-environment --shell /bin/bash -c "odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD} --db-filter ${ODOO_CONF_DB_FILTER}"

odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD} -u webhook_chat_incoming --stop-after-init --no-http


vault login -method=token $(vault write -field=token auth/mcpprod1/login role=${VAULT_ROLE} jwt=$(cat /run/secrets/kubernetes.io/serviceaccount/token))
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.modules_to_update="aram_base"
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" deploy.toggle.update.app=False
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" integration.toggle.sending_by_kafka.agent_status=True



vault kv get -mount="bss" "${VAULT_NAMESPACE}/applications"

vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" integration.toggle.sending_by_kafka.agent_status=True

vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" ticket_enriching.count.getting.merchant=5
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" ticket_enriching.delay.getting.merchant=6
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" email_notification.filter_event_type.receiving_by_kafka.catalog_events='{"MERCHANT": ["posDisabled"]}'
vault kv patch -mount="bss" "${VAULT_NAMESPACE}/applications" web.base_url.freeze=True


odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  -i aram_orm  --stop-after-init --no-http

odoo -c /etc/odoo/odoo.conf -u aram_base,aram_sip -i aram_callback,aram_attachment_s3,base_fileurl_field,base_fileurl_field_aram --stop-after-init --no-http
