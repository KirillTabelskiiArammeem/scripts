path="/home/kirill/aram/my/scripts/db_fixtures/fixture.sql.zip"

rm -rf /tmp/db
mkdir -p /tmp/db

unzip ${path} -d /tmp/db

export PGPASSWORD=odoo
psql --host 127.0.0.1 -U odoo  -d postgres -c "drop database helpdesk"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create database helpdesk"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create role rdsadmin"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create role dbadmin"

psql --host 127.0.0.1 -U odoo  -d helpdesk -f /tmp/db/dump.sql
psql --host 127.0.0.1 -U odoo  -d helpdesk -c "UPDATE res_users SET password = 'admin' WHERE login = 'admin'"
rm -rf /tmp/db
