odoo  shell --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  --no-http
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  -i aram_vault --stop-after-init --no-http
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  --no-http --stop-after-init -u aram_api_client_backend
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  --no-http --stop-after-init -u aram_agent_status
odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}  --no-http --stop-after-init -u aram_base


odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD}

su odoo --preserve-environment --shell /bin/bash -c "odoo --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER} -w ${DB_PASSWORD} --db-filter ${ODOO_CONF_DB_FILTER}"

