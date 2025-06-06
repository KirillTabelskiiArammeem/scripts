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
path  = list(downloads.glob("odoo_am_dp_12_sand*"))[-1]


run_cmd("rm -rf /tmp/db")
run_cmd("mkdir -p /tmp/db")
run_cmd(f"unzip '{path}' -d /tmp/db")
run_cmd('psql --host 127.0.0.1 -U odoo  -d postgres -c "drop database dp"')
run_cmd('psql --host 127.0.0.1 -U odoo  -d postgres -c "create database dp"')
run_cmd('psql --host 127.0.0.1 -U odoo  -d postgres -c "create role rdsadmin"')
run_cmd('psql --host 127.0.0.1 -U odoo  -d postgres -c "create role dbadmin"')
run_cmd('psql --host 127.0.0.1 -U odoo  -d dp -f /tmp/db/dump.sql')
run_cmd("""psql --host 127.0.0.1 -U odoo  -d dp -c "UPDATE res_users SET password = 'admin^2Admin' WHERE login = 'admin'" """)
run_cmd("""psql --host 127.0.0.1 -U odoo  -d dp -c "UPDATE res_users SET password_write_date = '$(date '+%Y-%m-%d %H:%M:%S')' WHERE login = 'admin'" """)
run_cmd("mkdir -p /Users/kirill/aram/ops/rep_supply/driver-portal/datadir/dp")
run_cmd("cp -r /tmp/db/filestore/* /Users/kirill/aram/ops/rep_supply/driver-portal/datadir/dp")
run_cmd("rm -rf /tmp/db")
