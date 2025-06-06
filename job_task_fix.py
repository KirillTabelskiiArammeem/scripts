# odoo  shell -c /etc/odoo/odoo.conf --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER}  --no-http

task_id = "01971a03-2f7e-7855-9bc1-841eef64be41"
task = env["helpdesk.task"].search([("task_id", "=", task_id)])[0]
task.data["phone"] = task.data["phone"] + " "
task.run_atomic()
