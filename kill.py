proc = '''
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  1.7  0.8 854284 263536 ?       Ssl  10:42   0:24 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          46  3.8  0.6 2790368 224496 ?      Sl   10:42   0:53 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          48  3.9  0.7 2751436 248504 ?      Sl   10:42   0:54 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          50  4.1  0.7 2869244 240348 ?      Sl   10:42   0:56 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          52  3.9  0.7 2887428 232376 ?      Sl   10:42   0:54 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          54  4.2  0.7 2885892 234664 ?      Sl   10:42   0:58 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          56  3.9  0.7 2940952 240656 ?      Sl   10:42   0:53 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          58  3.9  0.7 2744780 236044 ?      Sl   10:42   0:53 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          60  4.2  0.7 2745804 241392 ?      Sl   10:42   0:58 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          62  4.4  0.7 2880260 231472 ?      Sl   10:42   1:00 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          64  3.9  0.7 2741708 232704 ?      Sl   10:42   0:53 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          66  3.9  0.7 2743244 245756 ?      Sl   10:42   0:54 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          67  3.9  0.7 2745292 237052 ?      Sl   10:42   0:54 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          69  2.3  0.7 1078688 227080 ?      Sl   10:42   0:32 /usr/bin/python3 /usr/bin/odoo gevent --db_host postgres.helpdesk12.erp.sa.toyou.am
root          71  0.1  0.5 588804 163676 ?       SNl  10:42   0:01 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          73  0.0  0.5 588804 163664 ?       SNl  10:42   0:01 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root          75  0.0  0.5 588804 163680 ?       SNl  10:42   0:01 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org
root        2055  0.0  0.0   2392   704 pts/0    Ss   11:04   0:00 sh -c clear; (bash || ash || sh)
root        2062  0.0  0.0   2392   104 pts/0    S    11:04   0:00 sh -c clear; (bash || ash || sh)
root        2063  0.0  0.0   5756  3624 pts/0    S    11:04   0:00 bash
root        2068  0.0  0.0   9396  3184 pts/0    R+   11:04   0:00 ps aux
'''
# ps aux | grep "/usr/bin/python3 /usr/bin/odoo -"
import re
numbers = re.compile('\d+')

lines = [numbers.findall(line) for line in proc.splitlines() if line.strip() if "gevent" not in line and "odoo" in line]
pids = [line[0] for line in lines if line and line[0] != "1"]

cmd = f'kill {" ".join(pids)}'

print(cmd)
