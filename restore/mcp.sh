
path="/home/kirill/Downloads/odoo_am_mcp_12_sand_2023-05-29_06-07-05.zip"

rm -rf /tmp/db
mkdir -p /tmp/db

unzip ${path} -d /tmp/db

export PGPASSWORD=odoo
psql --host 127.0.0.1 -U odoo  -d postgres -c "drop database mcp"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create database mcp"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create role rdsadmin"
psql --host 127.0.0.1 -U odoo  -d postgres -c "create role dbadmin"

psql --host 127.0.0.1 -U odoo  -d mcp -f /tmp/db/dump.sql
psql --host 127.0.0.1 -U odoo  -d mcp -c "UPDATE res_users SET password = 'admin' WHERE login = 'admin'"
sudo cp -r /tmp/db/filestore/*  ~/aram/mcp/odoo-modules-mcp-12/datadir/filestore/mcp

sudo chmod -R 777 ~/aram/mcp/odoo-modules-mcp-12/datadir/
rm -rf /tmp/db
