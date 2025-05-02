
path=( $ls /home/${USER}/Downloads/odoo_am_helpdesk_12_sand*)
path=${path[-1]}

ls ${path}

rm -rf /tmp/db
mkdir -p /tmp/db

unzip ${path} -d /tmp/db

export PGPASSWORD=odoo
psql --host 127.0.0.1 -U odoo  -d postgres -c "drop database helpdesk"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create database helpdesk"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create role rdsadmin"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create role dbadmin"

psql --host 127.0.0.1 -U odoo  -d helpdesk -f /tmp/db/dump.sql
psql --host 127.0.0.1 -U odoo  -d helpdesk -c "UPDATE res_users SET password = 'admin^2Admin' WHERE login = 'admin'"
psql --host 127.0.0.1 -U odoo  -d helpdesk -c "UPDATE res_users SET password_write_date = '$(date '+%Y-%m-%d %H:%M:%S')' WHERE login = 'admin'"
psql --host 127.0.0.1 -U odoo  -d helpdesk -c "UPDATE ir_config_parameter SET value = 'http://127.0.0.1:8069' WHERE key = 'web.base.url'"

mkdir -p ~/aram/helpdesk/helpdesk/datadir/filestore/helpdesk
sudo cp -r /tmp/db/filestore/*  ~/aram/helpdesk/helpdesk/datadir/filestore/helpdesk
sudo chmod -R 777 ~/aram/helpdesk/helpdesk/datadir/
rm -rf /tmp/db
