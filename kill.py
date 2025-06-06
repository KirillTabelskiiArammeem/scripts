proc = '''
odoo           1 15.0  0.8 859860 275908 ?       Ssl  13:51   0:08 /usr/local/bin/python3.10 /usr/local/bin/odoo --db_host postgres.hel
odoo          76  0.2  0.5 614224 177408 ?       Sl   13:51   0:00 /usr/local/bin/python3.10 /usr/local/bin/odoo --db_host postgres.hel
odoo          78  0.4  0.5 617296 185076 ?       Sl   13:51   0:00 /usr/local/bin/python3.10 /usr/local/bin/odoo --db_host postgres.hel
odoo          80  1.4  0.5 1041244 190196 ?      Sl   13:51   0:00 /usr/local/bin/python3.10 /usr/local/bin/odoo --db_host postgres.hel
odoo          82  1.8  0.5 1041244 190716 ?      Sl   13:51   0:00 /usr/local/bin/python3.10 /usr/local/bin/odoo --db_host postgres.hel
odoo          84  0.5  0.5 617296 185000 ?       Sl   13:51   0:00 /usr/local/bin/python3.10 /usr/local/bin/odoo --db_host postgres.hel
odoo          86  2.0  0.5 1571704 190336 ?      Sl   13:51   0:01 /usr/local/bin/python3.10 /usr/local/bin/odoo --db_host postgres.hel
odoo          88  0.7  0.5 616272 182684 ?       Sl   13:51   0:00 /usr/local/bin/python3.10 /usr/local/bin/odoo --db_host postgres.hel
odoo          90  1.5  0.5 1571704 190096 ?      Sl   13:51   0:00 /usr/local/bin/python3.10 /usr/local/bin/odoo --db_host postgres.hel
odoo          92  0.3  0.5 614224 177576 ?       Sl   13:51   0:00 /usr/local/bin/python3.10 /usr/local/bin/odoo --db_host postgres.hel
odoo          94  0.4  0.5 617296 184984 ?       Sl   13:51   0:00 /usr/local/bin/python3.10 /usr/local/bin/odoo --db_host postgres.hel
odoo          95  3.1  0.3 216804 116348 ?       S    13:51   0:01 /usr/local/bin/python3.10 /usr/local/bin/odoo gevent --db_host postg
odoo         171  0.0  0.0   2600   960 pts/0    Ss   13:52   0:00 sh -c clear; (bash || ash || sh)
odoo         179  0.0  0.0   2600   148 pts/0    S    13:52   0:00 sh -c clear; (bash || ash || sh)
'''
# ps aux | grep "/usr/bin/python3 /usr/bin/odoo -"
import re
numbers = re.compile('\d+')

lines = [numbers.findall(line) for line in proc.splitlines() if line.strip() if "gevent" not in line and "bin/odoo" in line]
pids = [line[0] for line in lines if line and line[0] != "1"]

cmd = f'kill {" ".join(pids)}'

print(cmd)
