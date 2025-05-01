proc = '''
root           1  6.0  1.1 1044752 364436 ?      Ssl  Apr29  83:06 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root          69  1.9  0.7 1005492 229884 ?      Sl   Apr29  26:02 /usr/bin/python3 /usr/bin/odoo gevent --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_pro
root        3479  0.0  0.0   2392   768 pts/0    Ss   Apr29   0:00 sh -c clear; (bash || ash || sh)
root        3486  0.0  0.0   2392   104 pts/0    S    Apr29   0:00 sh -c clear; (bash || ash || sh)
root        3487  0.0  0.0   5756  3644 pts/0    S+   Apr29   0:00 bash
root        3526  0.2  0.9 1020736 296952 ?      SNl  Apr29   3:33 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root        3527  0.1  0.7 946780 233192 ?       SNl  Apr29   2:27 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root        3529  0.1  0.7 945948 232416 ?       SNl  Apr29   2:10 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       78548  2.2  1.1 2967820 372236 ?      Sl   05:34   1:37 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       79365  2.0  1.1 2824660 375016 ?      Sl   05:57   1:00 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       79488  2.0  1.1 2802124 372820 ?      Sl   06:00   0:56 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       79726  2.2  1.1 2803660 372164 ?      Sl   06:06   0:51 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       79744  2.0  1.1 2821332 363860 ?      Sl   06:07   0:46 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       79754  2.0  1.1 2966028 366116 ?      Sl   06:07   0:48 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       80248  2.0  1.1 2876136 370288 ?      Sl   06:20   0:31 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       80428  1.9  1.1 2072980 364800 ?      Sl   06:25   0:24 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       80551  2.1  1.1 2800844 356716 ?      Sl   06:29   0:21 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       81082  1.6  1.0 1690240 343780 ?      Sl   06:40   0:04 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       81153  1.8  1.0 2070548 342384 ?      Sl   06:42   0:03 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       81236  1.8  1.0 1044624 335632 ?      Sl   06:45   0:00 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --dat
root       81238  0.0  0.0   2392   768 pts/1    Ss   06:45   0:00 sh -c clear; (bash || ash || sh)
root       81245  0.0  0.0   2392   104 pts/1    S    06:45   0:00 sh -c clear; (bash || ash || sh)
root       81246  0.0  0.0   5760  3608 pts/1    S    06:45   0:00 bash
root       81264  0.0  0.0   9396  3108 pts/1    R+   06:46   0:00 ps aux
'''
# ps aux | grep "/usr/bin/python3 /usr/bin/odoo -"
import re
numbers = re.compile('\d+')

lines = [numbers.findall(line) for line in proc.splitlines() if line.strip() if "gevent" not in line and "odoo" in line]
pids = [line[0] for line in lines if line and line[0] != "1"]

cmd = f'kill {" ".join(pids)}'

print(cmd)
