
path=( $ls /home/${USER}/Downloads/odoo_am_dp_12_sand*)

path=${path[-1]}

ls ${path}

rm -rf /tmp/db
mkdir -p /tmp/db

unzip ${path} -d /tmp/db

export PGPASSWORD=odoo
psql --host 127.0.0.1 -U odoo  -d postgres -c "drop database dp"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create database dp"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create role rdsadmin"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create role dbadmin"

psql --host 127.0.0.1 -U odoo  -d dp -f /tmp/db/dump.sql
psql --host 127.0.0.1 -U odoo  -d dp -c "UPDATE res_users SET password = 'admin' WHERE login = 'admin'"
sudo cp -r /tmp/db/filestore/*  ~/aram/dp/odoo-modules-dp-12/datadir/filestore/dp

sudo chmod -R 777 ~/aram/dp/odoo-modules-dp-12/datadir/
rm -rf /tmp/db
