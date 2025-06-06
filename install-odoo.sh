curent_dir=$(pwd)
pip install /Users/kirill/aram/ops/vatnumber
pip install /Users/kirill/aram/ops/suds-jurko
cd /Users/kirill/aram/platform/odoo
git checkout current
pip install .

cd $curent_dir
