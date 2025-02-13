export PGPASSWORD=odoo
psql --host 127.0.0.1 -U odoo  -d postgres -c "drop database helpdesk_"
psql --host 127.0.0.1 -U odoo  -d postgres -c "CREATE DATABASE helpdesk_ WITH TEMPLATE helpdesk OWNER odoo"
