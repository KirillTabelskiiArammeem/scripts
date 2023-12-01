odoo  shell --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  --no-http
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  --no-http --stop-after-init -u order
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  --no-http --stop-after-init -u aram_api_client_backend
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  --no-http --stop-after-init -u aram_agent_status
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  --no-http --stop-after-init -u aram_favicon