# odoo  shell -c /etc/odoo/odoo.conf --db_host ${DB_HOST} -d ${DB_NAME} --db_user ${DB_USER}  --no-http

task_id = "0196f3a8-ae65-76c2-b907-b8e8ad7e74ee"
task = env["helpdesk.task"].search([("task_id", "=", task_id)])[0]
task.data["phone"] = task.data["phone"] + " "
task.run_atomic()
