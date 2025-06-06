import subprocess
import os
from pathlib import Path

def run_cmd(cmd):
    """Run a command in the shell."""
    print(f"Running command: {cmd}")
    env = os.environ.copy()
    env["PGPASSWORD"] = "odoo"  # Set the PGPASSWORD environment variable
    result = subprocess.run(cmd, shell=True, check=False, text=True, env=env, capture_output=True)
    print(f"Command output: {result.stdout}")
    print(f"Command error: {result.stderr}")
    return result

home = Path.home()

downloads = home / "Downloads"
path  = list(downloads.glob("odoo_am_helpdesk_12_sand*"))[-1]


run_cmd("rm -rf /tmp/db")
run_cmd("mkdir -p /tmp/db")
run_cmd(f"unzip '{path}' -d /tmp/db")
run_cmd('psql --host 127.0.0.1 -U odoo  -d postgres -c "drop database helpdesk"')
run_cmd('psql --host 127.0.0.1 -U odoo  -d postgres -c "create database helpdesk"')
run_cmd('psql --host 127.0.0.1 -U odoo  -d postgres -c "create role rdsadmin"')
run_cmd('psql --host 127.0.0.1 -U odoo  -d postgres -c "create role dbadmin"')
run_cmd('psql --host 127.0.0.1 -U odoo  -d helpdesk -f /tmp/db/dump.sql')
run_cmd("""psql --host 127.0.0.1 -U odoo  -d helpdesk -c "UPDATE res_users SET password = 'admin^2Admin' WHERE login = 'admin'" """)
run_cmd("""psql --host 127.0.0.1 -U odoo  -d helpdesk -c "UPDATE res_users SET password_write_date = '$(date '+%Y-%m-%d %H:%M:%S')' WHERE login = 'admin'" """)
run_cmd("mkdir -p ~/aram/ops/support/helpdesk/datadir/filestore/helpdesk")
run_cmd("cp -r /tmp/db/filestore/* ~/aram/ops/support/helpdesk/datadir/filestore/helpdesk")
run_cmd("chmod -R 777 ~/aram/ops/support/helpdesk/datadir/")
run_cmd("rm -rf /tmp/db")
