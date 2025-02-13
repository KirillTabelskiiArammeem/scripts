proc = '''
root           1  0.8  0.3 769748 250192 ?       Ssl  Jan30   4:00 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root          67  1.3  0.3 999880 224076 ?       Sl   Jan30   6:29 /usr/bin/python3 /usr/bin/odoo gevent --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root          68  0.1  0.2 896736 185656 ?       SNl  Jan30   0:47 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root          70  0.1  0.2 900320 186284 ?       SNl  Jan30   0:39 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root          72  0.1  0.2 898784 184092 ?       SNl  Jan30   0:54 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root        5665  0.0  0.0   2392   768 pts/0    Ss   Jan30   0:00 sh -c clear; (bash || ash || sh)
root        5672  0.0  0.0   2392   104 pts/0    S    Jan30   0:00 sh -c clear; (bash || ash || sh)
root        5673  0.0  0.0   5756  3556 pts/0    S    Jan30   0:00 bash
root        5798  0.1  0.3 823744 198040 pts/0   Sl+  Jan30   0:26 /usr/bin/python3 /usr/bin/odoo shell --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org -d odoo_am_helpdesk_12_prod --db_user odoo_am_helpdesk_12_prod --no-http -c /etc/odoo/odoo.conf
root       22374  1.9  0.7 3969980 499064 ?      Sl   Jan30   5:21 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root       22645  2.0  0.6 5011136 432744 ?      Sl   Jan30   5:45 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root       22652  1.9  0.6 4437464 436944 ?      Sl   Jan30   5:26 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root       23184  1.8  0.6 3932300 402440 ?      Sl   Jan30   4:52 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root       23207  1.8  0.6 5005424 401088 ?      Sl   Jan30   5:04 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root       23271  1.7  0.6 3371936 404568 ?      Sl   Jan30   4:42 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root       23533  2.1  0.6 5528288 415404 ?      Sl   Jan30   5:40 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root       24390  1.7  0.6 4440280 395992 ?      Sl   00:05   4:30 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root       24506  1.5  0.6 3399024 405884 ?      Sl   00:07   3:53 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root       24845  1.6  0.5 4437128 377836 ?      Sl   00:15   3:57 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root       26903  1.4  0.6 3340988 400252 ?      Sl   01:15   2:35 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root       29207  1.3  0.5 3198400 347520 ?      Sl   03:44   0:27 /usr/bin/python3 /usr/bin/odoo --db_host postgres.helpdesk12.erp.sa.toyou.amhub.org --db_port 5432 --db_user odoo_am_helpdesk_12_prod --database odoo_am_helpdesk_12_prod --db-filter ^odoo_am_helpdesk_12_prod$
root       29753  0.0  0.0   2392   772 pts/1    Ss   04:18   0:00 sh -c clear; (bash || ash || sh)
root       29760  0.0  0.0   2392   108 pts/1    S    04:18   0:00 sh -c clear; (bash || ash || sh)
root       29761  0.0  0.0   5756  3592 pts/1    S    04:18   0:00 bash
root       29779  0.0  0.0   9396  3144 pts/1    R+   04:18   0:00 ps aux
root      4953  0.0  0.0   4984  2108 pts/1    S+   14:32   0:00 grep /usr/bin/python3 /usr/bin/odoo --db_host
'''
# ps aux | grep "/usr/bin/python3 /usr/bin/odoo -"
import re
numbers = re.compile('\d+')

lines = [numbers.findall(line)[0] for line in proc.splitlines() if line.strip()]
cmd = f'kill {" ".join(lines[1:])}'

print(cmd)
