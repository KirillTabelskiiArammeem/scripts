
path="/home/kirill/Downloads/odoo_am_crm_12_sand_2023-07-03_06-05-36.zip"

rm -rf /tmp/db
mkdir -p /tmp/db

unzip ${path} -d /tmp/db

export PGPASSWORD=odoo
psql --host 127.0.0.1 -U odoo  -d postgres -c "drop database crm"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create database crm"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create role rdsadmin"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create role dbadmin"

psql --host 127.0.0.1 -U odoo  -d crm -f /tmp/db/dump.sql
psql --host 127.0.0.1 -U odoo  -d crm -c "UPDATE res_users SET password = 'admin' WHERE login = 'admin'"
sudo cp -r /tmp/db/filestore/*  ~/aram/crm/odoo-modules-crm-12/datadir/filestore/crm

sudo chmod -R 777 ~/aram/crm/odoo-modules-crm-12/datadir/
rm -rf /tmp/db
