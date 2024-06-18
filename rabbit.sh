
rabbitmqctl add_user "odoo"
rabbitmqctl add_vhost odoo --description "odoo celery" --default-queue-type classic --tags odoo,celery
rabbitmqctl set_permissions -p "odoo" "rabbit" ".*" ".*" ".*"
rabbitmqctl set_permissions -p "odoo" "odoo" ".*" ".*" ".*"

