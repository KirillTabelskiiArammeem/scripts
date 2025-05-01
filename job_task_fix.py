# odoo  shell -c /etc/odoo/odoo.conf --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER}  --no-http

task_id = "0196805e-f173-722e-b25b-eb07a516db9b"
task = env["helpdesk.task"].search([("task_id", "=", task_id)])[0]
task.data["phone"] = task.data["phone"] + " "
task.run_atomic()
